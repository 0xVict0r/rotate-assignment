# Rotate Data Challenge

In order to run the API, one should run `uvicorn api:app --reload` from the terminal.

Then, navigate to `http://127.0.0.1:8000/get_daily_route_capacity/origin_icao&destination_icao` and input the origin and destination in ICAO format (eg. "KMEM" and "PHNL")

Hit enter and the API should return the daily cargo capacity both in terms of weight and volume.
