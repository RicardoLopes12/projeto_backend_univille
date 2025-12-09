# Projeto Back End Univille

## Sobre
Backend criado como parte do projeto universitário — implementado em Python com FastAPI. Este repositório contém o servidor, configuração para servir arquivos estáticos e integração com APIs externas (via `requests` / SDKs).


---
## Tecnologias

* Python 3.10+
* FastAPI
* Uvicorn
* python-dotenv
* requests
* openai
  

---
## Estrutura do repositório (exemplo)

```
projeto_backend_univille/
├── main.py
├── static/ # arquivos estáticos (HTML, CSS, JS)
├── .env
├── requirements.txt
├── README.md # este arquivo
└── LICENSE
```

---
## Instruções para rodar localmente

### 1. Clone o repositório:

  ```bash
git clone https://github.com/RicardoLopes12/projeto_backend_univille.git
cd projeto_backend_univille
```

### 2. Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv venv
# Linux / macOS

source venv/bin/activate

# Windows
venv\Scripts\activate

```

  

### 3. Instale as dependências (se houver `requirements.txt`):

```bash
pip install -r requirements.txt
```

  
### 4. Variáveis de ambiente
Crie um arquivo `.env` na raiz com as variáveis necessárias. Exemplo:

```
PORT=8000
OPENAI_API_KEY= chave_api
```



### 5. Rodando a aplicação

Se o ponto de entrada for `main.py` e sua app for chamada `app` (padrão FastAPI):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port ${PORT:-8000}
```

Após isso, abra `http://localhost:8000` (ou a porta configurada) no navegador.

---
## Licença
Este projeto utiliza a licença MIT. Verifique o arquivo `LICENSE` para mais detalhes.

---