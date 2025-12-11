DROP TABLE IF EXISTS item_compra;
DROP TABLE IF EXISTS compra;
DROP TABLE IF EXISTS produto_fornecedor;
DROP TABLE IF EXISTS fornecedor;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS cliente;

CREATE TABLE cliente (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE produto (
    id_produto INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
);

CREATE TABLE fornecedor (
    id_fornecedor INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

CREATE TABLE produto_fornecedor (
    id_produto INTEGER,
    id_fornecedor INTEGER,
    PRIMARY KEY (id_produto, id_fornecedor),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor)
);

CREATE TABLE compra (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    data_hora TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE item_compra (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_compra INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);
