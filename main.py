from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv("chaveapi.env")

# --- CONFIGURAÇÃO DA IA ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------------
# 1) ENDPOINT NORMAL DE CLIMA  
# --------------------
@app.get("/clima")
def clima():
    try:
        # Pegando localização com timeout
        loc = requests.get("https://ipwho.is", timeout=3).json()

        lat = loc.get("latitude")
        lon = loc.get("longitude")
        cidade = loc.get("city")

        if lat is None or lon is None:
            return {"erro": "Não foi possível obter a localização."}

        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
        )

        resp = requests.get(url, timeout=3).json()
        temperatura = resp["hourly"]["temperature_2m"][0]

        return {
            "cidade": cidade,
            "latitude": lat,
            "longitude": lon,
            "temperatura_agora": temperatura
        }

    except Exception as e:
        return {"erro": f"Falha ao carregar clima: {str(e)}"}


# --------------------
# 2) ENDPOINT DE ANÁLISE POR IA  
# --------------------

@app.get("/clima-ia")
def clima_ia():
    try:
        loc = requests.get("https://ipwho.is", timeout=3).json()
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        cidade = loc.get("city")

        if lat is None or lon is None:
            return {"erro": "Não foi possível obter a localização."}

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weather_code"
        resp = requests.get(url, timeout=3).json()

        temperatura = resp["hourly"]["temperature_2m"][0]
        weather_code = resp["hourly"]["weather_code"][0]

        codigos = {
             0: "céu limpo",
        1: "poucas nuvens",
        2: "parcialmente nublado",
        3: "nublado",
        45: "nevoeiro",
        48: "geada",
        51: "chuva fraca",
        53: "chuva moderada",
        55: "chuva intensa",
        56: "chuva congelante fraca",
        57: "chuva congelante forte",
        61: "chuva leve",
        63: "chuva moderada",
        65: "chuva forte",
        66: "chuva congelante leve",
        67: "chuva congelante forte",
        71: "neve leve",
        73: "neve moderada",
        75: "neve forte",
        77: "granizo",
        80: "chuva de pancadas leve",
        81: "chuva de pancadas moderada",
        82: "chuva de pancadas forte",
        85: "neve de pancadas leve",
        86: "neve de pancadas forte",
        95: "tempestade leve ou moderada",
        96: "tempestade com granizo leve",
        99: "tempestade com granizo forte"
}
        descricao = codigos.get(weather_code, "condição desconhecida")

        prompt = f"""
        Relatório interestelar: {cidade} registra {temperatura}°C com clima {descricao}.
        Analise o clima como um alien completamente confuso com costumes humanos: diga se está quente, frio ou agradável, e dê uma recomendação hilária em 2 linhas.
        """

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        analise = resposta.choices[0].message.content

        return {
            "cidade": cidade,
            "temperatura": temperatura,
            "descricao_clima": descricao,
            "analise_da_ia": analise,
        }

    except Exception as e:
        return {"erro": f"Falha ao gerar análise da IA: {str(e)}"}



# --------------------
# 3) SERVIR O HTML  
# --------------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "<h1>Arquivo index.html não encontrado na pasta /static</h1>"
