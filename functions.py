import pandas as pd
import numpy as np


def gather_flight_data():
    flight_df = pd.read_csv(r"./data/flight_events/2022-10-03.csv", sep=";")

    for i in np.arange(4, 10):
        temp = pd.read_csv(f"./data/flight_events/2022-10-0{i}.csv", sep=";")
        flight_df = pd.concat([flight_df, temp], ignore_index=True)

    return flight_df


def gather_aircraft_data():
    aircraft_df = pd.read_json(r'./data/airplane_details.json', lines=True)

    average_cargo_density = aircraft_df["payload"].mean(
        skipna=True) / aircraft_df["volume"].mean(skipna=True)

    for i in range(len(aircraft_df)):
        if pd.isna(aircraft_df.at[i, "volume"]):
            aircraft_df.at[i, "volume"] = aircraft_df.at[i,
                                                         "payload"] / average_cargo_density

    return aircraft_df


def make_capacity_table(flight_df, aircraft_df, save_to_csv):
    cargo_capacity_df = flight_df[["callsign", "destination_icao", "equipment", "flight", "flight_id",
                                   "operator", "origin_icao", "registration"]].drop_duplicates(subset=["flight_id"])

    cargo_capacity_df = cargo_capacity_df[cargo_capacity_df["equipment"].isin(
        aircraft_df["code_icao"])].reset_index(drop=True)

    for i in range(len(cargo_capacity_df)):
        aircraft_icao = cargo_capacity_df.at[i, "equipment"]
        cargo_capacity_df.at[i, "capacity_weight"] = aircraft_df[aircraft_df["code_icao"]
                                                                 == aircraft_icao]["payload"].values[0]
        cargo_capacity_df.at[i, "capacity_volume"] = aircraft_df[aircraft_df["code_icao"]
                                                                 == aircraft_icao]["volume"].values[0]

    if save_to_csv:
        cargo_capacity_df.to_csv(r"./data/cargo_capacity.csv")

    return cargo_capacity_df


def route_daily_capacity(origin_icao, destination_icao):

    capacity_df = pd.read_csv(r"./data/cargo_capacity.csv", index_col=0)

    route_df = capacity_df.loc[(capacity_df["origin_icao"] == origin_icao) &
                               (capacity_df["destination_icao"] == destination_icao)]

    route_daily_weight = route_df["capacity_weight"].sum() / 7
    route_daily_volume = route_df["capacity_volume"].sum() / 7

    return {"Origin Airport": origin_icao, "Destination Airport": destination_icao, "Daily Cargo Weight [kg]": route_daily_weight, "Daily Cargo Volume [m3]": route_daily_volume}


if __name__ == "main":
    route_daily_capacity("KMEM", "PHNL")
