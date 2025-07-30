from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root():
   response = templates.TemplateResponse("index.html", {"request": {}})
   return response

@app.get("/suporte")
async def get_root():
   response = templates.TemplateResponse("suporte.html", {"request": {}})
   return response

@app.get("/sobre")
async def get_root():
   response = templates.TemplateResponse("sobre.html", {"request": {}})
   return response

@app.get("/planos")
async def get_root():
   response = templates.TemplateResponse("planos.html", {"request": {}})
   return response

@app.get("/pagamento")
async def get_root():
   response = templates.TemplateResponse("pagamento.html", {"request": {}})
   return response

@app.get("/login")
async def get_root():
   response = templates.TemplateResponse("login.html", {"request": {}})
   return response

@app.get("/cadastro")
async def get_root():
   response = templates.TemplateResponse("cadastro.html", {"request": {}})
   return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, 
    reload=True)
