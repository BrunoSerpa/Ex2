from pymongo.mongo_client import MongoClient
import os
from conexaoMongo import conectar
from validacoes import validarNaoVazio, validarCNPJ, validarEmail, validarTelefone
from formatacaoJson import vendedorJson, enderecoJson, produtoJson
from busca import buscarVendedor
from endereco import cadastrarEnderecos, gerenciarEnderecos
from produtos import cadastrarProduto, gerenciarProdutos, deletarProduto
vendedores = conectar().Vendedor

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not validacao(entrada): print(erroMensagem)
        else: return entrada

def cadastrarVendedor():
    os.system('cls')
    print("Cadastrando um vendedor...")
    nome = obterEntrada("Insira o nome do vendedor: ", validarNaoVazio, "Nome não pode estar em branco.")
    cnpj = obterEntrada("Insira o CNPJ do vendedor: ", validarCNPJ, "CNPJ inválido. Deve conter 14 dígitos numéricos.")
    email = obterEntrada("Insira o email do vendedor: ", validarEmail, "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = obterEntrada("Insira o telefone do vendedor: ", validarTelefone, "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
    enderecos = cadastrarEnderecos()
    produtos = []
    while True:
        if input("Deseja cadastrar um produto? (S/N)\n").upper() != "S": break
        produto = cadastrarProduto()
        if produto: produtos.append(produto)
    vendedor = {
        "nome_vendedor": nome,
        "cnpj": cnpj,
        "email_vendedor": email,
        "telefone_vendedor": telefone,
        "enderecos": enderecos,
        "produtos": produtos,
        "vendas": []
    }
    try:
        vendedores.insert_one(vendedor)
        print("Vendedor cadastrado com sucesso!")
    except Exception as e: 
        print(f"Erro ao cadastrar vendedor: {e}")
        input("Insira qualquer coisa para continuar...")

def listarVendedor():
    os.system('cls')
    print("Listando vendedores...")
    if input("Deseja procurar um vendedor específico? (S/N)\n").upper() == 'S':
        while True:
            nomeVendedor = input('Insira o nome do vendedor desejado: ')
            achouVendedor = buscarVendedor(nomeVendedor, 'nome', False)
            if not achouVendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Vendedores Existentes:')
        buscarVendedor('', 'nome', False)

def atualizarVendedor():
    os.system('cls')
    print("Editando vendedor...")
    vendedor = None
    while not vendedor:
        achouVendedor = buscarVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouVendedor, dict):
            vendedor = buscarVendedor(input('Insira o id do vendedor desejado: '), 'id', False)
            if not vendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: vendedor = achouVendedor
    while True:
        vendedorJson(vendedor)
        print("================================")
        print("Que tipo de dado deseja mudar?")
        print("--------------------------------")
        print("1 - Nome")
        print("2 - CNPJ")
        print("3 - Email")
        print("4 - Telefone")
        print("5 - Endereços")
        print("6 - Produtos")
        print("--------------------------------")
        print("0 - Salvar e sair")
        print("================================")
        opcao = input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            if "produtos" in vendedor:
                produtos = conectar().Produto
                for produto in vendedor["produtos"]:
                    try:
                        produto["nome_vendedor"] = vendedor["nome_vendedor"]
                        produtos.update_one({"_id": produto["_id"]}, {"$set": produto})
                    except Exception as e:
                        print(f"Erro ao atualizar o produto: {e}")
                        input("Insira qualquer coisa para continuar...")
                resposta = "Vendedor e seus produtos atualizados com sucesso!"
            else: resposta = "Vendedor atualizado com sucesso!"
            try:
                vendedores.update_one({"_id": vendedor["_id"]}, {"$set": vendedor})
            except Exception as e:
                print(f"Erro ao atualizar o vendedor: {e}")
                input("Insira qualquer coisa para continuar...")
            print(resposta)
            break
        elif opcao == "1":
            vendedor["nome_vendedor"] = obterEntrada("Insira o novo nome do vendedor: ", validarNaoVazio, "Nome não pode estar em branco.")
        elif opcao == "2":
            vendedor["cnpj"] = obterEntrada("Insira o novo CNPJ do vendedor: ", validarCNPJ, "CNPJ inválido. Deve conter 14 dígitos numéricos.")
        elif opcao == "3":
            vendedor["email_vendedor"] = obterEntrada("Insira o email do vendedor: ", validarEmail, "Email inválido. Certifique-se de que contém '@' e '.'.")
        elif opcao == "4":
            vendedor["telefone_vendedor"] = obterEntrada("Insira o telefone do vendedor: ", validarTelefone, "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
        elif opcao == "5":
            vendedor["enderecos"] = gerenciarEnderecos(vendedor.get("enderecos", []))
        elif opcao == "6":
            vendedor["produtos"] = gerenciarProdutos(vendedor.get("produtos", []), vendedor["_id"])

def deletarVendedor():
    os.system('cls')
    print("Deletando vendedor...")
    vendedor = None
    while not vendedor:
        achouVendedor = buscarVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouVendedor, dict):
            vendedor = buscarVendedor(input('Insira o id do vendedor desejado: '), 'id', False)
            if not vendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: vendedor = achouVendedor
    try:
        if "produtos" in vendedor:
            for produto in vendedor["produtos"]: deletarProduto(produto)
        vendedores.delete_one({"_id": vendedor["_id"]})
        print("Vendedor deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar o vendedor: {e}")
        input("Insira qualquer coisa para continuar...")