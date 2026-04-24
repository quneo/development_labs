from typing import List
from datetime import datetime, timedelta
import pandas as pd
from pydantic import BaseModel
from enum import Enum
import random 
import numpy as np


class CategoryName(str, Enum):
    mushrooms = "mushrooms"
    fruits = "fruits"
    vegetable = "vegetables"
    greens = "greens"
    flowers = "flowers"


class Region(str, Enum):
    krasnoyarsk = "krasnoyarsk"
    irkutsk = "irkutsk"
    kansk = "kansk"


class Category(BaseModel):
    name: CategoryName  
    avg_price: float
    std_price: float

    @property
    def price(self) -> float:
        return round(float(np.random.normal(loc=self.avg_price, scale=self.std_price)), 2)


class SalesData(BaseModel):
    date: datetime
    category: Category  
    region: Region
    sales: int
    income: int


def generate_daily_by_category() -> List[SalesData]:
    data = []
    
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    categories = [
        Category(name=CategoryName.mushrooms, avg_price=500, std_price=50),
        Category(name=CategoryName.fruits, avg_price=300, std_price=30),
        Category(name=CategoryName.vegetable, avg_price=200, std_price=20),
        Category(name=CategoryName.greens, avg_price=150, std_price=15),
        Category(name=CategoryName.flowers, avg_price=800, std_price=100)
    ]
    
    regions = list(Region)
    
    current_date = start_date
    while current_date <= end_date:
        for category in categories:
            for region in regions:
                price = category.price
                
                sales = int(np.random.normal(loc=200, scale=2))
                
                income = int(price * sales)
                
                record = SalesData(
                    date=current_date,
                    category=category,
                    region=region,
                    sales=sales,
                    income=income
                )
                data.append(record)
        current_date += timedelta(days=1)
    
    return data


def save_csv(data: List[SalesData]) -> None:
    data_dicts = []
    for record in data:
        data_dicts.append({
            'date': record.date.strftime('%Y-%m-%d'),
            'category': record.category.name,  
            'region': record.region,
            'sales': record.sales,
            'income': record.income,   
        })

    df = pd.DataFrame(data_dicts)
    df.to_csv("data/dataset.csv", index=False, encoding='utf-8')


data = generate_daily_by_category()
save_csv(data)