/*
 * ============================================================================
 *  FarmTech Solutions — PBL Fase 5 | "Ir Além" Opção 1
 *  ESP32 (Wokwi) — Coleta de sensores + envio HTTP POST para a API da Issue #3
 * ============================================================================
 *
 *  Fluxo:
 *    DHT22  (temperatura + umidade relativa)  ─┐
 *    sensor de chuva (analógico, via pot. na simulação) ─┤─> ESP32 monta JSON
 *                                                        └> POST /predict
 *                                                           -> API FastAPI
 *                                                              -> classificador
 *                                                                 de saúde
 *    Resposta {"health":"Saudável"|"Não Saudável","confidence":..} exibida no Serial.
 *
 *  Hardware (diagram.json):
 *    - ESP32 DevKitC V4 (part Wokwi: board-esp32-devkit-c-v4)
 *    - DHT22 em GPIO4  (VCC=3V3, GND=GND, SDA=GPIO4)
 *    - "Sensor de chuva" emulado por POTENCIÔMETRO em GPIO34 (ADC1, compatível c/ WiFi)
 *
 *  Bibliotecas (resolvidas pelo Wokwi):
 *    - WiFi.h, HTTPClient.h        (core do ESP32)
 *    - DHT.h (Adafruit DHT sensor)  (suporte nativo ao DHT22 no Wokwi)
 *
 *  Autor: grupo FarmTech — Issue #4
 * ============================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// ---------------------------------------------------------------------------
// 1. Configuração de rede e destino da API
// ---------------------------------------------------------------------------
// No Wokwi a rede é simulada: qualquer SSID/senha conecta. Em hardware real,
// troque pelo SSID/senha reais e aponte API_HOST para o host onde a API roda
// (ex.: ngrok ou IP da nuvem). A API da Issue #3 escuta em /predict.
#define WIFI_SSID     "Wokwi-GUEST"        // SSID da rede Wi-Fi
#define WIFI_PASSWORD ""                   // senha (vazia para rede aberta simulada)

// Host da API FastAPI. Para testar ponta-a-ponta fora do Wokwi, exponha a API
// num host alcançável pela rede do ESP32 (ex.: tunnel) e ajuste aqui.
#define API_HOST      "http://127.0.0.1:8000"
#define API_ENDPOINT  API_HOST "/predict"

// Cultura monitorada neste nó ESP32. Deve ser um dos valores aceitos pela API:
// "Cocoa, beans" | "Oil palm fruit" | "Rice, paddy" | "Rubber, natural"
#define CROP          "Cocoa, beans"

// ---------------------------------------------------------------------------
// 2. Mapeamento de pinos
// ---------------------------------------------------------------------------
#define DHT_PIN       4      // pino de dados do DHT22
#define RAIN_PIN      34     // pino analógico do "sensor de chuva" (ADC1_CH6)

// ---------------------------------------------------------------------------
// 3. Parâmetros do sensor de chuva
// ---------------------------------------------------------------------------
// O ADC do ESP32 lê 0..4095. Um sensor de chuva real dá tensão MENOR quanto
// mais molhado. Aqui o potenciômetro emula essa saída analógica.
// A escala de precipitação do dataset de treino é ~2000..3000 (mm equivalentes),
// por isso mapeamos a leitura para esse intervalo. CALIBRAR em campo.
#define RAIN_MIN_ADC    0      // leitura quando totalmente molhado
#define RAIN_MAX_ADC  4095     // leitura quando seco
#define RAIN_MIN_MM  2000.0f   // precipitação mínima (dataset)
#define RAIN_MAX_MM  3000.0f   // precipitação máxima (dataset)

// ---------------------------------------------------------------------------
// 4. Inicialização do sensor DHT22
// ---------------------------------------------------------------------------
DHT dht(DHT_PIN, DHT22);

// ---------------------------------------------------------------------------
// 5. Calcula umidade específica (g/kg) a partir de T (°C) e UR (%)
//    Fórmula meteorológica padrão (Magnus para pressão de saturação):
//      e_s = 6.112 * exp(17.67*T / (T+243.5))   [hPa]   (pressão de saturação)
//      e   = (UR/100) * e_s                     [hPa]   (pressão de vapor real)
//      q   = 622 * e / (P - e)                   [g/kg]  (umidade específica)
//    P = 1013.25 hPa (pressão ao nível do mar). Reproduz ~17.7 g/kg a 26°C/83%
//    (coerente com a feature do dataset de treino).
// ---------------------------------------------------------------------------
float specificHumidity(float tempC, float relHumPct) {
  const float P = 1013.25;  // pressão atmosférica padrão (hPa)
  float e_s = 6.112f * expf(17.67f * tempC / (tempC + 243.5f));
  float e   = (relHumPct / 100.0f) * e_s;
  float q   = 622.0f * e / (P - e);
  return q;  // g/kg
}

// ---------------------------------------------------------------------------
// 6. Converte leitura analógica do sensor de chuva em precipitação (mm)
//    Leitura alta (seco) -> precipitação baixa; leitura baixa (molhado) -> alta.
// ---------------------------------------------------------------------------
float rainToMm(int adc) {
  if (adc < RAIN_MIN_ADC) adc = RAIN_MIN_ADC;
  if (adc > RAIN_MAX_ADC) adc = RAIN_MAX_ADC;
  // Inverte: quanto menor o ADC, maior a chuva; normaliza 0..1 e escala p/ mm.
  float wetness = (float)(RAIN_MAX_ADC - adc) / (float)(RAIN_MAX_ADC - RAIN_MIN_ADC);
  return RAIN_MIN_MM + wetness * (RAIN_MAX_MM - RAIN_MIN_MM);
}

// ---------------------------------------------------------------------------
// 7. Extrai o valor de "health" do JSON de resposta (parse minimalista).
//    Resposta esperada: {"health":"Saudável","confidence":0.84}
//    Evita depender de biblioteca JSON externa.
// ---------------------------------------------------------------------------
String extractHealth(const String &body) {
  const String key = "\"health\":\"";
  int i = body.indexOf(key);
  if (i < 0) return "";
  int start = i + key.length();
  int end = body.indexOf('"', start);
  if (end < 0) return "";
  return body.substring(start, end);
}

float extractConfidence(const String &body) {
  const String key = "\"confidence\":";
  int i = body.indexOf(key);
  if (i < 0) return -1.0f;
  return body.substring(i + key.length()).toFloat();
}

// ---------------------------------------------------------------------------
// 8. setup() — inicializa serial, sensor DHT e Wi-Fi
// ---------------------------------------------------------------------------
void setup() {
  Serial.begin(115200);          // monitor serial para log e resultado
  delay(500);
  dht.begin();                   // inicializa DHT22

  // Conecta ao Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Wi-Fi conectado. IP: ");
  Serial.println(WiFi.localIP());
}

// ---------------------------------------------------------------------------
// 9. loop() — a cada CICLO, lê sensores, envia POST e exibe a classificação
// ---------------------------------------------------------------------------
#define CICLO_MS 5000   // intervalo entre leituras

void loop() {
  // (a) Lê temperatura e umidade relativa do DHT22
  float tempC = dht.readTemperature();        // °C
  float relH  = dht.readHumidity();           // %
  if (isnan(tempC) || isnan(relH)) {          // leitura falhou?
    Serial.println("[ERRO] Falha na leitura do DHT22. Reiniciando ciclo.");
    delay(CICLO_MS);
    return;
  }

  // (b) Lê sensor de chuva (analógico) e estima precipitação
  int rainAdc = analogRead(RAIN_PIN);
  float precip = rainToMm(rainAdc);

  // (c) Calcula umidade específica (g/kg) a partir de T e UR
  float specH = specificHumidity(tempC, relH);

  // Log dos sensores
  Serial.printf("Sensores -> T=%.2f°C  UR=%.2f%%  q=%.2f g/kg  chuva(ADC=%d)=%.1f mm\n",
                tempC, relH, specH, rainAdc, precip);

  // (d) Envia POST para a API se houver rede
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_ENDPOINT);             // endpoint /predict
    http.addHeader("Content-Type", "application/json");

    // Monta o corpo JSON exatamente como o esquema Pydantic espera.
    char body[256];
    snprintf(body, sizeof(body),
             "{\"crop\":\"%s\","
             "\"precipitation\":%.2f,"
             "\"specific_humidity\":%.2f,"
             "\"relative_humidity\":%.2f,"
             "\"temperature\":%.2f}",
             CROP, precip, specH, relH, tempC);

    int code = http.POST(body);           // envia requisição
    if (code > 0) {
      String resp = http.getString();    // corpo da resposta
      String health = extractHealth(resp);
      float conf = extractConfidence(resp);
      Serial.printf("API respondeu (HTTP %d): %s\n", code, resp.c_str());
      if (health.length() > 0) {
        Serial.printf(">>> Classificação de saúde: %s  (confiança: %.2f)\n",
                      health.c_str(), conf);
      }
    } else {
      Serial.printf("[ERRO] POST falhou: %s\n",
                    http.errorToString(code).c_str());
    }
    http.end();
  } else {
    Serial.println("[AVISO] Sem Wi-Fi. Tentando reconectar...");
    WiFi.reconnect();
  }

  delay(CICLO_MS);   // aguarda até o próximo ciclo
}