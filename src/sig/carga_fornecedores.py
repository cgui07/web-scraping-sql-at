import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("mercado.db")

EXCEL_PATH = Path("dados/fornecedores_produtos.xlsx")

def carregar_fornecedores():
    conn = sqlite3.connect(DB_PATH)

    df_fornecedores = pd.read_excel(
        EXCEL_PATH,
        sheet_name="fornecedores"
    )

    df_fornecedores.to_sql(
        "fornecedor",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()
    print("Fornecedores carregados com sucesso.")

def carregar_produtos_fornecedores():
    conn = sqlite3.connect(DB_PATH)

    df_relacao = pd.read_excel(
        EXCEL_PATH,
        sheet_name="produtos-fornecedores"
    )

    df_relacao.to_sql(
        "produto_fornecedor",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()
    print("Relação produto-fornecedor carregada com sucesso.")

if __name__ == "__main__":
    carregar_fornecedores()
    carregar_produtos_fornecedores()
