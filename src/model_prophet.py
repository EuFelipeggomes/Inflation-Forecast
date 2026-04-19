import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import config


def prepare_prophet_df(df: pd.DataFrame) -> pd.DataFrame:
    # Prophet exige colunas com nomes exatos: ds (data) e y (valor)
    prophet_df = df.reset_index()
    prophet_df.columns = ["ds", "y"]
    return prophet_df


def train_prophet(train: pd.DataFrame) -> Prophet:
    print("Treinando modelo Prophet...")

    train_df = prepare_prophet_df(train)

    model = Prophet(
        seasonality_mode="multiplicative",  # sazonalidade proporcional ao nível da série
        yearly_seasonality=True,
        weekly_seasonality=False,           # dados mensais — sem sazonalidade semanal
        daily_seasonality=False,
        interval_width=0.95
    )

    model.fit(train_df)
    print("Prophet treinado com sucesso.")
    return model


def forecast_prophet(model: Prophet, steps: int) -> pd.Series:
    future = model.make_future_dataframe(periods=steps, freq="MS")
    forecast = model.predict(future)

    # Retorna apenas os steps finais (período de teste)
    pred = forecast.tail(steps)[["ds", "yhat"]].set_index("ds")["yhat"]
    return pred


def plot_prophet_components(model: Prophet, train: pd.DataFrame) -> None:
    train_df = prepare_prophet_df(train)
    future = model.make_future_dataframe(periods=12, freq="MS")
    forecast = model.predict(future)

    model.plot_components(forecast)
    plt.tight_layout()
    plt.savefig("results/figures/prophet_components.png", dpi=150)
    plt.close()
    print("Componentes Prophet salvos em results/figures/prophet_components.png")


def forecast_futuro_prophet(df: pd.DataFrame, steps: int) -> pd.DataFrame:
    print(f"Retreinando Prophet com todos os dados ({len(df)} meses)...")

    modelo_final = train_prophet(df)
    future = modelo_final.make_future_dataframe(periods=steps, freq="MS")
    forecast = modelo_final.predict(future)

    resultado = forecast.tail(steps)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    return resultado


def plot_previsao_futura(df: pd.DataFrame, forecast_arima, conf_int,
                         forecast_prophet: pd.DataFrame, save_path: str) -> None:
    fig, ax = plt.subplots(figsize=(16, 6))

    # Últimos 24 meses históricos para contexto
    historico = df.tail(24)
    ax.plot(historico.index, historico["ipca_pct"],
            color="black", linewidth=1.5, label="Histórico")

    # Previsão ARIMA
    ax.plot(forecast_arima.index, forecast_arima,
            color="darkorange", linewidth=1.5,
            linestyle="--", label="ARIMA")
    ax.fill_between(conf_int.index,
                    conf_int.iloc[:, 0],
                    conf_int.iloc[:, 1],
                    color="darkorange", alpha=0.15)

    # Previsão Prophet
    prophet_index = pd.to_datetime(forecast_prophet["ds"])
    ax.plot(prophet_index, forecast_prophet["yhat"],
            color="steelblue", linewidth=1.5,
            linestyle="--", label="Prophet")
    ax.fill_between(prophet_index,
                    forecast_prophet["yhat_lower"],
                    forecast_prophet["yhat_upper"],
                    color="steelblue", alpha=0.15)

    ax.axvline(df.index[-1], color="gray",
               linestyle=":", linewidth=1, label="Início da previsão")
    ax.axhline(0, color="red", linewidth=0.8, linestyle="--", alpha=0.5)

    ax.set_title(f"Previsão IPCA — Próximos {len(forecast_arima)} meses", fontsize=14)
    ax.set_xlabel("Data")
    ax.set_ylabel("Variação (%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{save_path}/figures/previsao_futura.png", dpi=150)
    plt.close()
    print("Previsão futura salva em results/figures/previsao_futura.png")