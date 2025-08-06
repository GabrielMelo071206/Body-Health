from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/suporte", response_class=HTMLResponse)
async def get_suporte(request: Request):
    return templates.TemplateResponse("suporte.html", {"request": request})

@app.get("/sobre", response_class=HTMLResponse)
async def get_sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})

@app.get("/planos", response_class=HTMLResponse)
async def get_planos(request: Request):
    return templates.TemplateResponse("planos.html", {"request": request})

@app.get("/pagamento", response_class=HTMLResponse)
async def get_pagamento(request: Request):
    return templates.TemplateResponse("pagamento.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def get_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
