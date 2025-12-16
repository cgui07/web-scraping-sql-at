from src.comum.menus_utils import ler_opcao_int, pause
from src.caixa.operacoes_caixa import (
    registrar_compra,
    fechar_caixa
)

def menu_principal():
    while True:
        print("SISTEMA DE CAIXA")
        print("1 - Registrar compra")
        print("2 - Fechar caixa")
        print("0 - Sair")

        opcao = ler_opcao_int("Escolha uma opção: ", [0, 1, 2, 3, 4])

        if opcao == 1:
            registrar_compra()
            pause()

        elif opcao == 2:
            fechar_caixa()
            pause()

        elif opcao == 0:
            print("Saindo do sistema de caixa...")
            break
