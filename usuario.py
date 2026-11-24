import hashlib
from myneo4j import driver

def create_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    senha = hashlib.sha256(input("Senha: ").encode()).hexdigest()

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
        CREATE (u:Usuario {cpf: $cpf, nome: $nome, sobrenome: $sobrenome, email: $email, senha: $senha})
        WITH u
        UNWIND $enderecos AS e
        CREATE (u)-[:MORA_EM]->(en:Endereco)
        SET en = e
        """,
        cpf=cpf, nome=nome, sobrenome=sobrenome, email=email, senha=senha, enderecos=enderecos
    )
    print("Inserido: ", cpf)
    print("Nós criados: ", resumo.counters.nodes_created, "| Relacionamentos criados: ", resumo.counters.relationships_created)


def read_usuario(nome=""):
    nome = nome or input("Nome (vazio para todos): ")
    registros, resumo, chaves = driver.execute_query(
        """
        MATCH (u:Usuario)
        WHERE $nome = '' OR u.nome = $nome
        OPTIONAL MATCH (u)-[:MORA_EM]->(e:Endereco)
        RETURN u.nome AS nome, u.sobrenome AS sobrenome, u.cpf AS cpf, u.email AS email, collect(e) AS enderecos
        ORDER BY nome
        """,
        nome=nome
    )
    for r in registros:
        print(r.data())