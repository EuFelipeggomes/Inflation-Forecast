import logging

import config
from src.data_loader import data_loader
from src.evaluation import calculate_metrics, baseline_naive, baseline_mean, save_metrics
from src.model_arima import find_arima_params, train_arima, forecast_arima, plot_diagnostics
from src.model_prophet import train_prophet, forecast_prophet, plot_prophet_components
from src.preprocessing import clean_data, split_temporal

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("Coletando dados...")
    df_raw = data_loader()

    log.info("Preprocessando...")
    df = clean_data(df_raw)

    log.info("Dividindo treino e teste...")
    train, test = split_temporal(df, config.TRAIN_END_DATE, config.TEST_START_DATE)

    log.info("Calculando baselines...")
    pred_naive = baseline_naive(train, test)
    pred_mean = baseline_mean(train, test)

    metricas_naive = calculate_metrics(test, pred_naive, name="Naive")
    metricas_mean = calculate_metrics(test, pred_mean, name="Mean")

    save_metrics([metricas_naive, metricas_mean], path=config.RESULTS_PATH)

    log.info("Treinando ARIMA...")
    order = find_arima_params(train)
    modelo_arima = train_arima(train, order)

    log.info("Gerando previsões ARIMA...")
    pred_arima = forecast_arima(modelo_arima, steps=len(test))

    metricas_arima = calculate_metrics(test, pred_arima, name="ARIMA")

    save_metrics(
        [metricas_naive, metricas_mean, metricas_arima],
        path=config.RESULTS_PATH
    )

    log.info("Analisando resíduos...")
    plot_diagnostics(modelo_arima)

    log.info("Treinando Prophet...")
    modelo_prophet = train_prophet(train)

    log.info("Gerando previsões Prophet...")
    pred_prophet = forecast_prophet(modelo_prophet, steps=len(test))
    pred_prophet.index = test.index  # garante alinhamento de índices

    metricas_prophet = calculate_metrics(test, pred_prophet, name="Prophet")

    save_metrics(
        [metricas_naive, metricas_mean, metricas_arima, metricas_prophet],
        path=config.RESULTS_PATH
    )

    log.info("Plotando componentes Prophet...")
    plot_prophet_components(modelo_prophet, train)

if __name__ == "__main__":
    main()