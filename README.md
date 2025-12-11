Sistema dividido em duas aplicações independentes:

Sistema de Caixa

SIG – Sistema de Informações Gerenciais
Ambos utilizam o mesmo banco de dados: mercado.db.

PRÉ-REQUISITOS

Antes de usar o projeto, instale:

pip install pandas

Se precisar recriar o banco de dados, execute:

python criar_banco.py

ESTRUTURA DO PROJETO

src/caixa → Sistema operacional de caixa
src/sig → Sistema gerencial (consultas)
src/comum → Funções compartilhadas
dados/ → Arquivos JSON, CSV e Excel
mercado.db → Banco SQLite usado pelos dois sistemas

COMO USAR O SISTEMA DE CAIXA

Para abrir o Caixa:

python src/caixa/main_caixa.py

Funções disponíveis no Caixa:

Carregar clientes (JSON)

Carregar produtos (CSV)

Registrar compra

Adicionar itens

Emitir nota fiscal

Fechar caixa (total vendido)

Fluxo recomendado:

Carregar clientes

Carregar produtos

Registrar compras

Ver fechamento do caixa

COMO USAR O SIG

Para abrir o SIG:

python src/sig/main_sig.py

FUNCIONALIDADES DO MENU "CLIENTES":

Clientes com compras

Clientes sem compras

Listar compras de um cliente

Detalhar compra (nota fiscal)

Top clientes que mais compram

Top clientes que mais gastam

FUNCIONALIDADES DO MENU "PRODUTOS":

Cadastrar produto

Listar produtos

Atualizar produto

Excluir produto

Produtos mais vendidos

Produtos menos vendidos

Produtos com pouco estoque

Ver fornecedores de um produto

Carregar fornecedores e relações via Excel

ARQUIVOS DE DADOS

Os arquivos usados pelo sistema estão em /dados:

clientes.json
produtos.csv
fornecedores_produtos.xlsx

Eles podem ser substituídos por versões atualizadas desde que mantenham o formato original.

OBSERVAÇÕES IMPORTANTES

Caixa e SIG são sistemas separados, mas compartilham o mesmo banco.

Qualquer compra registrada no Caixa aparece automaticamente nas consultas do SIG.

Menus possuem validação básica para evitar erros do usuário.