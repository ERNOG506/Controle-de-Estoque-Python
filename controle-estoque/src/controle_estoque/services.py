import sqlite3


class EstoqueService:
    def __init__(self, conexao: sqlite3.Connection):
        self.conexao = conexao

    def cadastrar_produto(
        self,
        nome: str,
        categoria: str,
        preco: float,
        quantidade: int = 0,
        estoque_minimo: int = 5,
    ) -> int:
        self._validar_texto(nome, "Nome")
        self._validar_texto(categoria, "Categoria")

        if preco < 0:
            raise ValueError("Preco nao pode ser negativo.")
        if quantidade < 0:
            raise ValueError("Quantidade nao pode ser negativa.")
        if estoque_minimo < 0:
            raise ValueError("Estoque minimo nao pode ser negativo.")

        cursor = self.conexao.execute(
            """
            INSERT INTO produtos (nome, categoria, preco, quantidade, estoque_minimo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome.strip(), categoria.strip(), preco, quantidade, estoque_minimo),
        )
        self.conexao.commit()
        return int(cursor.lastrowid)

    def listar_produtos(self) -> list[sqlite3.Row]:
        cursor = self.conexao.execute(
            """
            SELECT id, nome, categoria, preco, quantidade, estoque_minimo
            FROM produtos
            ORDER BY nome
            """
        )
        return list(cursor.fetchall())

    def buscar_produtos(self, termo: str) -> list[sqlite3.Row]:
        termo_busca = f"%{termo.strip()}%"
        cursor = self.conexao.execute(
            """
            SELECT id, nome, categoria, preco, quantidade, estoque_minimo
            FROM produtos
            WHERE nome LIKE ? OR categoria LIKE ?
            ORDER BY nome
            """,
            (termo_busca, termo_busca),
        )
        return list(cursor.fetchall())

    def registrar_entrada(
        self,
        produto_id: int,
        quantidade: int,
        observacao: str = "",
    ) -> None:
        self._validar_produto(produto_id)
        self._validar_quantidade_movimentacao(quantidade)

        self.conexao.execute(
            "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
            (quantidade, produto_id),
        )
        self._registrar_movimentacao(produto_id, "entrada", quantidade, observacao)
        self.conexao.commit()

    def registrar_saida(
        self,
        produto_id: int,
        quantidade: int,
        observacao: str = "",
    ) -> None:
        produto = self._validar_produto(produto_id)
        self._validar_quantidade_movimentacao(quantidade)

        if produto["quantidade"] < quantidade:
            raise ValueError("Quantidade insuficiente em estoque.")

        self.conexao.execute(
            "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
            (quantidade, produto_id),
        )
        self._registrar_movimentacao(produto_id, "saida", quantidade, observacao)
        self.conexao.commit()

    def listar_estoque_baixo(self) -> list[sqlite3.Row]:
        cursor = self.conexao.execute(
            """
            SELECT id, nome, categoria, preco, quantidade, estoque_minimo
            FROM produtos
            WHERE quantidade <= estoque_minimo
            ORDER BY quantidade ASC, nome ASC
            """
        )
        return list(cursor.fetchall())

    def listar_movimentacoes(self) -> list[sqlite3.Row]:
        cursor = self.conexao.execute(
            """
            SELECT
                movimentacoes.id,
                produtos.nome AS produto,
                movimentacoes.tipo,
                movimentacoes.quantidade,
                movimentacoes.observacao,
                movimentacoes.criado_em
            FROM movimentacoes
            INNER JOIN produtos ON produtos.id = movimentacoes.produto_id
            ORDER BY movimentacoes.id DESC
            """
        )
        return list(cursor.fetchall())

    def _registrar_movimentacao(
        self,
        produto_id: int,
        tipo: str,
        quantidade: int,
        observacao: str,
    ) -> None:
        self.conexao.execute(
            """
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
            VALUES (?, ?, ?, ?)
            """,
            (produto_id, tipo, quantidade, observacao.strip()),
        )

    def _validar_produto(self, produto_id: int) -> sqlite3.Row:
        cursor = self.conexao.execute(
            """
            SELECT id, nome, categoria, preco, quantidade, estoque_minimo
            FROM produtos
            WHERE id = ?
            """,
            (produto_id,),
        )
        produto = cursor.fetchone()

        if produto is None:
            raise ValueError("Produto nao encontrado.")

        return produto

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> None:
        if not valor.strip():
            raise ValueError(f"{campo} e obrigatorio.")

    @staticmethod
    def _validar_quantidade_movimentacao(quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
