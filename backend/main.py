from fastapi import FastAPI;
from banco import conectar;

app = FastAPI();

@app.get("/")
def inicio():
  return {"message": "Hello World!"};

@app.get("/api/teste-banco")
def teste_banco():
  conexao = conectar();
  cursor = conexao.cursor();
  
  cursor.execute("SELECT COUNT(*) FROM operadoras;")
  resultado = cursor.fetchone();
  
  cursor.close();
  conexao.close();
  
  return {
    "Menssagem": "Conexão realizada com sucesso!",
    "Total de operadoras": resultado[0]
  }