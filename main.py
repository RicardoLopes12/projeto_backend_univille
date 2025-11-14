from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# Permitir que qualquer front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar pasta static se não existir
if not os.path.exists("static"):
    os.makedirs("static")

# Montar a pasta static para servir arquivos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint de clima
@app.get("/clima")
def clima():
    # Pegar localização pelo IP
    loc = requests.get("https://ipwho.is").json()
    lat = loc["latitude"]
    lon = loc["longitude"]
    cidade = loc["city"]

    # Consultar API de clima
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    resp = requests.get(url).json()
    temperatura_agora = resp["hourly"]["temperature_2m"][0]

    return {
        "cidade": cidade,
        "latitude": lat,
        "longitude": lon,
        "temperatura_agora": temperatura_agora
    }

# Servir HTML principal
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
