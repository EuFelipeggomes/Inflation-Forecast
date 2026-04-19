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