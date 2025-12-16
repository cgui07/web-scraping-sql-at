import json
import pandas as pd
from datetime import datetime
from src.comum.db import get_connection
from src.comum.repositorio import buscar_cliente_por_id, buscar_produto_por_id

def ler_planilha_excel(arquivo, aba):
    df = pd.read_excel(arquivo, sheet_name=aba)
    df.columns = df.columns.str.strip().str.lower()
    return df

def carregar_fornecedores_do_excel():
    conn = get_connection()
    cursor = conn.cursor()

    df = ler_planilha_excel("dados/fornecedores.xlsx", 'fornecedores')

    contador = 0
    for _, linha in df.iterrows():
        cursor.execute(
            "INSERT OR IGNORE INTO fornecedor (id_fornecedor, nome) VALUES (?, ?)",
            (linha["id_fornecedor"], linha["nome"])
        )
        contador += 1

    conn.commit()
    conn.close()
        
    print(f"{contador} fornecedores carregados com sucesso!")

def carregar_produtos_de_fornecedores_do_excel():
    conn = get_connection()
    cursor = conn.cursor()

    df = ler_planilha_excel("dados/fornecedores.xlsx", 'produtos-fornecedores')

    contador = 0
    for _, linha in df.iterrows():
        cursor.execute(
            "INSERT OR IGNORE INTO produto_fornecedor (id_produto, id_fornecedor) VALUES (?, ?)",
            (int(linha["id_produto"]), int(linha["id_fornecedor"])),
        )
        contador += 1

    conn.commit()
    conn.close()
        
    print(f"{contador} produtos relacionados com fornecedores!")

def carregar_clientes_json():
    with open("dados/clientes.json", "r", encoding="utf-8") as f:
        clientes = json.load(f)

    conn = get_connection()
    cursor = conn.cursor()

    for cliente in clientes:
        cursor.execute(
            "INSERT OR IGNORE INTO cliente (id_cliente, nome) VALUES (?, ?)",
            (cliente["id_cliente"], cliente["nome"])
        )

    conn.commit()
    conn.close()
    print("Clientes carregados com sucesso.")


def carregar_produtos_csv():
    df = pd.read_csv("dados/produtos.csv")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT OR REPLACE INTO produto (id_produto, nome, quantidade, preco) VALUES (?, ?, ?, ?)",
            (int(row["id_produto"]), row["nome"], int(row["quantidade"]), float(row["preco"]))
        )

    conn.commit()
    conn.close()
    print("Produtos carregados com sucesso.")


def registrar_compra():
    print("\nREGISTRAR COMPRA")

    id_cliente = int(input("Informe o ID do cliente: "))
    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        print("Cliente não encontrado.")
        return

    print(f"Cliente encontrado: {cliente[1]}")

    conn = get_connection()
    cursor = conn.cursor()

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO compra (id_cliente, data_hora) VALUES (?, ?)",
        (id_cliente, data_hora)
    )

    id_compra = cursor.lastrowid
    itens = {}

    while True:
        id_produto = int(input("\nInforme o ID do produto (ou 0 para finalizar): "))
        if id_produto == 0:
            break

        produto = buscar_produto_por_id(id_produto)
        if not produto:
            print("Produto não encontrado.")
            continue

        quantidade = int(input("Quantidade: "))
        itens[id_produto] = itens.get(id_produto, 0) + quantidade

        print(f"Item adicionado: {produto[1]}")

    for id_produto, quantidade_total in itens.items():
        produto = buscar_produto_por_id(id_produto)
        preco = produto[3]

        cursor.execute(
            "INSERT INTO item_compra (id_compra, id_produto, quantidade, preco) VALUES (?, ?, ?, ?)",
            (id_compra, id_produto, quantidade_total, preco)
        )

        cursor.execute(
            "UPDATE produto SET quantidade = quantidade - ? WHERE id_produto = ?",
            (quantidade_total, id_produto)
        )

    conn.commit()
    conn.close()
    print("\nCompra finalizada com sucesso!")


def fechar_caixa():
    print("\nFECHAMENTO DE CAIXA")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(i.quantidade * i.preco)
        FROM compra c
        JOIN item_compra i ON i.id_compra = c.id_compra
    """)

    total = cursor.fetchone()[0] or 0
    print(f"Total vendido até agora: R$ {total:.2f}")

    conn.close()
