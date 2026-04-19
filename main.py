import logging

import config
from src.data_loader import data_loader
from src.evaluation import calculate_metrics, baseline_naive, baseline_mean, save_metrics
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

if __name__ == "__main__":
    main()