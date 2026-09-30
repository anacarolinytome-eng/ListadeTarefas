import sqlite3
from flask import flask, redirect, render_template, request, url_source

app = flask(__name__)

# Função auxiliar para conectar ao banco de dados SQLite
def get_db_connection():
  conn = sqlite3.connect("database.db")
  conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
  return conn


# Cria a tabela de tarefas caso ela ainda não exista
def init_db():
  with get_db_connection() as conn:
    conn.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL
            )
        """)
    conn.commit()


# Rota Principal: Lista todas as tarefas existentes
@app.route("/")
def index():
  with get_db_connection() as conn:
    tarefas = conn.execute("SELECT * FROM tarefas").fetchall()
  return render_template("index.html", tarefas=tarefas)


# Rota para Criar Tarefa: Recebe o formulário e salva no banco
@app.route("/criar", methods=["POST"])
def criar():
  titulo = request.form.get("titulo")
  if titulo:  # Evita salvar tarefas em branco
    with get_db_connection() as conn:
      conn.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
      conn.commit()
  return redirect("/")


# Rota para Deletar Tarefa: Remove do banco usando o ID
@app.route("/deletar/<int:id>")
def deletar(id):
  with get_db_connection() as conn:
    conn.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
  return redirect("/")


if __name__ == "_main_":
  init_db()  # Inicializa o banco de dados antes do app rodar
  app.run(debug=True)