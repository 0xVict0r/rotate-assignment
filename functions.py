import pandas as pd
import numpy as np


def gather_flight_data():

    # Read the first csv file and make a pd dataframe
    flight_df = pd.read_csv(r"./data/flight_events/2022-10-03.csv", sep=";")

    # Loop through the other ones and append them to the initial one
    for i in np.arange(4, 10):
        temp = pd.read_csv(f"./data/flight_events/2022-10-0{i}.csv", sep=";")
        flight_df = pd.concat([flight_df, temp], ignore_index=True)

    return flight_df


def gather_aircraft_data():

    # Read the json file and make a pd dataframe
    aircraft_df = pd.read_json(r'./data/airplane_details.json', lines=True)

    # Calculate the average cargo density to populate the missing values
    average_cargo_density = aircraft_df["payload"].mean(
        skipna=True) / aircraft_df["volume"].mean(skipna=True)

    # Loop through the df and add volume where it is missing
    for i in range(len(aircraft_df)):
        if pd.isna(aircraft_df.at[i, "volume"]):
            aircraft_df.at[i, "volume"] = aircraft_df.at[i,
                                                         "payload"] / average_cargo_density

    return aircraft_df


def make_capacity_table(flight_df, aircraft_df, save_to_csv):

    # Create the cargo capacity df from the existing flight df (only keep one event per flight)
    cargo_capacity_df = flight_df[["callsign", "destination_icao", "equipment", "flight", "flight_id",
                                   "operator", "origin_icao", "registration"]].drop_duplicates(subset=["flight_id"])

    # print(cargo_capacity_df[~cargo_capacity_df["equipment"].isin(
    #     aircraft_df["code_icao"])]["equipment"].value_counts().head(20))

    # Remove all the flights where the aircraft is not in aircraft_df (a majority of helicopters, GA and jets which are generally useless for cargo)
    cargo_capacity_df = cargo_capacity_df[cargo_capacity_df["equipment"].isin(
        aircraft_df["code_icao"])].reset_index(drop=True)

    # Loop through the df to add capacity weight and volume to each flight, by checking the aircraft type
    for i in range(len(cargo_capacity_df)):
        aircraft_icao = cargo_capacity_df.at[i, "equipment"]
        cargo_capacity_df.at[i, "capacity_weight"] = aircraft_df[aircraft_df["code_icao"]
                                                                 == aircraft_icao]["payload"].values[0]
        cargo_capacity_df.at[i, "capacity_volume"] = aircraft_df[aircraft_df["code_icao"]
                                                                 == aircraft_icao]["volume"].values[0]

    # If true, save the data to a new csv, useful to save the data and use it instead of running this everytime
    if save_to_csv:
        cargo_capacity_df.to_csv(r"./data/cargo_capacity.csv")

    return cargo_capacity_df


def route_daily_capacity(origin_icao, destination_icao):

    # Read the capacity df (the one saved using the funtion above)
    capacity_df = pd.read_csv(r"./data/cargo_capacity.csv", index_col=0)

    # Filter the df by the origin and destination airports
    route_df = capacity_df.loc[(capacity_df["origin_icao"] == origin_icao) &
                               (capacity_df["destination_icao"] == destination_icao)]

    # Calculate the average daily weight and volume on that route (/7 because the initial data is an aggregate of 7 days of flights)
    route_daily_weight = route_df["capacity_weight"].sum() / 7
    route_daily_volume = route_df["capacity_volume"].sum() / 7
    daily_flights = len(route_df["capacity_volume"]) / 7

    return {"Origin Airport": origin_icao, "Destination Airport": destination_icao, "Daily Capacity Weight [kg]": route_daily_weight, "Daily Capacity Volume [m3]": route_daily_volume, "Daily Flights": daily_flights}


if __name__ == "__main__":
    result = make_capacity_table(
        gather_flight_data(), gather_aircraft_data(), True)
