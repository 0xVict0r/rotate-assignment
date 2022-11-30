from fastapi import FastAPI
from functions import *

app = FastAPI()

# Home endpoint
@app.get('/')
def home():
    return {"Data": "Use /get_daily_route_capacity/origin_icao&destination_icao"}

# Main route endpoint (run using "uvicorn api:app --reload")
@app.get('/get_daily_route_capacity/{origin_icao}&{destination_icao}')
def daily_cargo(origin_icao: str, destination_icao: str):
    return route_daily_capacity(origin_icao, destination_icao)
