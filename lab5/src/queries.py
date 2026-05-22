from pathlib import Path
from typing import List, Optional

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent / "data" / "passenger_flow.csv"


def filterQuerySet(
    stations: Optional[List[str]] = None,
    hour: Optional[int] = None,
    data_path: str = str(DATA_PATH)
) -> pd.DataFrame:

    data = pd.read_csv(data_path)
    data["date"] = pd.to_datetime(data["date"])

    if stations:
        data = data[data["station"].isin(stations)]

    if hour is not None:
        data = data[data["hour"] == hour]

    return data


def filter_dataframe(
    data: pd.DataFrame,
    stations: Optional[List[str]] = None,
    hour: Optional[int] = None
) -> pd.DataFrame:

    filtered_data = data.copy()
    filtered_data["date"] = pd.to_datetime(filtered_data["date"])

    if stations:
        filtered_data = filtered_data[filtered_data["station"].isin(stations)]

    if hour is not None:
        filtered_data = filtered_data[filtered_data["hour"] == hour]

    return filtered_data


def get_all_data(data_path: str = str(DATA_PATH)) -> pd.DataFrame:
    data = pd.read_csv(data_path)
    data["date"] = pd.to_datetime(data["date"])
    return data
