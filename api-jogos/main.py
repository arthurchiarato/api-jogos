from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import json

app = FastAPI()

# Modelo do login
class Login(BaseModel):
    email: str
    password: str

class Jogo(BaseModel):
    nome: str
    tipo: str
    nota: int
    review: str

def carregar_jogos():

    with open("jogos.json", "r", encoding="utf-8") as arquivo:

        return json.load(arquivo)

def salvar_jogos(jogos):

    with open("jogos.json", "w", encoding="utf-8") as arquivo:

        json.dump(jogos, arquivo, indent=4, ensure_ascii=False)

jogos = carregar_jogos()

# Rota inicial
@app.get("/")
def home():
    return {"mensagem": "API funcionando"}

# Login
@app.post("/login")
def login(dados: Login):

    if (
        dados.email == "usuario@esoft.com"
        and dados.password == "Abc123"
    ):

        token = str(uuid.uuid4())

        return {
            "token": token
        }

    raise HTTPException(
        status_code=401,
        detail="Email ou senha inválidos"
    )

@app.get("/jogos")
def listar_jogos():
    return jogos

@app.get("/jogos/{id}")
def buscar_jogo(id: int):

    for jogo in jogos:
        if jogo["id"] == id:
            return jogo

    raise HTTPException(
        status_code=404,
        detail="Jogo não encontrado"
    )

@app.post("/jogos", status_code=201)
def cadastrar_jogo(jogo: Jogo):

    novo_jogo = {
        "id": len(jogos) + 1,
        "nome": jogo.nome,
        "tipo": jogo.tipo,
        "nota": jogo.nota,
        "review": jogo.review
    }

    jogos.append(novo_jogo)

    salvar_jogos(jogos)

    return novo_jogo

@app.put("/jogos/{id}")
def atualizar_jogo(id: int, jogo: Jogo):

    for item in jogos:

        if item["id"] == id:

            item["nome"] = jogo.nome
            item["tipo"] = jogo.tipo
            item["nota"] = jogo.nota
            item["review"] = jogo.review

            return item

        salvar_jogos(jogos)

    raise HTTPException(
        status_code=404,
        detail="Jogo não encontrado"
    )

@app.delete("/jogos/{id}", status_code=204)
def deletar_jogo(id: int):

    for item in jogos:

        if item["id"] == id:

            jogos.remove(item)

            salvar_jogos(jogos)

            return

    raise HTTPException(
        status_code=404,
        detail="Jogo não encontrado"
    )