# Rotate Data Challenge

## Tutorial

To use this app, one can either go to this [website](https://0xvict0r-rotate-assignment-rotate-data-challenge-2h6uhy.streamlit.app/) and follow instructions, or use the integrated API as explained below.

In order to run the API, one should run `uvicorn api:app --reload` from the terminal.

Then, navigate to `http://127.0.0.1:8000/get_daily_route_capacity/origin_icao&destination_icao` and input the origin and destination in ICAO format (eg. "KMEM" and "PHNL")

Hit enter and the API should return the daily cargo capacity both in terms of weight and volume.

## Extra information

For missing data : 
- Computed the average density of cargo space (mass/volume) and populated the missing volumes by using this density
- For aircrafts missing in the airplane_details, I looked at the ones that are used the most that are not helicopters, GA or private jets (which end up being Embraer, CRJ and ATR) and I manually added them to the airplane_details json file

All methods are in the `functions.py`, API endpoints are found in `api.py` and the Streamlit app is located in `Rotate_Data_Challenge.py`.

**Question 1 :** I made 2 methods to access both datasets (json & csv). They both convert the data into pandas DataFrames that can be used in question 2.

**Question 2 :** The capacity table is created from the method `make_capacity_table` that takes the DataFrames from Q1. It returns the capacity table in the format of a pandas DataFramme which can also be saved as a csv file for repetitive use (could be made into a SQL database too, but for simplicity reasons, it was made a csv file here).

**Question 3 :** An API endpoint was made, alongside a simple GUI, for which the tutorial is given above.