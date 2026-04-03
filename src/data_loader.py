from datetime import datetime
from pathlib import Path
from bcb import sgs
import pandas as pd
import config


def data_loader() -> pd.DataFrame:
    try:
        ipca = sgs.get(
            config.IPCA_SERIES_CODE,
            start=config.START_DATE,
            end=config.TRAIN_END_DATE
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar IPCA: {e}")

    if ipca.empty:
        raise ValueError("Dataset IPCA retornou vazio.")

    output_path = Path(config.RAW_DATA_PATH)
    output_path.mkdir(parents=True, exist_ok=True)

    today = datetime.today().strftime("%Y%m%d")
    filename = output_path / f"ipca_raw_{today}.csv"

    ipca.to_csv(filename)

    print(f"Arquivo salvo em: {filename}")
    return ipca