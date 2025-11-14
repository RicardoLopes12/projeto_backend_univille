from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
from openai import OpenAI

# --- CONFIGURAÇÃO DA IA ---
client = OpenAI(api_key="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")

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


# --------------------
# 1) ENDPOINT NORMAL DE CLIMA  
# --------------------
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


# --------------------
# 2) ENDPOINT DE ANÁLISE POR IA  
# --------------------
@app.get("/clima-ia")
def clima_ia():
    # Pegar localização
    loc = requests.get("https://ipwho.is").json()
    lat = loc.get("latitude")
    lon = loc.get("longitude")
    cidade = loc.get("city")

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
    )
    resp = requests.get(url).json()

    temperatura_agora = resp["hourly"]["temperature_2m"][0]

    # IA
    prompt = f"""
    Relatório interestelar: {cidade} apresenta {temperatura_agora}°C.
Analise o clima como um alien tentando entender humanos: diga se está quente, frio ou agradável e dê uma recomendação engraçada porém em 4 linhas.

    """

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    analise = resposta.choices[0].message.content

    return {
        "cidade": cidade,
        "temperatura": temperatura_agora,
        "analise_da_ia": analise
    }

# --------------------
# 3) SERVIR O HTML  
# --------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
