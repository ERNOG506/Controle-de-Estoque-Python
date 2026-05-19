import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from controle_estoque.database import conectar
from controle_estoque.services import EstoqueService


class EstoqueServiceTestCase(unittest.TestCase):
    def criar_service(self):
        pasta_temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(pasta_temporaria.cleanup)

        caminho_banco = Path(pasta_temporaria.name) / "estoque.db"
        conexao = conectar(caminho_banco)
        self.addCleanup(conexao.close)
        return EstoqueService(conexao)

    def test_cadastra_produto(self):
        service = self.criar_service()

        produto_id = service.cadastrar_produto(
            nome="Mouse Gamer",
            categoria="Perifericos",
            preco=129.90,
            quantidade=10,
            estoque_minimo=3,
        )

        produtos = service.listar_produtos()

        self.assertEqual(produto_id, 1)
        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0]["nome"], "Mouse Gamer")

    def test_registra_entrada_e_saida(self):
        service = self.criar_service()
        produto_id = service.cadastrar_produto("Teclado", "Perifericos", 199.90, 5, 2)

        service.registrar_entrada(produto_id, 3, "Compra de reposicao")
        service.registrar_saida(produto_id, 4, "Venda")

        produto = service.listar_produtos()[0]
        movimentacoes = service.listar_movimentacoes()

        self.assertEqual(produto["quantidade"], 4)
        self.assertEqual(len(movimentacoes), 2)

    def test_bloqueia_saida_sem_estoque(self):
        service = self.criar_service()
        produto_id = service.cadastrar_produto("Monitor", "Eletronicos", 899.90, 2, 1)

        with self.assertRaises(ValueError):
            service.registrar_saida(produto_id, 3)

    def test_lista_estoque_baixo(self):
        service = self.criar_service()
        service.cadastrar_produto("Cabo HDMI", "Acessorios", 29.90, 2, 5)
        service.cadastrar_produto("Notebook", "Eletronicos", 3500.00, 10, 2)

        produtos = service.listar_estoque_baixo()

        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0]["nome"], "Cabo HDMI")

    def test_busca_produto_por_categoria(self):
        service = self.criar_service()
        service.cadastrar_produto("Headset", "Audio", 159.90, 6, 2)

        produtos = service.buscar_produtos("audio")

        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0]["nome"], "Headset")


if __name__ == "__main__":
    unittest.main()
