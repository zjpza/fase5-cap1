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
| `Temperatura a 2 metros (ºC)` | Temperatura a 2 m do solo |
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

<!-- TODO: preencher após cotação na calculadora AWS -->
<!-- Candidata: t3.small (2 vCPU, 2 GiB) — verificar se existe linha com exatamente 1 GiB e 2 vCPU -->

| Instância | vCPU | RAM | Região |
|-----------|------|-----|--------|
| _a definir_ | 2 | 1 GiB | sa-east-1 / us-east-1 |

### Comparativo de custos

<!-- Inserir prints da calculadora AWS em assets/ e referenciar aqui -->

| Componente | São Paulo (sa-east-1) | Virgínia (us-east-1) |
|------------|----------------------|----------------------|
| Instância (On-Demand, mensal) | _R$ / US$_ | _R$ / US$_ |
| Volume EBS 50 GB (gp3) | _R$ / US$_ | _R$ / US$_ |
| **Total mensal** | _R$ / US$_ | _R$ / US$_ |

![Cotação AWS — São Paulo](assets/cotacao_sa_east_1.png)
![Cotação AWS — Virgínia](assets/cotacao_us_east_1.png)

### Justificativa técnica

> **Considerando:** (1) necessidade de acesso rápido aos dados dos sensores e (2) restrições legais para armazenamento no exterior.

<!-- TODO: desenvolver justificativa abordando:
- Latência de rede: round-trip BR→EUA (~120 ms) vs local (<5 ms)
- Conformidade com a LGPD: dados de sensores agrícolas em território nacional
- Viabilidade econômica vs conformidade/latência
- Conclusão: região escolhida e por quê
-->

### 🎥 Vídeo demonstrativo (Entrega 2)

[🔗 Link do vídeo no YouTube — não listado](_PLACEHOLDER_VIDEO_ENTREGA2_)

---

## 🚀 Como executar o notebook

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
git clone https://github.com/zjpza/fase-5-pbl-agro.git
cd fase-5-pbl-agro

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
fase-5-pbl-agro/
├── README.md                              # Este arquivo (intro + Entrega 2 AWS)
├── requirements.txt                       # Dependências Python
├── .gitignore
├── data/
│   └── crop_yield.csv                     # Dataset (a adicionar)
├── notebooks/
│   └── JoaoPedroZavanelaAndreu_rm570231_pbl_fase5.ipynb   # Entrega 1 — ML
├── src/                                   # Código auxiliar (se necessário)
└── assets/                                # Prints da calculadora AWS e figuras
    ├── cotacao_sa_east_1.png
    └── cotacao_us_east_1.png
```

---

## 🧭 Ir Além *(opcional, sem nota)*

Se o grupo optar por um dos desafios "Ir Além", a documentação ficará nesta seção.

- [ ] **Opção 1** — Sistema de coleta e comunicação de dados com ESP32 + Wi-Fi
- [ ] **Opção 2** — Classificação da saúde de plantações com ML + ESP32

> _A definir conforme disponibilidade do grupo._