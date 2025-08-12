from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from passlib.context import CryptContext
from data.models.usuario_model import Usuario
from data.repo.usuario_repo import inserir_usuario, obter_todos_usuarios

# Inicialização da aplicação FastAPI
app = FastAPI()

# Monta o diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configura o motor de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------------------------------
# ROTAS PARA SERVIR PÁGINAS HTML (GET)
# ----------------------------------------------------

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


@app.get("/usuarios_pagina", response_class=HTMLResponse)
async def get_usuarios_pagina(request: Request):
    usuarios = obter_todos_usuarios()
    return templates.TemplateResponse(
        "lista_usuarios.html", 
        {"request": request, "usuarios": usuarios}
    )


# ----------------------------------------------------
# ROTA PARA LISTAR TODOS OS USUÁRIOS (GET /usuarios)
# ----------------------------------------------------

@app.get("/usuarios")
async def get_usuarios():
    """
    Retorna uma lista de todos os usuários cadastrados no banco de dados.
    Esta é a rota que você usará para ver se o cadastro funcionou.
    """
    usuarios = obter_todos_usuarios()
    return {"usuarios": usuarios}

# ----------------------------------------------------
# ROTA DE PROCESSAMENTO DO FORMULÁRIO (POST /cadastro)
# ----------------------------------------------------

@app.post("/cadastro")
async def post_cadastro(
    tipoConta: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmarSenha: str = Form(...),
    nomeCliente: str = Form(None),
    cpfCliente: str = Form(None),
    nomeProfissional: str = Form(None),
    cpfProfissional: str = Form(None),
    dataNascimentoProfissional: str = Form(None),
    tipoProfissional: str = Form(None),
    numeroRegistro: str = Form(None),
    diplomaFoto: UploadFile = File(None)
):
    # Validação básica
    if senha != confirmarSenha:
        raise HTTPException(status_code=400, detail="Senhas não conferem")

    if tipoConta == "cliente":
        nome = nomeCliente
        data_nascimento = "" 
        tipo_usuario = "cliente"
    elif tipoConta == "profissional":
        nome = nomeProfissional
        data_nascimento = dataNascimentoProfissional or ""
        tipo_usuario = tipoProfissional
    else:
        raise HTTPException(status_code=400, detail="Tipo de conta inválido")

    senha_hash = pwd_context.hash(senha)

    usuario = Usuario(
        id=0,
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        data_nascimento=data_nascimento,
        sexo="",
        tipo_usuario=tipo_usuario
    )
    
    # Chama a função para inserir o usuário no banco de dados
    id_usuario = inserir_usuario(usuario)
    
    if id_usuario is None:
        raise HTTPException(status_code=500, detail="Erro ao salvar usuário")

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

# ----------------------------------------------------
# EXECUÇÃO DA APLICAÇÃO
# ----------------------------------------------------

if __name__ == "__main__":
    # Inicia o servidor Uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)