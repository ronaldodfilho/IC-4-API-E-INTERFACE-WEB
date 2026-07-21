from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from banco import conectar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
  
@app.get("/api/operadoras")
def listar_operadoras(page: int = Query(default=1, ge=1), limit: int = Query(default=10, ge=1, le = 100), busca: str = ""):
    offset = (page - 1) * limit
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    termo_busca = f"%{busca}%"
    
    cursor.execute("SELECT * FROM operadoras WHERE razao_social LIKE %s OR cnpj LIKE %s ORDER BY razao_social LIMIT %s OFFSET %s", (termo_busca, termo_busca, limit, offset))
    operadoras = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) AS total FROM operadoras WHERE razao_social LIKE %s OR cnpj LIKE %s", (termo_busca, termo_busca))
    resultado = cursor.fetchone()
  
    cursor.close()
    conexao.close()
  
    return {
      "data": operadoras,
      "total" : resultado["total"],
      "page": page,
      "limit": limit,
    }
    
@app.get("/api/operadoras/{cnpj}")
def buscar_operadora(cnpj : str):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM operadoras WHERE cnpj = %s", (cnpj,))
    operadora = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    if operadora is None:
      raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    return {
      "data": operadora
    }
    
@app.get("/api/operadoras/{cnpj}/despesas")
def buscar_despesas_operadora(cnpj: str):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("""
                  SELECT o.cnpj, o.razao_social, dc.ano, dc.trimestre, dc.valor_despesas FROM despesas_consolidadas AS dc
                  JOIN operadoras o 
                  ON o.id = dc.operadora_id
                  WHERE o.cnpj = %s
                  ORDER BY dc.ano DESC, dc.trimestre DESC
                  """, (cnpj,))
    
    despesas = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    if not despesas:
        raise HTTPException(status_code=404, detail="Despesas não encontradas para a operadora")
      
    return {
        "data": despesas
      }
    
@app.get("/api/estatisticas")
def estatisticas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("""
                   SELECT SUM(valor_despesas) AS total_despesas,
                   AVG(valor_despesas) AS media_despesas
                   FROM despesas_consolidadas;     
                   """)
    
    estatisticas = cursor.fetchone()
    
    cursor.execute("""
                   SELECT o.cnpj, o.razao_social,SUM(dc.valor_despesas) AS total_despesas
                    FROM despesas_consolidadas AS dc
                    JOIN operadoras AS o
                      ON o.id = dc.operadora_id
                    GROUP BY o.cnpj, o.id, o.razao_social
                    ORDER BY total_despesas DESC
                    LIMIT 5;
                   """)
    
    top_operadoras = cursor.fetchall()
    
    cursor.execute("""SELECT 
                      o.uf,
                      ROUND(SUM(da.total_despesas), 2) AS total_despesas_uf,
                      ROUND(AVG(da.total_despesas), 2) AS media_despesas_por_operadora
                      FROM despesas_agregadas AS da
                      JOIN operadoras AS o
                        ON o.id = da.operadora_id
                      GROUP BY o.uf
                      ORDER BY total_despesas_uf DESC;""")
    
    distribuicao_uf = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return {
        "total_despesas": estatisticas["total_despesas"],
        "media_despesas": estatisticas["media_despesas"],
        "top_operadoras": top_operadoras,
        "distribuicao_uf": distribuicao_uf
    }