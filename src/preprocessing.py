from pathlib import Path
import pandas as pd
import config
from datetime import datetime


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    date = datetime.today().strftime("%Y%m%d")
    current_month = datetime.today().strftime("%Y%m")

    output_path = Path(config.PROCESSED_DATA_PATH)
    output_path.mkdir(parents=True, exist_ok=True)

    existing = list(output_path.glob(f"ipca_clean_{current_month}*.csv"))
    if existing:
        print(f"Dados processados do mês atual já existem. Carregando: {existing[0]}")
        df = pd.read_csv(existing[0], index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index)
        return df

    df.columns = ["ipca_pct"]
    df.index = pd.to_datetime(df.index)
    df = df.resample("MS").mean()

    nulls = df["ipca_pct"].isnull().sum()
    if nulls > 0:
        print(f"Atenção: {nulls} valores nulos encontrados. Aplicando interpolação.")
        df["ipca_pct"] = df["ipca_pct"].interpolate(method="time")
    else:
        print("Nenhum valor nulo encontrado.")

    filename = output_path / f"ipca_clean_{date}.csv"
    df.to_csv(filename)
    print(f"Dado processado salvo em: {filename}")

    return df