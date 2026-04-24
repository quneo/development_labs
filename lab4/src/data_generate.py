from datetime import datetime, timedelta
from typing import List
from dataclasses import dataclass
from enum import Enum
import random
import csv


class StationName(str, Enum):
    central = "Центральная"
    east = "Восточная"
    west = "Западная"
    north = "Северная"
    south = "Южная"
    university = "Университет"
    park = "Парк"
    river = "Речная"


@dataclass
class Station:
    name: StationName
    base_passengers: int
    morning_factor: float
    evening_factor: float


@dataclass
class PassengerFlow:
    date: datetime
    station: StationName
    hour: int
    passengers: int


def get_hour_factor(hour: int, station: Station) -> float:
    if 7 <= hour <= 10:
        return station.morning_factor

    if 17 <= hour <= 20:
        return station.evening_factor

    if 11 <= hour <= 16:
        return 0.75

    if 21 <= hour <= 23:
        return 0.45

    return 0.18


def get_day_factor(date: datetime) -> float:
    if date.weekday() >= 5:
        return 0.7

    return 1.0


def generate_passenger_flow() -> List[PassengerFlow]:
    random.seed(42)

    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)

    stations = [
        Station(name=StationName.central, base_passengers=1450, morning_factor=1.7, evening_factor=1.8),
        Station(name=StationName.east, base_passengers=900, morning_factor=1.5, evening_factor=1.3),
        Station(name=StationName.west, base_passengers=760, morning_factor=1.35, evening_factor=1.45),
        Station(name=StationName.north, base_passengers=820, morning_factor=1.4, evening_factor=1.35),
        Station(name=StationName.south, base_passengers=700, morning_factor=1.3, evening_factor=1.25),
        Station(name=StationName.university, base_passengers=1100, morning_factor=1.6, evening_factor=1.2),
        Station(name=StationName.park, base_passengers=650, morning_factor=1.1, evening_factor=1.4),
        Station(name=StationName.river, base_passengers=580, morning_factor=1.2, evening_factor=1.25),
    ]

    current_date = start_date
    while current_date <= end_date:
        for station in stations:
            for hour in range(24):
                hour_factor = get_hour_factor(hour, station)
                day_factor = get_day_factor(current_date)
                noise = random.gauss(mu=1.0, sigma=0.08)

                passengers = int(station.base_passengers * hour_factor * day_factor * noise)
                passengers = max(passengers, 20)

                data.append(PassengerFlow(
                    date=current_date,
                    station=station.name,
                    hour=hour,
                    passengers=passengers
                ))

        current_date += timedelta(days=1)

    return data


def save_csv(data: List[PassengerFlow]) -> None:
    with open("data/passenger_flow.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "station", "hour", "passengers"])

        for record in data:
            writer.writerow([
                record.date.strftime("%Y-%m-%d"),
                record.station.value,
                record.hour,
                record.passengers,
            ])


if __name__ == "__main__":
    passenger_flow = generate_passenger_flow()
    save_csv(passenger_flow)
