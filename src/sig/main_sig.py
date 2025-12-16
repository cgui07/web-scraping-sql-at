import sqlite3
from src.caixa.operacoes_caixa import carregar_clientes_json, carregar_fornecedores_do_excel, carregar_produtos_csv, carregar_produtos_de_fornecedores_do_excel
from src.sig.menu_sig import menu_principal

def criar_banco_se_necessario():
    conn = sqlite3.connect("mercado.db") 
    cursor = conn.cursor()

    # cursor.execute("""
    #     DELETE FROM fornecedor
    # """)

    cursor.execute("""
        SELECT 1
        FROM fornecedor
    """)

    fornecedor = cursor.fetchall()

    if len(fornecedor) == 0: 
        print("Criando banco de dados...")
        with open("script_ddl.sql", "r", encoding="utf-8") as f:
            ddl = f.read()  
        conn.executescript(ddl)
        conn.commit()
        conn.close()
        
        print("Carregando clientes...")
        carregar_clientes_json()
        print("Carregando produtos...")
        carregar_produtos_csv()
        print("Carregando fornecedores...")
        carregar_fornecedores_do_excel()
        print("Relacionado produtos aos fornecedores...")
        carregar_produtos_de_fornecedores_do_excel()

        print("Banco de dados criado com sucesso!")

def main():
    criar_banco_se_necessario()
    menu_principal()

if __name__ == "__main__":
    main()
