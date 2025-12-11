import sqlite3

with open("script_ddl.sql", "r", encoding="utf-8") as f:
    ddl = f.read()

conn = sqlite3.connect("mercado.db")
conn.executescript(ddl)
conn.commit()
conn.close()

print("Banco criado com sucesso!")
