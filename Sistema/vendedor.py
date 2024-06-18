from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
# CONEXÃO COM A COLEÇÃO DE CLIENTE
from conexaoMongo import conectar
vendedores = conectar().Vendedor

# VALIDAÇÕES
from validacoes import validarNaoVazio, validarCNPJ, validarEmail, validarTelefone

# ENDEREÇO
from endereco import cadastrarEnderecos, gerenciarEnderecos, enderecoJson

# FAVORITO
from produtos import cadastrarProduto, gerenciarProdutos
from busca import buscarProduto, buscaVendedor
from formatacaoJson import produtoJson, vendedorJson

# FUNÇÃO CADASTRAR
def cadastrarVendedor():
    os.system('cls')
    print("Cadastrando um vendedor...")
    while True:
        nome = input("Insira o nome do vendedor: ")
        if not validarNaoVazio(nome):
            print("Nome não pode estar em branco.")
            continue
        break
    while True:
        cnpj = input("Insira o CNPJ do vendedor: ")
        if not validarCNPJ(cnpj):
            print("CNPJ inválido. Deve conter 14 dígitos numéricos.")
            continue
        break
    while True:
        email = input("Insira o email do vendedor: ")
        if not validarEmail(email):
            print("Email inválido. Certifique-se de que contém '@' e '.'.")
            continue
        break
    while True:
        telefone = input("Insira o telefone do vendedor: ")
        if not validarTelefone(telefone):
            print("Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            continue
        break
    enderecos = cadastrarEnderecos()
    produtos = []
    vendedor = {
        "nome_vendedor": nome,
        "cnpj": cnpj,
        "email_vendedor": email,
        "telefone_vendedor": telefone,
        "enderecos": enderecos,
        "produtos": produtos
    }
    try:
        vendedores.insert_one(vendedor)
        print("Vendedor cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar vendedor: {e}")
    try:
        if input("Deseja cadastrar um produto? (S/N)\n").upper() == "S":
            while True:
                produto = cadastrarProduto(vendedor)
                if produto: 
                    produtos.append(produto)
                if input("Deseja cadastrar mais algum produto? (S/N)\n").upper() == "S":
                    continue
                break
            vendedores.update_one({"_id": vendedor["_id"]}, {"$set": {"produtos": produtos}})
            print("Produtos vinculados com sucesso!")
    except Exception as e:
        print(f"Erro ao vincular produtos ao vendedor: {e}")

# FUNÇÃO LISTAR
def listarVendedor():
    os.system('cls')
    print("Listando vendedores...")
    if input("Deseja procurar um vendedor específico? (S/N)\n").upper() == 'S':
        while True:
            nomeVendedor = input('Insira o nome do vendedor desejado: ')
            achouVendedor = buscaVendedor(nomeVendedor, 'nome', False)
            if not achouVendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Vendedores Existentes:')
        listaVendedores = vendedores.find().sort("nome_vendedor")
        count = 0
        for vendedor in listaVendedores:
            count += 1
            print("===========================================")
            vendedorJson(vendedor)
        if count == 0:
            print("Nenhum vendedor cadastrado!")
        else:
            print("===========================================")

# FUNÇÃO ATUALIZAR
def atualizarVendedor():
    os.system('cls')
    print("Editando vendedor...")
    while True:
        achouVendedor = buscaVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        elif not isinstance(achouVendedor, dict):
            while True:
                vendedor = buscaVendedor(input('Insira o id do vendedor desejado: '), 'id', False)
                if vendedor == None:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                    else: return
                break
        else: vendedor = achouVendedor
        break
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
        opcao=input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            try:
                vendedores.update_one({ "_id": vendedor["_id"] },{ "$set": vendedor })
                print("Vendedor atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao atualizar o vendedor: {e}")
            break
        elif opcao == "1":
            nome = input("Insira o novo nome do vendedor: ")
            if not validarNaoVazio(nome): print("Nome não pode estar em branco.")
            else: vendedor["nome_vendedor"] = nome
        elif opcao == "2":
            cnpj = input("Insira o novo CNPJ do vendedor: ")
            if not validarCNPJ(cnpj): print("CNPJ inválido. Deve conter 11 dígitos numéricos.")
            else: vendedor["cnpj"] = cnpj
        elif opcao == "3":
            email = input("Insira o email do vendedor: ")
            if not validarEmail(email): print("Email inválido. Certifique-se de que contém '@' e '.'.")
            else: vendedor["email_vendedor"]= email
        elif opcao == "4":
            telefone = input("Insira o telefone do vendedor: ")
            if not validarTelefone(telefone): print("Telefone inválido. Deve conter apenas dígitos e ter pelo menos 8 caracteres.")
            else: vendedor["telefone_vendedor"] = telefone
        elif opcao == "5": vendedor["enderecos"] = gerenciarEnderecos(vendedor["enderecos"])
        elif opcao == "6":
            if not vendedor["produtos"]:
                vendedor["produtos"] = []
            vendedor["produtos"] = gerenciarProdutos(vendedor["produtos"], idVendedor)

def atualizarProduto(produto, funcao):
    vendedor = buscaVendedor(produto["idVendedor"], 'id', False)
    if vendedor:
        if funcao == "cadastrar":
            if produtos in vendedor:
                vendedor["produtos"].append(produto)
            else:
                vendedor["produtos"]=[produto]
        elif funcao == "editar":
            for produtoVendedor in vendedor["produtos"]:
                if produtoVendedor["_id"] == produto["_id"]: produtoVendedor = produto
        else:
            for produtoVendedor in vendedor["produtos"]:
                if produtoVendedor["_id"] == produto["_id"]: vendedor["produtos"].remove(produtoVendedor)
    try:
        vendedores.update_one({ "_id": vendedor["_id"] },{ "$set": vendedor })
        print("Vendedor atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar o vendedor: {e}")

def deletarVendedor():
    while True:
        nomeVendedor = input('Insira o nome do vendedor desejado: ')
        achouVendedor = buscaVendedor(nomeVendedor, 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        while True:
            idVendedor = input('Insira o id do vendedor desejado: ')
            achouVendedor = buscaVendedor(idVendedor, 'id', False)
            if achouVendedor == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                else: return
            if produtos in achouVendedor:
                for produto in achouVendedor["produtos"]:        
                    deletarProduto(produto)
            vendedores.delete_one(achouVendedor)
            break    
        break