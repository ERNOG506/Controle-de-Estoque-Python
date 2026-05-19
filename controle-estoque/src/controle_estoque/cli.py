from pathlib import Path

from controle_estoque.database import conectar
from controle_estoque.services import EstoqueService


ROOT_DIR = Path(__file__).resolve().parents[2]
DATABASE_FILE = ROOT_DIR / "data" / "estoque.db"


def main() -> None:
    with conectar(DATABASE_FILE) as conexao:
        service = EstoqueService(conexao)

        while True:
            mostrar_menu()
            opcao = input("Escolha uma opcao: ").strip()

            try:
                if opcao == "1":
                    cadastrar_produto(service)
                elif opcao == "2":
                    listar_produtos(service)
                elif opcao == "3":
                    buscar_produtos(service)
                elif opcao == "4":
                    registrar_entrada(service)
                elif opcao == "5":
                    registrar_saida(service)
                elif opcao == "6":
                    listar_estoque_baixo(service)
                elif opcao == "7":
                    listar_movimentacoes(service)
                elif opcao == "0":
                    print("Sistema encerrado. Ate logo!")
                    break
                else:
                    print("Opcao invalida. Tente novamente.")
            except ValueError as erro:
                print(f"Erro: {erro}")


def mostrar_menu() -> None:
    print("\n===== Controle de Estoque =====")
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Buscar produtos")
    print("4. Registrar entrada")
    print("5. Registrar saida")
    print("6. Listar estoque baixo")
    print("7. Listar movimentacoes")
    print("0. Sair")


def cadastrar_produto(service: EstoqueService) -> None:
    nome = input("Nome do produto: ")
    categoria = input("Categoria: ")
    preco = ler_float("Preco: ")
    quantidade = ler_int("Quantidade inicial: ")
    estoque_minimo = ler_int("Estoque minimo: ")

    produto_id = service.cadastrar_produto(
        nome=nome,
        categoria=categoria,
        preco=preco,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
    )
    print(f"Produto cadastrado com sucesso! ID: {produto_id}")


def listar_produtos(service: EstoqueService) -> None:
    produtos = service.listar_produtos()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\nProdutos cadastrados:")
    for produto in produtos:
        mostrar_produto(produto)


def buscar_produtos(service: EstoqueService) -> None:
    termo = input("Digite parte do nome ou categoria: ").strip()

    if not termo:
        print("Digite um termo para buscar.")
        return

    produtos = service.buscar_produtos(termo)

    if not produtos:
        print("Nenhum produto encontrado.")
        return

    print("\nProdutos encontrados:")
    for produto in produtos:
        mostrar_produto(produto)


def registrar_entrada(service: EstoqueService) -> None:
    produto_id = ler_int("ID do produto: ")
    quantidade = ler_int("Quantidade de entrada: ")
    observacao = input("Observacao (opcional): ")

    service.registrar_entrada(produto_id, quantidade, observacao)
    print("Entrada registrada com sucesso!")


def registrar_saida(service: EstoqueService) -> None:
    produto_id = ler_int("ID do produto: ")
    quantidade = ler_int("Quantidade de saida: ")
    observacao = input("Observacao (opcional): ")

    service.registrar_saida(produto_id, quantidade, observacao)
    print("Saida registrada com sucesso!")


def listar_estoque_baixo(service: EstoqueService) -> None:
    produtos = service.listar_estoque_baixo()

    if not produtos:
        print("Nenhum produto com estoque baixo.")
        return

    print("\nProdutos com estoque baixo:")
    for produto in produtos:
        mostrar_produto(produto)


def listar_movimentacoes(service: EstoqueService) -> None:
    movimentacoes = service.listar_movimentacoes()

    if not movimentacoes:
        print("Nenhuma movimentacao registrada.")
        return

    print("\nHistorico de movimentacoes:")
    for item in movimentacoes:
        observacao = item["observacao"] or "Sem observacao"
        print(
            f"{item['id']} - {item['produto']} | {item['tipo']} | "
            f"{item['quantidade']} un. | {observacao} | {item['criado_em']}"
        )


def mostrar_produto(produto) -> None:
    print(
        f"{produto['id']} - {produto['nome']} | {produto['categoria']} | "
        f"R$ {produto['preco']:.2f} | Qtd: {produto['quantidade']} | "
        f"Min: {produto['estoque_minimo']}"
    )


def ler_int(mensagem: str) -> int:
    valor = input(mensagem).strip()

    if not valor.isdigit():
        raise ValueError("Digite um numero inteiro valido.")

    return int(valor)


def ler_float(mensagem: str) -> float:
    valor = input(mensagem).strip().replace(",", ".")

    try:
        return float(valor)
    except ValueError as erro:
        raise ValueError("Digite um valor numerico valido.") from erro
