from validacoes import validarNaoVazio
import os

def menuCliente():
    while True:
        print("================================")
        print("O que deseja fazer?")
        print("--------------------------------")
        print("1 - Cadastar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Deletar cliente")
        print("--------------------------------")
        print("0 - Voltar para menu")
        print("================================")
        opcao=input("Insira uma opção: ")
        os.system('cls')
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            break
        elif opcao == "1":
            cadastrarCliente()
        elif opcao == "2":
            listarCliente()
        elif opcao == "3":
            atualizarCliente()
        elif opcao == "4":
            deletarCliente()
        else:
            print("Opção inválida!")

def menuVendedor():
    while True:
        print("================================")
        print("O que deseja fazer?")
        print("--------------------------------")
        print("1 - Cadastar vendedor")
        print("2 - Listar vendedores")
        print("3 - Atualizar vendedor")
        print("4 - Deletar vendedor")
        print("--------------------------------")
        print("0 - Voltar para menu")
        print("================================")
        opcao=input("Insira uma opção: ")
        os.system('cls')
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            break
        elif opcao == "1":
            cadastrarVendedor()
        elif opcao == "2":
            listarVendedor()
        elif opcao == "3":
            atualizarVendedor()
        elif opcao == "4":
            deletarVendedor()
        else:
            print("Opção inválida!")

def menuProduto():
    while True:
        print("================================")
        print("O que deseja fazer?")
        print("--------------------------------")
        print("1 - Cadastar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Deletar produto")
        print("--------------------------------")
        print("0 - Voltar para menu")
        print("================================")
        opcao=input("Insira uma opção: ")
        os.system('cls')
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            break
        elif opcao == "1":
            cadastrarProduto()
        elif opcao == "2":
            listarProduto()
        elif opcao == "3":
            atualizarProduto()
        elif opcao == "4":
            deletarProduto()
        else:
            print("Opção inválida!")

def menuCompra():
    while True:
        print("================================")
        print("O que deseja fazer?")
        print("--------------------------------")
        print("1 - Cadastar compra")
        print("2 - Listar compras")
        print("--------------------------------")
        print("0 - Voltar para menu")
        print("================================")
        opcao=input("Insira uma opção: ")
        os.system('cls')
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            break
        elif opcao == "1":
            cadastrarCompra()
        elif opcao == "2":
            listarCompras()
        else:
            print("Opção inválida!")

def Home():
    while True:        
        print("================================")
        print("O que deseja fazer?")
        print("--------------------------------")
        print("1 - Gerenciar Clientes")
        print("2 - Gerenciar Vendedores")
        print("3 - Gerenciar Produtos")
        print("4 - Gerenciar Compras")
        print("--------------------------------")
        print("0 - Sair")
        print("================================")
        opcao=input("Insira uma opção: ")
        os.system('cls')
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            break
        elif opcao == "1":
            menuCliente()
        elif opcao == "2":
            menuVendedor()
        elif opcao == "3":
            menuProduto()
        elif opcao == "4":
            menuCompra()
        else:
            print("Opção inválida!")