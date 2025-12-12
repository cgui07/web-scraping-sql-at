from src.comum.menus_utils import ler_opcao_int, pause
from src.sig.clientes_sig import menu_clientes
from src.sig.produtos_sig import menu_produtos

def menu_principal():
    while True:
        print("\nSIG - Sistema de Informações Gerenciais")
        print("1 - Clientes")
        print("2 - Produtos")
        print("0 - Sair")

        opcao = ler_opcao_int("Escolha uma opção: ", [0, 1, 2])

        if opcao == 1:
            menu_clientes()
        elif opcao == 2:
            menu_produtos()
        elif opcao == 0:
            print("Saindo do SIG...")
            break
