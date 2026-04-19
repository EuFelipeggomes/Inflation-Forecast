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
| Período utilizado | Janeiro/1995 a Dezembro/2022 |
| Fonte de coleta | API pública do BCB via `python-bcb` |

### Divisão temporal

```
|--------- TREINO ----------|---- TESTE ----|---- PREVISÃO ----|
  jan/1995 → dez/2021         jan → dez/2022    jan/2023 →
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

Os parâmetros `(p, d, q)` foram selecionados a partir dos gráficos ACF e PACF e confirmados via critério AIC com `auto_arima`. O modelo selecionado foi **ARIMA(1, 0, 2) com intercepto** — AIC de 205.51.

### Prophet

Modelo desenvolvido pelo Meta que decompõe a série em:

```
y(t) = tendência + sazonalidade + feriados + erro
```

Configurado com `seasonality_mode='multiplicative'` para capturar a sazonalidade do IPCA, que tende a ser proporcional ao nível da série.

---

## 📉 Resultados

### Métricas — Período de teste (2022)

| Modelo | MAE | RMSE |
|---|---|---|
| **Prophet** | **0.4490** | **0.5913** |
| ARIMA | 0.4529 | 0.6271 |
| Mean Baseline | 0.4567 | 0.6274 |
| Naive Baseline | 0.6183 | 0.7843 |

> Prophet venceu em ambas as métricas. O RMSE significativamente menor indica que o Prophet cometeu menos erros grandes ao longo do ano de 2022.

### Previsão — Próximos 6 meses (a partir de jan/2023)

Os valores abaixo refletem a previsão gerada pelo Prophet, modelo com melhor desempenho no período de teste:

| Mês | Prophet (%) | Intervalo Inferior | Intervalo Superior |
|---|---|---|---|
| Jan/2023 | ~0.60 | ~0.10 | ~1.10 |
| Fev/2023 | ~0.55 | ~0.00 | ~1.10 |
| Mar/2023 | ~0.55 | ~-0.05 | ~1.15 |
| Abr/2023 | ~0.50 | ~-0.10 | ~1.10 |
| Mai/2023 | ~0.45 | ~-0.15 | ~1.05 |
| Jun/2023 | ~0.45 | ~-0.15 | ~1.05 |

> Os valores exatos estão em `results/metrics/previsao_futura.csv`.

Os resultados completos estão em `results/metrics/` e os gráficos em `results/figures/`.

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
│   └── evaluation.py           # Métricas, baselines, gráficos e exportação
│
├── results/
│   ├── figures/                # Gráficos gerados
│   │   ├── real_vs_previsto.png
│   │   ├── erros_por_mes.png
│   │   ├── arima_diagnostics.png
│   │   ├── prophet_components.png
│   │   └── previsao_futura.png
│   └── metrics/                # Tabelas de métricas em CSV
│       ├── comparison.csv
│       └── previsao_futura.csv
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
git clone https://github.com/EuFelipeggomes/Inflation-Forecast.git
cd Inflation-Forecast
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


### 4. Verifique o Setup do Projeto

```bash
python check_setup.py
```

### 5. Execute o pipeline completo

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

```bash
jupyter notebook notebooks/eda.ipynb
```

---

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

### O Prophet venceu — mas por margem pequena

O Prophet obteve MAE de 0.449 contra 0.457 do baseline Mean — uma melhoria de apenas 1.7%. O ARIMA ficou entre os dois com MAE de 0.453. A margem pequena não é surpresa: 2022 foi um ano extraordinariamente difícil de prever.

### O evento que quebrou todos os modelos

Em julho de 2022 o governo federal zerou impostos sobre combustíveis, causando deflação de -0.68% — o maior choque negativo da série desde 1998. Nenhum modelo previu isso porque é um evento de política fiscal discricionária, impossível de capturar com dados históricos. O erro de todos os modelos em julho foi acima de 1 ponto percentual.

### Quando o Prophet se saiu melhor

O Prophet capturou a tendência de queda do segundo semestre de 2022 melhor que o ARIMA, resultando em RMSE significativamente menor (0.591 vs 0.627). Isso sugere que o Prophet é mais adequado para períodos de mudança de tendência.

### Quando o ARIMA se saiu melhor

No primeiro semestre, onde a série estava em alta, o ARIMA convergiu mais rapidamente para os valores reais. Para períodos de inflação estável e crescente, o componente autorregressivo forte (ar.L1 = 0.84) é uma vantagem.

### Qual modelo usar em produção

O Prophet seria a escolha para previsão de médio prazo (3–6 meses) por capturar melhor mudanças de tendência. O ARIMA seria preferível para previsão de curtíssimo prazo (1–2 meses) onde a persistência autorregressiva é mais relevante.

### Limitação principal

Ambos os modelos univariados ignoram completamente as variáveis que mais movem a inflação: taxa Selic, câmbio, preço do petróleo e choques de oferta. Um modelo multivariado (SARIMAX ou Prophet com regressores externos) seria o próximo passo natural.

---

## 🚀 Próximos Passos

- [ ] Implementar **walk-forward validation** para estimativa mais robusta do desempenho
- [ ] Adicionar variáveis exógenas: Taxa Selic, câmbio USD/BRL, preço do petróleo
- [ ] Testar modelo **SARIMAX** com variáveis externas
- [ ] Criar dashboard interativo com Streamlit para visualização das previsões
- [ ] Automatizar atualização mensal dos dados e retreinamento do modelo

---

## 👤 Autor

**Felipe Gomes** — [@EuFelipeggomes](https://github.com/EuFelipeggomes)

Projeto de ciência de dados aplicado a macroeconomia brasileira, desenvolvido como parte do portfólio de Machine Learning.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
