from src.comum.db import get_connection
from src.comum.menus_utils import ler_opcao_int, pause
from src.comum.repositorio import buscar_cliente_por_nome, buscar_cliente_por_id


def menu_clientes():
    while True:
        print("\n=== CLIENTES ===")
        print("1 - Clientes com compras")
        print("2 - Clientes sem compras")
        print("3 - Top clientes (mais compras)")
        print("4 - Top clientes (mais gastam)")
        print("0 - Voltar")

        opcao = ler_opcao_int("Escolha uma opção: ", [0,1,2,3,4])

        if opcao == 1:
            clientes_compras()
        elif opcao == 2:
            clientes_sem_compras()
        elif opcao == 3:
            top_clientes_compras()
        elif opcao == 4:
            top_clientes_gastos()
        elif opcao == 0:
            break

def clientes_compras():
    nome = input("Digite o nome (ou parte) do cliente: ")
    resultados = buscar_cliente_por_nome(nome)

    if not resultados:
        print("Nenhum cliente encontrado.")
        return

    print("\nClientes encontrados:")
    for c in resultados:
        print(f"{c[0]} - {c[1]}")

    id_cliente = int(input("\nEscolha o ID do cliente: "))
    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        print("ID inválido.")
        return

    print(f"\nConsultando compras de: {cliente[1]}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_compra, data_hora
        FROM compra
        WHERE id_cliente = ?
        ORDER BY data_hora DESC
    """, (id_cliente,))

    compras = cursor.fetchall()

    if not compras:
        print("Este cliente não possui compras.")
        return

    print("\nCompras:")
    for c in compras:
        print(f"Compra {c[0]} - {c[1]}")

    id_compra = int(input("\nEscolha o ID da compra para detalhar: "))
    detalhar_compra(id_compra)

def detalhar_compra(id_compra):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id_compra, c.data_hora, cli.nome
        FROM compra c
        JOIN cliente cli ON cli.id_cliente = c.id_cliente
        WHERE c.id_compra = ?
    """, (id_compra,))

    info = cursor.fetchone()

    if not info:
        print("Compra não encontrada.")
        return

    print(f"\n=== NOTA FISCAL ===")
    print(f"Compra ID: {info[0]}")
    print(f"Data/Hora: {info[1]}")
    print(f"Cliente: {info[2]}\n")

    cursor.execute("""
        SELECT p.nome, i.quantidade, i.preco, (i.quantidade * i.preco)
        FROM item_compra i
        JOIN produto p ON p.id_produto = i.id_produto
        WHERE i.id_compra = ?
    """, (id_compra,))

    itens = cursor.fetchall()
    total = 0

    print("Itens:")
    for nome, qtd, preco, subtotal in itens:
        print(f"{nome} - {qtd} x R$ {preco:.2f} = R$ {subtotal:.2f}")
        total += subtotal

    print(f"\nTOTAL DA COMPRA: R$ {total:.2f}")

    pause()

def clientes_sem_compras():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cli.id_cliente, cli.nome
        FROM cliente cli
        LEFT JOIN compra c ON c.id_cliente = cli.id_cliente
        WHERE c.id_compra IS NULL
        ORDER BY cli.nome
    """)

    clientes = cursor.fetchall()

    print("\nClientes que nunca compraram:")
    for c in clientes:
        print(f"{c[0]} - {c[1]}")

    pause()

def top_clientes_compras():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cli.nome, COUNT(c.id_compra) AS total
        FROM cliente cli
        JOIN compra c ON c.id_cliente = cli.id_cliente
        GROUP BY cli.id_cliente
        ORDER BY total DESC
        LIMIT 10
    """)

    ranking = cursor.fetchall()

    print("\nTop clientes – mais compras:")
    for nome, total in ranking:
        print(f"{nome}: {total} compras")

    pause()

def top_clientes_gastos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cli.nome, SUM(i.quantidade * i.preco) AS total
        FROM cliente cli
        JOIN compra c ON c.id_cliente = cli.id_cliente
        JOIN item_compra i ON i.id_compra = c.id_compra
        GROUP BY cli.nome
        ORDER BY total DESC
        LIMIT 10
    """)

    ranking = cursor.fetchall()

    print("\nTop clientes - maior valor gasto:")
    for nome, total in ranking:
        print(f"{nome}: R$ {total:.2f}")

    pause()
