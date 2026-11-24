from myneo4j import driver

def create_vendedor():
    nome = input("Nome: ")
    cpf_cnpj = input("CPF/CNPJ: ")
    email = input("Email: ")
    senha = input("Senha: ")

    enderecos = []
    key = 'S'
    while key.upper() == 'S':
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {
            "rua": rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        enderecos.append(endereco)
        key = input("Outro endereço? (S/N)?").upper()

    registros, resumo, chaves = driver.execute_query(
        """
        CREATE (v:Vendedor {cpf_cnpj: $cpf_cnpj, nome: $nome, email: $email, senha: $senha})
        WITH v
        UNWIND $enderecos AS e
        CREATE (v)-[:FICA_EM]->(en:Endereco)
        SET en = e
        """,
        cpf_cnpj=cpf_cnpj, nome=nome, email=email, senha=senha, enderecos=enderecos
    )
    print("Inserido: ", cpf_cnpj)
    print("Nós criados: ", resumo.counters.nodes_created, "| Relacionamentos criados: ", resumo.counters.relationships_created)


def read_vendedor(nome=""):
    nome = nome or input("Nome (vazio para todos): ")
    registros, resumo, chaves = driver.execute_query(
        """
        MATCH (v:Vendedor)
        WHERE $nome = '' OR v.nome = $nome
        OPTIONAL MATCH (v)-[:FICA_EM]->(e:Endereco)
        RETURN v.nome AS nome, v.cpf_cnpj AS cpf_cnpj, v.email AS email, collect(e) AS enderecos
        ORDER BY nome
        """,
        nome=nome
    )
    for r in registros:
        print(r.data())