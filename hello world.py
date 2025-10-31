# main.py
from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir que qualquer front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/clima")
def clima():
    
    loc = requests.get("https://ipwho.is").json()
    lat = loc["latitude"]
    lon = loc["longitude"]
    cidade = loc["city"]

  
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    resp = requests.get(url).json()
    temperatura_agora = resp["hourly"]["temperature_2m"][0]

    return {
        "cidade": cidade,
        "latitude": lat,
        "longitude": lon,
        "temperatura_agora": temperatura_agora
    }
