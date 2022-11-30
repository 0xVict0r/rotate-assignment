import pandas as pd
import numpy as np
import json


def gather_flight_data():
    flight_df = pd.read_csv(r"./data/flight_events/2022-10-03.csv", sep=";")

    for i in np.arange(4, 10):
        temp = pd.read_csv(f"./data/flight_events/2022-10-0{i}.csv", sep=";")
        flight_df = pd.concat([flight_df, temp], ignore_index=True)

    return flight_df


def gather_aircraft_data():
    aircraft_df = pd.read_json(r'./data/airplane_details.json', lines=True)

    return aircraft_df


print(gather_aircraft_data())
