import uuid
from myneo4j import driver

def buscar_usuario_por_nome(nome):
    registros, resumo, chaves = driver.execute_query(
        "MATCH(u:Usuario {nome: $nome}) RETURN elementId(u) AS id LIMIT 1",
        nome=nome
    )
    if len(registros) == 0:
        print("Usuario nao encontrado")
        return None
    return registros[0]["id"]


def buscar_produto_por_nome(nome):
    registros, resumo, chaves = driver.execute_query(
        "MATCH(p:Produto {nome: $nome}) RETURN elementId(p) AS id, p.preco AS preco LIMIT 1",
        nome=nome
    )
    if len(registros) == 0:
        print("Produto nao encontrado")
        return None
    return registros[0]


def ler_itens():
    itens = []
    key = 'S'
    while key.upper() == 'S':
        nome_produto =input("Nome do produto: ")
        produto = buscar_produto_por_nome(nome_produto)
        if produto is None:
            continue

        quantidade = int(input("Quantidade: "))

        item = {
            "produto_id": produto["id"],
            "quantidade": quantidade,
            "preco_unitario": produto["preco"]
        }
        itens.append(item)
        key = input("Adicionar outro item (S/N)? ").upper()

    return itens


def calcular_total(itens):
    total = 0
    for item in itens:
        total += item["quantidade"] * item["preco_unitario"]
        return round(total, 2)


def create_compra():
    nome_usuario = input("Nome do usuário: ")
    usuario_id = buscar_usuario_por_nome(nome_usuario)
    if usuario_id is None:
        return

    itens = ler_itens()
    compra_id = str(uuid.uuid4())

    registros, resumo, chaves = driver.execute_query(
        """
        MATCH(u:Usuario) WHERE elementId(u) = $usuario_id
        CREATE (u)-[:FEZ]->(c:Compra {id: $compra_id, valor_total: $valor_total})
        WITH c
        UNWIND $itens AS item
        MATCH(p:Produto) WHERE elementId(p) = item.produto_id
        CREATE (c)-[:CONTEM {quantidade: item.quantidade, preco_unitario: item.preco_unitario}]->(p)
        """,
        usuario_id=usuario_id, compra_id=compra_id, valor_total=calcular_total(itens), itens=itens
    )
    print("Inserido: ", compra_id)
    print("Nós criados: ", resumo.counters.nodes_created, "| Relacionamentos criados: ", resumo.counters.relationships_created)


def read_compra(nome_usuario=""):
    nome_usuario = nome_usuario or input("Nome do usuário (vazio para todos): ")
    registros, resumo, chaves = driver.execute_query(
        """
        MATCH (u:Usuario)-[:FEZ]->(c:Compra)-[i:CONTEM]->(p:Produto)
        WHERE $nome = '' OR u.nome = $nome
        RETURN c.id AS id, u.nome AS usuario, c.valor_total AS valor_total, collect({produto: p.nome, quantidade: i.quantidade, preco_unitario: i.preco_unitario}) AS itens
        ORDER BY usuario
        """,
        nome=nome_usuario
    )
    for r in registros:
        print(r.data())