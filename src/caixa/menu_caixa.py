from src.comum.menus_utils import ler_opcao_int, pause
from src.caixa.operacoes_caixa import (
    carregar_clientes_json,
    carregar_produtos_csv,
    registrar_compra,
    fechar_caixa
)


def menu_principal():
    while True:
        print("\n=== SISTEMA DE CAIXA ===")
        print("1 - Carregar clientes (JSON)")
        print("2 - Carregar produtos (CSV)")
        print("3 - Registrar compra")
        print("4 - Fechar caixa")
        print("0 - Sair")

        opcao = ler_opcao_int("Escolha uma opção: ", [0, 1, 2, 3, 4])

        if opcao == 1:
            carregar_clientes_json()
            pause()

        elif opcao == 2:
            carregar_produtos_csv()
            pause()

        elif opcao == 3:
            registrar_compra()
            pause()

        elif opcao == 4:
            fechar_caixa()
            pause()

        elif opcao == 0:
            print("Saindo do sistema de caixa...")
            break
