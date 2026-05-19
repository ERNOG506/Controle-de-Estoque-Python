# Controle de Estoque

Sistema de controle de estoque desenvolvido em Python com banco de dados SQLite.
O projeto permite cadastrar produtos, registrar entradas e saidas, consultar
estoque baixo, buscar produtos e visualizar o historico de movimentacoes.

Foi criado com uma estrutura organizada para portfolio, seguindo boas praticas
simples do ecossistema Python.

## Funcionalidades

- Cadastro de produtos
- Listagem de produtos
- Busca por nome ou categoria
- Registro de entrada no estoque
- Registro de saida do estoque
- Validacao de quantidade disponivel
- Alerta de produtos com estoque baixo
- Historico de movimentacoes
- Persistencia dos dados em SQLite
- Testes automatizados

## Tecnologias

- Python 3.10+
- SQLite
- `sqlite3`
- `pathlib`
- `unittest`

## Estrutura do projeto

```txt
controle-estoque/
├── main.py
├── README.md
├── .gitignore
├── requirements.txt
├── LICENSE
├── data/
│   └── .gitkeep
├── src/
│   └── controle_estoque/
│       ├── __init__.py
│       ├── cli.py
│       ├── database.py
│       └── services.py
└── tests/
    ├── __init__.py
    └── test_estoque.py
```

## Como executar

Entre na pasta do projeto:

```powershell
cd "C:controle-estoque"
```

Execute o sistema:

```powershell
py main.py
```

## Menu do sistema

```txt
1. Cadastrar produto
2. Listar produtos
3. Buscar produtos
4. Registrar entrada
5. Registrar saida
6. Listar estoque baixo
7. Listar movimentacoes
0. Sair
```

## Banco de dados

Os dados sao salvos automaticamente em:

```txt
data/estoque.db
```

Esse arquivo e criado automaticamente quando o sistema e executado.

## Como rodar os testes

```powershell
py -m unittest discover -s tests
```

## Objetivo do projeto

Este projeto demonstra conhecimentos importantes para desenvolvimento backend:

- uso de banco de dados SQLite;
- criacao de tabelas;
- operacoes de cadastro e consulta;
- controle de entrada e saida de estoque;
- validacao de regras de negocio;
- separacao de responsabilidades;
- testes automatizados;
- organizacao de projeto Python.

## Possiveis melhorias futuras

- Interface grafica
- Exportacao de relatorios
- Dashboard com indicadores
- Login de usuarios
- API com FastAPI
- Controle de fornecedores
- Edicao e exclusao de produtos
