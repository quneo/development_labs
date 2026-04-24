from typing import List, Optional

import pandas as pd


def filterQuerySet(
    stations: Optional[List[str]] = None,
    hour: Optional[int] = None,
    data_path: str = "data/passenger_flow.csv"
) -> pd.DataFrame:

    data = pd.read_csv(data_path)
    data["date"] = pd.to_datetime(data["date"])

    if stations:
        data = data[data["station"].isin(stations)]

    if hour is not None:
        data = data[data["hour"] == hour]

    return data


def get_all_data(data_path: str = "data/passenger_flow.csv") -> pd.DataFrame:
    data = pd.read_csv(data_path)
    data["date"] = pd.to_datetime(data["date"])
    return data
