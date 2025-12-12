from src.comum.db import get_connection

def buscar_cliente_por_id(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_cliente, nome 
        FROM cliente 
        WHERE id_cliente = ?
    """, (id_cliente,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado


def buscar_cliente_por_nome(nome):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_cliente, nome 
        FROM cliente 
        WHERE nome LIKE ?
    """, (f"%{nome}%",))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_produto_por_id(id_produto):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_produto, nome, quantidade, preco
        FROM produto 
        WHERE id_produto = ?
    """, (id_produto,))

    produto = cursor.fetchone()
    conn.close()
    return produto


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
    return produtos


def atualizar_estoque(cursor, id_produto, quantidade_vendida):
    cursor.execute("""
        UPDATE produto
        SET quantidade = quantidade - ?
        WHERE id_produto = ?
    """, (quantidade_vendida, id_produto))


def listar_compras_por_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_compra, data_hora
        FROM compra
        WHERE id_cliente = ?
        ORDER BY data_hora DESC
    """, (id_cliente,))

    compras = cursor.fetchall()
    conn.close()
    return compras
