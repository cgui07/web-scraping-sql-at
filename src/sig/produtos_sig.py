import pandas as pd
from src.comum.db import get_connection
from src.comum.menus_utils import ler_opcao_int, pause

def menu_produtos():
    while True:
        print("\nPRODUTOS")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Excluir produto")
        print("5 - Produtos mais vendidos")
        print("6 - Produtos menos vendidos")
        print("7 - Produtos com pouco estoque")
        print("8 - Ver fornecedores de um produto")        
        print("9 - Carregar fornecedores do Excel")
        print("0 - Voltar")

        opcao = ler_opcao_int("Escolha uma opção: ", list(range(10)))

        if opcao == 1:
            cadastrar_produto()
        elif opcao == 2:
            listar_produtos()
        elif opcao == 3:
            atualizar_produto()
        elif opcao == 4:
            excluir_produto()
        elif opcao == 5:
            produtos_mais_vendidos()
        elif opcao == 6:
            produtos_menos_vendidos()
        elif opcao == 7:
            produtos_pouco_estoque()
        elif opcao == 8:
            fornecedores_produto()
        elif opcao == 9:
            carregar_fornecedores_excel()
        elif opcao == 0:
            break

def cadastrar_produto():
    nome = input("Nome do produto: ")
    quantidade = int(input("Quantidade em estoque: "))
    preco = float(input("Preço: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produto (nome, quantidade, preco)
        VALUES (?, ?, ?)
    """, (nome, quantidade, preco))

    conn.commit()
    conn.close()

    print("Produto cadastrado com sucesso!")
    pause()


def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_produto, nome, quantidade, preco
        FROM produto
        ORDER BY nome
    """)

    produtos = cursor.fetchall()
    conn.close()

    print("\nProdutos cadastrados:")
    for p in produtos:
        print(f"{p[0]} - {p[1]} | Estoque: {p[2]} | R$ {p[3]:.2f}")

    pause()


def atualizar_produto():
    id_produto = int(input("ID do produto: "))

    nome = input("Novo nome: ")
    quantidade = int(input("Nova quantidade: "))
    preco = float(input("Novo preço: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE produto
        SET nome = ?, quantidade = ?, preco = ?
        WHERE id_produto = ?
    """, (nome, quantidade, preco, id_produto))

    conn.commit()
    conn.close()

    print("Produto atualizado.")
    pause()


def excluir_produto():
    id_produto = int(input("ID do produto: "))

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM produto_fornecedor WHERE id_produto = ?", (id_produto,))
        cursor.execute("DELETE FROM produto WHERE id_produto = ?", (id_produto,))
        conn.commit()
        print("Produto excluído.")
    except:
        print("Erro: produto já possui vendas registradas.")
    finally:
        conn.close()

    pause()

def produtos_mais_vendidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nome, SUM(i.quantidade) AS total
        FROM produto p
        JOIN item_compra i ON p.id_produto = i.id_produto
        GROUP BY p.id_produto
        ORDER BY total DESC
    """)

    produtos = cursor.fetchall()
    conn.close()

    print("\nProdutos mais vendidos:")
    for nome, total in produtos:
        print(f"{nome}: {total} unidades")

    pause()

def produtos_menos_vendidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nome, SUM(i.quantidade) AS total
        FROM produto p
        LEFT JOIN item_compra i ON p.id_produto = i.id_produto
        GROUP BY p.id_produto
        ORDER BY total ASC
    """)

    produtos = cursor.fetchall()
    conn.close()

    print("\nProdutos menos vendidos:")
    for nome, total in produtos:
        print(f"{nome}: {total} unidades")

    pause()

def produtos_pouco_estoque():
    limite = int(input("Exibir produtos com estoque ≤: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_produto, nome, quantidade
        FROM produto
        WHERE quantidade <= ?
    """, (limite,))

    produtos = cursor.fetchall()
    conn.close()

    print("\nProdutos com pouco estoque:")
    for p in produtos:
        print(f"{p[0]} - {p[1]} | Estoque: {p[2]}")

    pause()


def fornecedores_produto():
    id_produto = int(input("ID do produto: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.nome
        FROM fornecedor f
        JOIN produto_fornecedor pf ON pf.id_fornecedor = f.id_fornecedor
        WHERE pf.id_produto = ?
    """, (id_produto,))

    fornecedores = cursor.fetchall()
    conn.close()

    print("\nFornecedores do produto:")
    for f in fornecedores:
        print(f"- {f[0]}")

    pause()

def carregar_fornecedores_excel():
    df_fornecedores = pd.read_excel("dados/fornecedores_produtos.xlsx", sheet_name="fornecedores")
    df_relacao = pd.read_excel("dados/fornecedores_produtos.xlsx", sheet_name="produtos-fornecedores")

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df_fornecedores.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO fornecedor (id_fornecedor, nome)
            VALUES (?, ?)
        """, (row["id_fornecedor"], row["nome"]))

    for _, row in df_relacao.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO produto_fornecedor (id_produto, id_fornecedor)
            VALUES (?, ?)
        """, (row["id_produto"], row["id_fornecedor"]))

    conn.commit()
    conn.close()

    print("Fornecedores e relações carregados com sucesso!")
    pause()
