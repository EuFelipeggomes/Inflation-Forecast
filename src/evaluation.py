import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
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

def plot_comparativo(test: pd.DataFrame, previsoes: dict, save_path: str) -> None:
    fig, ax = plt.subplots(figsize=(14, 6))

    # Série real
    ax.plot(test.index, test["ipca_pct"],
            color="black", linewidth=2, label="Real", zorder=5)

    # Previsões de cada modelo
    cores = {
        "Prophet": "steelblue",
        "ARIMA":   "darkorange",
        "Mean":    "green",
        "Naive":   "gray"
    }

    for nome, pred in previsoes.items():
        ax.plot(test.index, pred,
                color=cores.get(nome, "purple"),
                linewidth=1.5,
                linestyle="--",
                label=nome,
                alpha=0.8)

    ax.set_title("IPCA — Real vs Previsto (2022)", fontsize=14)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Variação (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{save_path}/figures/real_vs_previsto.png", dpi=150)
    plt.close()
    print("Gráfico salvo em results/figures/real_vs_previsto.png")


def plot_erros(test: pd.DataFrame, previsoes: dict, save_path: str) -> None:
    fig, ax = plt.subplots(figsize=(14, 5))

    cores = {
        "Prophet": "steelblue",
        "ARIMA":   "darkorange",
        "Mean":    "green"
    }

    for nome, pred in previsoes.items():
        if nome == "Naive":
            continue
        erro = (test["ipca_pct"] - pred).abs()
        ax.plot(test.index, erro,
                color=cores.get(nome, "purple"),
                linewidth=1.5,
                label=nome,
                alpha=0.8)

    ax.set_title("Erro Absoluto por Mês — 2022", fontsize=14)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Erro Absoluto (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{save_path}/figures/erros_por_mes.png", dpi=150)
    plt.close()
    print("Gráfico salvo em results/figures/erros_por_mes.png")