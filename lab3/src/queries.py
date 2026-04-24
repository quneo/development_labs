import pandas as pd
from data_generate import CategoryName, Region 
from datetime import datetime
from typing import List, Optional


def filterQuerySet(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    categories: Optional[List[CategoryName]] = None,
    regions: Optional[List[Region]] = None,
    data_path: str = "data/dataset.csv"
) -> pd.DataFrame:
    
    data = pd.read_csv(data_path)
    data['date'] = pd.to_datetime(data['date'])
    
    if start_date:
        data = data[data["date"] > start_date]

    if end_date:
        data = data[data["date"] < end_date]

    if categories:
        data = data[data["category"].isin(categories)]
    
    if regions:
        data = data[data["region"].isin(regions)]
    
    return data