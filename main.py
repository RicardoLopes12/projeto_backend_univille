from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import Base, engine, SessionLocal
from tabela import Clima

import requests
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv("chaveapi.env") 


# --- CONFIGURAÇÃO DA IA ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Permitir qualquer front-end acessar a API
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
# 1) CLIMA NORMAL + SALVAR NO BANCO
# --------------------
@app.get("/clima")
def clima():
    try:
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

        # ✅ TEXTO PARA SALVAR NO BANCO
        texto = f"{cidade} {temperatura}°"

        # ✅ SALVAR NO BANCO
        db = SessionLocal()
        registro = Clima(descricao=texto)
        db.add(registro)
        db.commit()
        db.close()

        # ✅ RETORNAR SEPARADO PARA O FRONT
        return {
            "cidade": cidade,
            "temperatura_agora": temperatura
        }

    except Exception as e:
        return {"erro": f"Falha ao carregar clima: {str(e)}"}



# --------------------
# 2) LISTAR TODOS OS CLIMAS SALVOS
# --------------------
@app.get("/climas")
def listar_climas():
    db = SessionLocal()
    climas = db.query(Clima).all()
    db.close()
    return climas


# --------------------
# 3) CLIMA COM ANÁLISE DA IA
# --------------------
@app.get("/clima-ia")
def clima_ia():
    try:
        loc = requests.get("https://ipwho.is", timeout=3).json()
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        cidade = loc.get("city")

        if lat is None or lon is None:
            return {"analise_da_ia": "Não foi possível obter a localização."}

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
            61: "chuva leve",
            63: "chuva moderada",
            65: "chuva forte",
            71: "neve leve",
            73: "neve moderada",
            95: "tempestade"
        }

        descricao = codigos.get(weather_code, "clima desconhecido")

        prompt = f"""
        Na cidade de {cidade}, a temperatura atual é {temperatura}°C com {descricao}.
        Analise de forma divertida como se fosse um alien confuso em 3 linhas
        """

        resposta = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
)

        analise = resposta.output_text


        return {
            "analise_da_ia": analise
        }

    except Exception as e:
        return {
            "analise_da_ia": f"Erro ao gerar análise: {str(e)}"
        }

# --------------------
# 4) SERVIR O FRONT-END
# --------------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "<h1>Arquivo index.html não encontrado na pasta /static</h1>"
