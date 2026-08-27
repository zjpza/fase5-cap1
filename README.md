# 🌾 FarmTech Solutions — PBL Fase 5 | Machine Learning & Nuvem

> **Predição de rendimento de safra com regressão supervisionada, clusterização de tendências e estimativa de custos em nuvem AWS.**

---

## 👨‍🎓 Integrantes

| Nome | RM | GitHub |
|------|----|--------|
| Henrique Sanches Silva | RM 570527 | [@HenriqueSanchesSilva](https://github.com/HenriqueSanchesSilva) |
| João Pedro Zavanela Andreu | RM 570231 | [@zjpza](https://github.com/zjpza) |
| Kayck Gabriel Evangelista da Silva | RM 572331 | [@Kayckxz](https://github.com/Kayckxz) |
| Luis Henrique Laurentino Boschi | RM 571352 | [@lhboschi](https://github.com/lhboschi) |
| Patrick Borges de Melo | RM 574030 | [@Trickmelo](https://github.com/Trickmelo) |

**Tutora:** Sabrina Otoni
**Coordenador:** André Godoi

> **FIAP — Inteligência Artificial | Turma: 1TIAOB-2026**

---

## 📜 Visão Geral

Este repositório contempla as **duas entregas obrigatórias** da Fase 5:

| Entrega | Tema | Onde está |
|---------|------|-----------|
| **Entrega 1** | Machine Learning — análise exploratória, clusterização e 5 modelos de regressão para prever rendimento de safra | [`notebooks/`](notebooks/) |
| **Entrega 2** | Computação em Nuvem — estimativa de custos AWS comparando São Paulo (BR) vs Virgínia do Norte (EUA) | Seção [☁️ Entrega 2 — Nuvem AWS](#-entrega-2--nuvem-aws) abaixo |

O detalhamento técnico completo (código, gráficos, achados e conclusões) está no **Jupyter Notebook**. Este README é apenas uma introdução que conduz o leitor até ele.

---

## 🎯 Entrega 1 — Machine Learning

A FarmTech Solutions atende uma fazenda de médio porte (≈200 ha) que produz várias culturas. A partir de uma base com condições de solo e clima (precipitação, umidade, temperatura), o grupo:

1. **Analisa exploratoriamente** a base `crop_yield.csv`;
2. **Clusteriza** os rendimentos para identificar tendências e cenários discrepantes (outliers);
3. **Constrói 5 modelos preditivos** com algoritmos distintos de regressão supervisionada, seguindo boas práticas de ML (split, pipeline, validação cruzada, métricas pertinentes).

### Variáveis do dataset

| Variável | Descrição |
|----------|-----------|
| `Cultura` | Nome da safra (categórica) |
| `Precipitação (mm dia 1)` | Chuva em mm/dia |
| `Umidade específica a 2 metros (g/kg)` | Vapor de água por kg de ar seco |
| `Umidade relativa a 2 metros (%)` | Umidade relativa do ar |
| `Temperatura a 2 metros (°C)` | Temperatura a 2 m do solo |
| `Rendimento` | Rendimento em toneladas por hectare (alvo) |

### 📒 Notebook

➡️ [`notebooks/JoaoPedroZavanelaAndreu_rm570231_pbl_fase5.ipynb`](notebooks/JoaoPedroZavanelaAndreu_rm570231_pbl_fase5.ipynb)

> O notebook contém células de código executadas e comentadas, além de células markdown com a análise, achados, pontos fortes e limitações do trabalho.

### 🎥 Vídeo demonstrativo (Entrega 1)

[🔗 Link do vídeo no YouTube — não listado](_PLACEHOLDER_VIDEO_ENTREGA1_)

---

## ☁️ Entrega 2 — Nuvem AWS

### Cenário

A Machine Learning da Entrega 1 precisa ser hospedada em nuvem para receber dados dos sensores da fazenda e executar a inferência. A missão é cotar, na **calculadora da AWS** (modelo On-Demand — 100%), uma máquina Linux simples comparando:

- **Região São Paulo (BR)** — `sa-east-1`
- **Região Virgínia do Norte (EUA)** — `us-east-1`

### Configuração exigida

| Recurso | Especificação |
|---------|---------------|
| vCPU | 2 |
| Memória | 1 GiB |
| Rede | Até 5 Gigabit |
| Armazenamento (HD) | 50 GB |

### Instância selecionada

A instância **`t3.micro`** atende exatamente à configuração exigida: 2 vCPU, 1 GiB de RAM,
rede "Up to 5 Gigabit" e armazenamento via EBS. (A `t3.small` tem 2 GiB — mais RAM do que o
pedido; a `t3.micro` é a correspondência exata.)

| Instância | vCPU | RAM | Rede | Região |
|-----------|------|-----|------|--------|
| `t3.micro` | 2 | 1 GiB | Até 5 Gbps | sa-east-1 / us-east-1 |

### Comparativo de custos (On-Demand, Linux, 730 h/mês)

Valores em USD, **fontes oficiais AWS** (referência 2025): tabela pública On-Demand do Amazon EC2
e tabela de preços do Amazon EBS — ambas em aws.amazon.com. BRL indicativo a ≈ R$ 5,50 / US$ 1.

**Fontes oficiais AWS:**
- EC2 On-Demand (t3.micro): <https://aws.amazon.com/ec2/pricing/on-demand/> — us-east-1 $0,0104/h; sa-east-1 $0,0168/h (Linux, On-Demand).
- Amazon EBS (gp3): <https://aws.amazon.com/ebs/pricing/> — us-east-1 $0,08/GB-mês; sa-east-1 $0,152/GB-mês.

| Componente | São Paulo (sa-east-1) | Virgínia (us-east-1) |
|------------|----------------------|----------------------|
| Instância t3.micro (On-Demand) | $0,0168/h → **$12,26/mês** | $0,0104/h → **$7,59/mês** |
| Volume EBS 50 GB (gp3) | $0,152/GB-mês → **$7,60/mês** | $0,08/GB-mês → **$4,00/mês** |
| **Total mensal (USD)** | **$19,86** | **$11,59** |
| Total mensal (BRL ≈5,50) | ≈ R$ 109,23 | ≈ R$ 63,75 |

> São Paulo custa **~71% mais caro** que a Virgínia neste perfil (instância + EBS).

### Evidências das cotações AWS

![Cotação AWS — São Paulo](assets/cotacao_sa_east_1.png)

![Cotação AWS — Virgínia](assets/cotacao_us_east_1.png)


![Comparativo de custos AWS](assets/custo_aws_comparativo.png)

### Justificativa técnica

> **Considerando:** (1) necessidade de acesso rápido aos dados dos sensores e (2) restrições
> legais para armazenamento no exterior.

- **Latência de rede:** os sensores da fazenda enviam dados continuamente para a API. Um
  round-trip Brasil→Virgínia custa da ordem de ~120–150 ms, contra <10 ms dentro de
  `sa-east-1` (São Paulo) — sem contar que links internacionais apresentam jitter e perda
  de pacotes mais variáveis que o backbone nacional. Para ingestão contínua de telemetria
  e inferência em tempo (quase) real da saúde da plantação, a baixa latência reduz o
  risco de timeout nas leituras frequentes e melhora a responsividade percebida.
- **Restrição legal / residência dos dados:** o cenário impõe restrições legais ao
  armazenamento no exterior. Manter instância e volume EBS em `sa-east-1` mantém
  processamento e armazenamento sob jurisdição brasileira, eliminando por completo o
  risco regulatório de transferência internacional e simplificando auditorias junto a
  órgãos nacionais.
  - **Observação sobre a LGPD:** dados climáticos e de cultura, isoladamente, não são
    dados pessoais — a LGPD (Lei 13.709/2018) não incide sobre eles. Porém, se a solução
    evoluir para agregar dados pessoais (telemetria de operadores, geolocalização
    vinculada a responsáveis, clientes da API), a lei passa a valer **e** a transferência
    internacional de dados pessoais exigiria as salvaguardas do art. 33 (jurisdição
    adequada, cláusulas contratuais padrão, consentimento específico etc.). Hospedar em
    `sa-east-1` remove essa fricção jurídica por desenho.
- **Viabilidade econômica:** São Paulo é ~71% mais cara ($19,86 vs $11,59/mês), diferença
  de ~$8,27/mês (~R$ 46). Em valor absoluto o prêmio é pequeno para uma única instância e
  é absorvido pelo ganho de latência e pela conformidade. (Se no futuro a frota escalar
  para dezenas de máquinas, o percentual volta à mesa — mas aí a comparação deve incluir
  Savings Plans, fora do escopo On-Demand desta entrega.)
- **Contraponto (análise crítica):** se a carga fosse de processamento em lote, sem
  restrição legal e sem sensibilidade a latência, `us-east-1` seria a escolha racional —
  economia de ~40% no conjunto. O que decide este caso não é o custo, e sim a combinação
  "dados em tempo real + barreira legal".
- **Conclusão:** escolhe-se **`sa-east-1` (São Paulo)**. O ganho de latência (<10 ms) e a
  eliminação do risco de transferência internacional de dados superam o prêmio de custo,
  que permanece trivial em valor absoluto neste porte.

### 🎥 Vídeo demonstrativo (Entrega 2)

[🔗 Link do vídeo no YouTube — não listado](_PLACEHOLDER_VIDEO_ENTREGA2_)

---

## 🚀 Como executar o notebook

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
git clone https://github.com/zjpza/fase5-cap1.git
cd fase5-cap1

python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### Executar

```bash
jupyter notebook notebooks/JoaoPedroZavanelaAndreu_rm570231_pbl_fase5.ipynb
```

> O dataset `crop_yield.csv` deve estar em `data/`.

---

## 📁 Estrutura do repositório

```
fase5-cap1/
├── README.md                              # Intro + Entrega 2 (AWS) + Ir Além
├── requirements.txt                       # Dependências (ML + API)
├── .gitignore
├── data/
│   └── crop_yield.csv                     # Dataset (Entrega 1)
├── notebooks/
│   └── JoaoPedroZavanelaAndreu_rm570231_pbl_fase5.ipynb   # Entrega 1 — ML
├── src/
│   ├── api/                               # "Ir Além" Opção 2 — API FastAPI
│   │   ├── main.py                        #   app + /health + /predict
│   │   └── schemas.py                     #   modelos Pydantic
│   ├── esp32/                             # "Ir Além" Opção 1 — ESP32 (Wokwi)
│   │   ├── farmtech_esp32.ino             #   firmware (sensores + POST)
│   │   ├── diagram.json                   #   circuito Wokwi
│   │   └── libraries.txt                  #   libs do Wokwi
│   └── ml/models/                         # modelos serializados (Entrega 1)
│       ├── best_regressor.pkl
│       ├── health_classifier.pkl
│       └── label_map.json
└── assets/                                # Figuras da EDA, modelos e arquitetura
    ├── eda_*.png  cluster_*.png  outliers_*.png  models_*.png
    ├── arquitetura_ir_alem.png            # diagrama do Ir Além
    └── cotacao_sa_east_1.png  cotacao_us_east_1.png  # (Entrega 2 — AWS, a adicionar manualmente)
```

---

## 🧭 Ir Além

Implementamos **duas** opções do "Ir Além", que se integram ponta-a-ponta num pipeline
único: o ESP32 (Opção 1) coleta os dados de sensores e envia via Wi-Fi para a API (Opção 2),
que classifica a saúde da plantação com o modelo de ML treinado na Entrega 1.

| Opção | Título | Onde está |
|-------|--------|-----------|
| **1** | Sistema de Coleta e Comunicação de Dados Usando ESP32 + Wi-Fi | [`src/esp32/`](src/esp32/) |
| **2** | Classificação da Saúde de Plantações Usando Machine Learning e ESP32 | [`src/api/`](src/api/) + [`src/ml/models/`](src/ml/models/) |

![Arquitetura Ir Além (ponta-a-ponta)](assets/arquitetura_ir_alem.png)

> Diagrama completo do fluxo: ESP32 (Wokwi) → Wi-Fi → API FastAPI → Pipeline sklearn → Resposta no Serial.

---

## 🟢 Ir Além — Opção 1: Coleta de Dados com ESP32 + Wi-Fi

> **Título do enunciado:** *Sistema de Coleta e Comunicação de Dados Usando ESP32 Integrado ao Wi-Fi.*

### Objetivo e escolha dos sensores

O firmware [`src/esp32/farmtech_esp32.ino`](src/esp32/farmtech_esp32.ino) roda num **ESP32
DevKitC V4** (chip clássico ESP-WROOM-32, part `board-esp32-devkit-c-v4`) simulado no
[Wokwi](https://wokwi.com). A cada ciclo ele:

1. lê **temperatura** e **umidade relativa** do **DHT22**;
2. lê o **sensor de chuva** (analógico, emulado por potenciômetro no Wokwi) e estima a
   precipitação;
3. calcula a **umidade específica** (g/kg) via fórmula meteorológica de Magnus a partir de
   T e UR (reproduz os valores do dataset de treino — ex.: ~17,7 g/kg a 26 °C / 83 %);
4. conecta ao Wi-Fi e envia `POST /predict` com `{crop, precipitation, specific_humidity,
   relative_humidity, temperature}`;
5. exibe no **monitor serial** a classificação `Saudável` / `Não Saudável` e a confiança.

### Justificativa dos sensores e alinhamento com a FarmTech

Os sensores espelham as features climáticas usadas no treino do classificador:

- **DHT22** (temperatura + umidade relativa): fornece diretamente `temperature` e
  `relative_humidity` e, via fórmula de Magnus, a `specific_humidity` — as três features
  derivadas de clima. Precisão ±0,5 °C / ±2 % UR, adequada a campo.
- **Sensor de chuva analógico:** aproxima a `precipitation`. No Wokwi é emulado por um
  potenciômetro (saída 0–3,3 V mapeada para a faixa de precipitação do dataset, com
  inversão: maior tensão = seco = menor chuva). Em campo seria um módulo de chuva real,
  calibrado para a escala de treino.
- **Alinhamento FarmTech:** a fazenda de médio porte já usa sensores climáticos para
  irrigation; o ESP32 reusa essa infraestrutura para alimentar o classificador de saúde em
  tempo real, sem instalar novos sensores — apenas o firmware + a API. A cultura (`crop`) é
  configurada por nó (`#define CROP`), permitindo um ESP32 por talhão.

### Circuito (Wokwi)

`src/esp32/diagram.json` monta: **ESP32 DevKitC V4** (`board-esp32-devkit-c-v4`) + DHT22
(GPIO4) + potenciômetro como sensor de chuva analógico (GPIO34, ADC1 — compatível com
Wi-Fi). Bibliotecas em `src/esp32/libraries.txt` (Adafruit DHT + Unified Sensor).

### Como simular

1. Suba a API da Opção 2 em um host alcançável pelo ESP32 e ajuste `API_HOST` no sketch.
2. Abra o Wokwi com os arquivos de `src/esp32/` (`.ino` + `diagram.json` + `libraries.txt`).
3. Inicie a simulação; o monitor serial mostra as leituras e a classificação a cada ciclo.

> **Nota de simulação:** a rede do Wokwi é simulada — para um teste ponta-a-ponta real,
> exponha a API num host público (ex.: tunnel/ngrok) e aponte `API_HOST` para ele.

### Arquivos

| Arquivo | Função |
|---------|--------|
| [`src/esp32/farmtech_esp32.ino`](src/esp32/farmtech_esp32.ino) | Firmware ESP32 (DHT22, chuva, Wi-Fi, POST) |
| [`src/esp32/diagram.json`](src/esp32/diagram.json) | Circuito Wokwi (ESP32 + DHT22 + pot. chuva) |
| [`src/esp32/libraries.txt`](src/esp32/libraries.txt) | Dependências de bibliotecas do Wokwi |

### ✅ Entregáveis (Opção 1)

- [x] ESP32 real (simulado no Wokwi) com comunicação Wi-Fi funcional
- [x] Dois sensores distintos (DHT22 + sensor de chuva) alinhados ao contexto FarmTech
- [x] Dados coletados enviados à API (POST `/predict`)
- [x] Código-fonte comentado e organizado no GitHub
- [x] Figura da arquitetura do circuito/tecnologias (`assets/arquitetura_ir_alem.png`)
- [x] Justificativa clara dos sensores (seção acima)
- [ ] Vídeo de demonstração (~5 min, YouTube "não listado") —
  [🔗 link a adicionar](_PLACEHOLDER_VIDEO_IRALEM_1_)

---

## 🔵 Ir Além — Opção 2: Classificação da Saúde da Plantação com ML

> **Título do enunciado:** *Classificação da Saúde de Plantações Usando Machine Learning e ESP32.*

### Objetivo

A API carrega o classificador de saúde serializado (treinado na Entrega 1) e retorna
**Saudável** ou **Não Saudável** (relativo à mediana de cada cultura), com a confiança da
predição. Os dados chegam em tempo real do ESP32 da Opção 1.

### Como rodar

```bash
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload --port 8000
```

Interface interativa (Swagger UI): <http://localhost:8000/docs>

### Endpoints

| Método | Rota | Descrição |
|---------|------|-----------|
| `GET` | `/health` | Status do serviço (`{"status":"ok","model_loaded":true}`) |
| `POST` | `/predict` | Classifica a saúde de uma observação |

**Exemplo de request (`POST /predict`):**

```json
{
  "crop": "Cocoa, beans",
  "precipitation": 2248.92,
  "specific_humidity": 17.72,
  "relative_humidity": 83.4,
  "temperature": 26.01
}
```

**Resposta:**

```json
{ "health": "Saudável", "confidence": 0.84 }
```

> Valores aceitos para `crop`: `Cocoa, beans`, `Oil palm fruit`, `Rice, paddy`,
> `Rubber, natural` (exatamente como no dataset). Outros valores são rejeitados (HTTP 422).

### Arquitetura do modelo

O `.pkl` serializado **é o pipeline sklearn completo** (`ColumnTransformer` +
`RandomForestClassifier`), logo o pré-processamento servido pela API é idêntico ao do
treino — sem leakage nem inconsistência. A API apenas mapeia os nomes amigáveis do
esquema de entrada (em inglês) para os nomes PT-BR esperados pelo `ColumnTransformer`
(descritos em `src/ml/models/label_map.json`).

### Arquivos

| Arquivo | Função |
|---------|--------|
| [`src/api/main.py`](src/api/main.py) | App FastAPI (lifespan, `/health`, `/predict`) |
| [`src/api/schemas.py`](src/api/schemas.py) | Modelos Pydantic de entrada/saída |
| [`src/ml/models/health_classifier.pkl`](src/ml/models/health_classifier.pkl) | Pipeline sklearn serializado (classificador de saúde) |
| [`src/ml/models/label_map.json`](src/ml/models/label_map.json) | Mapeamento de features/rótulos (esquema ↔ ColumnTransformer) |

### ✅ Entregáveis (Opção 2)

- [x] Modelo de ML funcional (RandomForestClassifier) treinado e serializado
- [x] Integração ESP32 → API (coleta em tempo real via Opção 1)
- [x] API estável servindo inferência (`/predict` + `/health`)
- [x] Validação com dados novos (inferência coerente, confiança informada)
- [x] Código-fonte comentado e organizado no GitHub
- [x] Figura da arquitetura com as tecnologias (`assets/arquitetura_ir_alem.png`)
- [x] Justificativa clara de sensores e metodologia
- [ ] Vídeo de demonstração (~5 min, YouTube "não listado") —
  [🔗 link a adicionar](_PLACEHOLDER_VIDEO_IRALEM_2_)
