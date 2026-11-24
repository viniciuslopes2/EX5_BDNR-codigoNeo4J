from myneo4j import driver

def create_produto():
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))
    nome_vendedor = input("Nome do vendedor: ")

    registros, resumo, chaves = driver.execute_query(
        """
        MATCH(v:Vendedor {nome: $nome_vendedor})
        WITH v LIMIT 1
        CREATE (v)-[:VENDE]->(p:Produto {nome: $nome, descricao: $descricao, preco: $preco, quantidade: $quantidade})
        RETURN p.nome AS nome
        """,
        nome_vendedor=nome_vendedor, nome=nome, descricao=descricao, preco=preco, quantidade=quantidade
    )

    if len(registros) == 0:
        print("Vendedor não encontrado")
        return

    print("Inserido: ",nome)
    print("Nós criados: ", resumo.counters.nodes_created, "| Relacionamentos criados: ", resumo.counters.relationships_created)


def read_produto(nome=""):
    nome = nome or input("Nome (vazio para todos): ")
    registros, resumo, chaves = driver.execute_query(
        """
        MATCH (v:Vendedor)-[:VENDE]->(p:Produto)
        WHERE $nome = '' OR p.nome = $nome
        RETURN p.nome AS nome, p.descricao AS descricao, p.preco AS preco, p.quantidade AS quantidade, v.nome AS vendedor
        ORDER BY nome
        """,
        nome=nome
    )
    for r in registros:
        print(r.data())