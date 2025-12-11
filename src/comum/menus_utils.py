def ler_opcao_int(msg, opcoes_validas):
    while True:
        try:
            opcao = int(input(msg))

            if opcao in opcoes_validas:
                return opcao
            else:
                print(f"Opção inválida. Escolha uma das opções: {opcoes_validas}")

        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def pause():
    input("\nPressione ENTER para continuar...")
