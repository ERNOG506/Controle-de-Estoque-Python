import sqlite3
from pathlib import Path


def conectar(caminho_banco: str | Path) -> sqlite3.Connection:
    caminho = Path(caminho_banco)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    criar_tabelas(conexao)
    return conexao


def criar_tabelas(conexao: sqlite3.Connection) -> None:
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL CHECK (preco >= 0),
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK (estoque_minimo >= 0),
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
            quantidade INTEGER NOT NULL CHECK (quantidade > 0),
            observacao TEXT,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
        """
    )
    conexao.commit()
