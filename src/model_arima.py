import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import config


def find_arima_params(train: pd.DataFrame) -> tuple:
    print("Buscando melhores parâmetros ARIMA...")

    model = auto_arima(
        train["ipca_pct"],
        start_p=0, max_p=3,
        start_q=0, max_q=3,
        d=0,
        seasonal=False,
        information_criterion="aic",
        trace=True,
        error_action="ignore",
        suppress_warnings=True,
        stepwise=True
    )

    print(f"\nMelhor modelo: ARIMA{model.order}")
    print(f"AIC: {model.aic():.4f}")
    return model.order


def train_arima(train: pd.DataFrame, order: tuple) -> ARIMA:
    print(f"Treinando ARIMA{order}...")

    model = ARIMA(train["ipca_pct"], order=order)
    fitted = model.fit()

    print(fitted.summary())
    return fitted


def forecast_arima(fitted_model, steps: int) -> pd.Series:
    forecast = fitted_model.forecast(steps=steps)
    return forecast


def plot_diagnostics(fitted_model) -> None:
    fitted_model.plot_diagnostics(figsize=(14, 8))
    plt.tight_layout()
    plt.savefig("results/figures/arima_diagnostics.png", dpi=150)
    plt.close()
    print("Diagnóstico salvo em results/figures/arima_diagnostics.png")

def forecast_futuro_arima(df: pd.DataFrame, steps: int) -> pd.Series:
    print(f"Retreinando ARIMA com todos os dados ({len(df)} meses)...")

    order = find_arima_params(df)
    modelo_final = train_arima(df, order)

    forecast = modelo_final.get_forecast(steps=steps)
    pred = forecast.predicted_mean
    conf_int = forecast.conf_int()

    return pred, conf_int