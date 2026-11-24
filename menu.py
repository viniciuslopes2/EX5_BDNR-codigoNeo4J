import usuario
import vendedor
import produto
import compra
from myneo4j import driver

def menu_usuario():
    sub = 0
    while sub != 'V':
        print("1-Inserir usuário")
        print("2-Consultar usuário")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            usuario.create_usuario()
        elif sub == '2':
            usuario.read_usuario()


def menu_vendedor():
    sub = 0
    while sub != 'V':
        print("1-Inserir vendedor")
        print("2-Consultar vendedor")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            vendedor.create_vendedor()
        elif sub == '2':
            vendedor.read_vendedor()

def menu_produto():
    sub = 0
    while sub != 'V':
        print("1-Inserir produto")
        print("2-Consultar produto")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            produto.create_produto()
        elif sub == '2':
            produto.read_produto()

def menu_compra():
    sub = 0
    while sub != 'V':
        print("1-Inserir compra")
        print("2-Consultar compra")
        sub = input("Operacao (V para voltar): ")

        if sub == '1':
            compra.create_compra()
        elif sub == '2':
            compra.read_compra()

key = 0
while key != 'S':
    print("\n1-Usuario")
    print("2-Vendedor")
    print("3-Produto")
    print("4-Compra")
    print("S-Sair")
    key = input("Acessar: ")

    if key == '1':
        menu_usuario()

    elif key == '2':
        menu_vendedor()

    elif key == '3':
        menu_produto()

    elif key == '4':
        menu_compra()

driver.close()
print("Tchau prof...")