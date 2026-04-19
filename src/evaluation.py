import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def baseline_naive(train: pd.DataFrame, test: pd.DataFrame) -> pd.Series:
    naive = train["ipca_pct"].shift(1).reindex(test.index, method="nearest")
    return naive


def baseline_mean(train: pd.DataFrame, test: pd.DataFrame) -> pd.Series:
    media = train["ipca_pct"].mean()
    mean_forecast = pd.Series(media, index=test.index)
    return mean_forecast


def calculate_metrics(test: pd.DataFrame, prevision: pd.Series, name: str) -> dict:
    real = test["ipca_pct"]
    mae = mean_absolute_error(real, prevision)
    rmse = np.sqrt(mean_squared_error(real, prevision))

    print(f"{name:20s} | MAE: {mae:.4f} | RMSE: {rmse:.4f}")

    return {"modelo": name, "mae": mae, "rmse": rmse}


def save_metrics(lista_metricas: list, path: str) -> None:
    df = pd.DataFrame(lista_metricas)
    df = df.sort_values("mae")
    filename = f"{path}/comparison.csv"
    df.to_csv(filename, index=False)
    print(f"\nMétricas salvas em: {filename}")
    print(df.to_string(index=False))