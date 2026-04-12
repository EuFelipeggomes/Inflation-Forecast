# Inflation-Forecast

# 📈 Previsão de Inflação (IPCA) — Brasil

Modelo de séries temporais para previsão do IPCA (Índice de Preços ao Consumidor Amplo), o índice oficial de inflação do Brasil, utilizando dados históricos do Banco Central do Brasil.

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Dados](#dados)
- [Modelos](#modelos)
- [Resultados](#resultados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Requisitos](#requisitos)
- [Conclusão Crítica](#conclusão-crítica)
- [Próximos Passos](#próximos-passos)

---

## 🎯 Sobre o Projeto

### Problema

A inflação é um dos principais indicadores macroeconômicos do Brasil. Prever o IPCA com antecedência é relevante para decisões de política monetária, planejamento empresarial e finanças pessoais. Este projeto desenvolve e compara modelos de séries temporais capazes de prever o IPCA mensal para os próximos 6 meses.

### Objetivo

Desenvolver um pipeline reprodutível de previsão de inflação que:

- Coleta dados históricos diretamente da API do Banco Central do Brasil (SGS)
- Realiza análise exploratória completa da série temporal
- Treina e compara dois modelos: **ARIMA** e **Prophet**
- Avalia os modelos com divisão temporal correta (sem embaralhamento de dados)
- Gera previsões futuras com intervalos de confiança

---

## 📊 Dados

**Fonte:** [Banco Central do Brasil — SGS (Sistema Gerenciador de Séries Temporais)](https://www.bcb.gov.br/estabilidadefinanceira/historicotaxasjuros)

| Atributo | Detalhe |
|---|---|
| Série | IPCA — Variação mensal (%) |
| Código SGS | 433 |
| Frequência | Mensal |
| Período utilizado | Janeiro/2000 — presente |
| Fonte de coleta | API pública do BCB via `python-bcb` |

### Divisão temporal

```
|--------- TREINO ---------|---- TESTE ----|---- PREVISÃO ----|
  jan/2000 → dez/2022        jan → dez/2023    jan/2024 →
```

> ⚠️ Os dados **nunca são embaralhados**. A ordem temporal é sempre respeitada.

---

## 🤖 Modelos

### Baseline (referência mínima)

Antes de qualquer modelo, dois baselines foram estabelecidos como piso de desempenho:

- **Naive Forecast:** prevê que o próximo mês será igual ao mês atual
- **Mean Forecast:** prevê sempre a média histórica do período de treino

Qualquer modelo que não supere esses baselines é considerado inútil.

### ARIMA

Modelo clássico de séries temporais composto por três componentes:

- **AR (AutoRegressivo):** usa valores passados da própria série
- **I (Integrado):** aplica diferenciação para garantir estacionariedade
- **MA (Média Móvel):** usa erros passados do modelo

Os parâmetros `(p, d, q)` foram selecionados a partir dos gráficos ACF e PACF e confirmados via critério AIC com `auto_arima`.

### Prophet

Modelo desenvolvido pelo Meta que decompõe a série em:

```
y(t) = tendência + sazonalidade + feriados + erro
```

Configurado com `seasonality_mode='multiplicative'` para capturar a sazonalidade do IPCA, que tende a ser proporcional ao nível da série.

---

## 📉 Resultados

> Os valores abaixo são exemplos de estrutura. Atualize com os resultados reais após executar o projeto.

### Métricas — Período de teste (2023)

| Modelo | MAE | RMSE |
|---|---|---|
| Naive Baseline | — | — |
| Mean Baseline | — | — |
| ARIMA | — | — |
| Prophet | — | — |

### Previsão — Próximos 6 meses

| Mês | Previsão IPCA (%) | Intervalo Inferior | Intervalo Superior |
|---|---|---|---|
| Mês +1 | — | — | — |
| Mês +2 | — | — | — |
| Mês +3 | — | — | — |
| Mês +4 | — | — | — |
| Mês +5 | — | — | — |
| Mês +6 | — | — | — |

Os resultados completos estão em `results/metrics/comparison.csv` e os gráficos em `results/figures/`.

---

## 🗂️ Estrutura do Projeto

```
inflation-forecast/
│
├── data/
│   ├── raw/                    # Dados brutos da API do BCB (nunca modificar)
│   └── processed/              # Dados limpos e prontos para modelagem
│
├── notebooks/
│   └── eda.ipynb               # Análise exploratória da série temporal
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Coleta de dados via API do BCB
│   ├── preprocessing.py        # Limpeza, tratamento e divisão temporal
│   ├── model_arima.py          # Treinamento e previsão com ARIMA
│   ├── model_prophet.py        # Treinamento e previsão com Prophet
│   └── evaluation.py           # Métricas, baseline e comparação
│
├── results/
│   ├── figures/                # Gráficos gerados
│   └── metrics/                # Tabelas de métricas em CSV
│
│── check_setup.py              # Script que verifica setup do projeto
├── config.py                   # Parâmetros centralizados do projeto
├── main.py                     # Pipeline completo (ponto de entrada)
├── requirements.txt            # Dependências do projeto
├── .gitignore
└── README.md
```

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/inflation-forecast.git
cd inflation-forecast
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o pipeline completo

```bash
python main.py
```

Isso irá:
1. Coletar os dados mais recentes da API do BCB
2. Realizar o pré-processamento
3. Treinar os modelos ARIMA e Prophet
4. Calcular as métricas de avaliação
5. Gerar os gráficos comparativos
6. Exportar os resultados em `results/`

### 5. Exploração interativa (opcional)

## 📦 Requisitos

- Python 3.10+

| Biblioteca | Finalidade |
|---|---|
| `pandas` | Manipulação de dados e séries temporais |
| `numpy` | Operações numéricas |
| `matplotlib` | Visualizações |
| `seaborn` | Visualizações estatísticas |
| `statsmodels` | Modelo ARIMA, testes estatísticos |
| `prophet` | Modelo Prophet |
| `pmdarima` | Seleção automática de parâmetros ARIMA |
| `scikit-learn` | Cálculo de métricas |
| `python-bcb` | Acesso à API do Banco Central do Brasil |

---

## 🔎 Conclusão Crítica

> Esta seção deve ser preenchida após a execução do projeto com os resultados reais.

Perguntas que este projeto deve responder objetivamente:

- O ARIMA superou o baseline naive? Em quanto?
- O Prophet superou o ARIMA no período de teste?
- O erro aumenta proporcionalmente com o horizonte de previsão?
- Os modelos falharam em algum período específico? Por quê?
- Qual modelo você usaria em produção e em quais condições ele falharia?

---

## 👤 Autor

Desenvolvido como projeto de ciência de dados aplicado a macroeconomia brasileira.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
