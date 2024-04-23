from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
# CONEXÃO COM A COLEÇÃO DE CLIENTE
from conexaoMongo import conectar
vendedores = conectar().Vendedor

# VALIDAÇÕES
from validacoes import validarNaoVazio, validarCPF, validarEmail, validarTelefone

# ENDEREÇO
from endereco import cadastrarEnderecos, gerenciarEnderecos, enderecoJson

# FAVORITO
from produtos import produtoJson, cadastrarProduto, gerenciarProdutos

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
        cpf = input("Insira o CPF do vendedor: ")
        if not validarCPF(cpf):
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
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
    novoVendedor = {
        "nome_vendedor": nome,
        "cpf": cpf,
        "email_vendedor": email,
        "telefone_vendedor": telefone,
        "enderecos": enderecos,
        "produtos": produtos
    }
    try:
        vendedor = vendedores.insert_one(novoVendedor)
        idVendedor = ObjectId(vendedor.inserted_id)
        print("Vendedor cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar vendedor: {e}")
    try:
        if input("Deseja cadastrar um produto? (S/N)\n").upper() == "S":
            while True:
                produto = cadastrarProduto(idVendedor)
                if produto: 
                    produtos.append(produto)
                if input("Deseja cadastrar mais algum produto? (S/N)\n").upper() == "S":
                    continue
                break
            vendedores.update_one({"_id": idVendedor}, {"$set": {"produtos": produtos}})
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
        nomeVendedor = input('Insira o nome do vendedor desejado: ')
        achouVendedor = buscaVendedor(nomeVendedor, 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        while True:
            idVendedor = input('Insira o id do vendedor desejado: ')
            vendedor = buscaVendedor(idVendedor, 'id', False)
            if vendedor == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                else: return
            break
        break
    while True:
        vendedorJson(vendedor)
        print("================================")
        print("Que tipo de dado deseja mudar?")
        print("--------------------------------")
        print("1 - Nome")
        print("2 - CPF")
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
            cpf = input("Insira o novo CPF do vendedor: ")
            if not validarCPF(cpf): print("CPF inválido. Deve conter 11 dígitos numéricos.")
            else: vendedor["cpf"] = cpf
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
            
            vendedores.delete_one(achouVendedor)
            break    
        break
# PROCURAR CLIENTE ESPECÍFICO
def buscaVendedor(dadoProcurado, tipoDado, comCodigo):
    global vendedores
    if tipoDado == 'nome':
        listaVendedores = vendedores.find({"nome_vendedor": dadoProcurado}).sort("nome_vendedor")
        count = 0
        primeiroVendedor= None
        for vendedor in listaVendedores:
            count+=1
            if count > 1 and primeiroVendedor==None:
                vendedorJson(vendedor)                    
                print("===========================================")
                if comCodigo and "_id" in vendedor:
                    print(f'Id: {vendedor["_id"]}') 
                vendedorJson(vendedor)
            elif primeiroVendedor != None:
                print("===========================================")
                if comCodigo and "_id" in primeiroVendedor:
                    print(f'Id: {primeiroVendedor["_id"]}') 
                vendedorJson(primeiroVendedor)
                print("===========================================")
                if comCodigo and "_id" in vendedor:
                    print(f'Id: {vendedor["_id"]}') 
                primeiroVendedor = None
            else:
                primeiroVendedor = vendedor
        if primeiroVendedor != None:
            if comCodigo and "_id" in primeiroVendedor:
                print("===========================================")
                print(f'Id: {primeiroVendedor["_id"]}') 
            vendedorJson(primeiroVendedor)
        elif count == 0:
            print("Nenhum vendedor encontrado!")
            return False
        print("===========================================")
        return True
    else:
        vendedor = vendedores.find_one({"_id": ObjectId(dadoProcurado)})
        if vendedor:
            print("Vendedor encontrado!")
            return vendedor
        else:
            print("Nenhum Vendedor encontrado!")
            return None
    
# FORMATAÇÃO JSON CLIENTE
def vendedorJson(arquivoJson):
    if "nome_vendedor" in arquivoJson:
        print(f'Nome: {arquivoJson["nome_vendedor"]}')
    if "cpf" in arquivoJson:
        print(f'CPF: {arquivoJson["cpf"]}')
    if "email_vendedor" in arquivoJson:
        print(f'Emai: {arquivoJson["email_vendedor"]}')
    if "telefone_vendedor" in arquivoJson:
        print(f'Telefone: {arquivoJson["telefone_vendedor"]}')
    count = 0
    for endereco in arquivoJson["enderecos"]:
        count += 1
        print("-----------------------------------------------")
        print(f'{count}º Endereco:')
        enderecoJson(endereco)
    count1 = 0
    for produto in arquivoJson["produtos"]:
        count1 += 1
        print("-----------------------------------------------")
        print(f'{count1}º Produto:')
        produtoJson(produto)
    if count != 0 or count1 != 0:
        print("-----------------------------------------------")