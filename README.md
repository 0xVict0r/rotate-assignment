# Rotate Data Challenge

To use this app, one can either go to this [website](https://0xvict0r-rotate-assignment-rotate-data-challenge-2h6uhy.streamlit.app/) and follow instructions, or use the integrated API as explained below.

In order to run the API, one should run `uvicorn api:app --reload` from the terminal.

Then, navigate to `http://127.0.0.1:8000/get_daily_route_capacity/origin_icao&destination_icao` and input the origin and destination in ICAO format (eg. "KMEM" and "PHNL")

Hit enter and the API should return the daily cargo capacity both in terms of weight and volume.

For missing data : 
- Computed the average density of cargo space (mass/volume) and populated the missing volumes by using this density
- For aircrafts missing in the airplane_details, I looked at the ones that are used the most that are not helicopters, GA or private jets (which end up being embraers and ATR) and I manually added them to the airplane_details json file