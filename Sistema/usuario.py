from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
# CONEXÃO COM A COLEÇÃO DE CLIENTE
from conexaoMongo import conectar
usuarios = conectar().Usuario

# VALIDAÇÕES
from validacoes import validarNaoVazio, validarCPF, validarEmail, validarTelefone

# ENDEREÇO
from endereco import cadastrarEnderecos, gerenciarEnderecos, enderecoJson
# FAVORITO
from favoritos import gerenciarFavoritos
from produtos import produtoJson

# FUNÇÃO CADASTRAR
def cadastrarUsuario():
    os.system('cls')
    print("Cadastrando um usuário...")
    while True:
        nome = input("Insira o nome do usuário: ")
        if not validarNaoVazio(nome):
            print("Nome não pode estar em branco.")
            continue
        break
    while True:
        cpf = input("Insira o CPF do usuário: ")
        if not validarCPF(cpf):
            print("CPF inválido. Deve conter 11 dígitos numéricos.")
            continue
        break
    while True:
        email = input("Insira o email do usuário: ")
        if not validarEmail(email):
            print("Email inválido. Certifique-se de que contém '@' e '.'.")
            continue
        break
    while True:
        telefone = input("Insira o telefone do usuário: ")
        if not validarTelefone(telefone):
            print("Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            continue
        break
    enderecos = cadastrarEnderecos()
    novoUsuario = {
        "nome_usuario": nome,
        "cpf": cpf,
        "email_usuario": email,
        "telefone_usuario": telefone,
        "enderecos": enderecos,
        "favoritos": []
    }
    try:
        usuarios.insert_one(novoUsuario)
        print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")

# FUNÇÃO LISTAR
def listarUsuario():
    os.system('cls')
    print("Listando usuários...")
    if input("Deseja procurar um usuário específico? (S/N)\n").upper() == 'S':
        while True:
            nomeUsuario = input('Insira o nome do usuário desejado: ')
            achouUsuario = buscaUsuario(nomeUsuario, 'nome', False)
            if not achouUsuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Usuários Existentes:')
        listaUsuarios = usuarios.find().sort("nome_usuario")
        count = 0
        for usuario in listaUsuarios:
            count += 1
            print("===========================================")
            usuarioJson(usuario)
        if count == 0:
            print("Nenhum usuário cadastrado!")
        else:
            print("===========================================")

# FUNÇÃO ATUALIZAR
def atualizarUsuario():
    os.system('cls')
    print("Editando usuário...")
    while True:
        nomeUsuario = input('Insira o nome do usuário desejado: ')
        achouUsuario = buscaUsuario(nomeUsuario, 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        while True:
            idUsuario = input('Insira o id do usuário desejado: ')
            usuario = buscaUsuario(idUsuario, 'id', False)
            if usuario == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                else: return
            break
        break
    while True:
        usuarioJson(usuario)
        print("================================")
        print("Que tipo de dado deseja mudar?")
        print("--------------------------------")
        print("1 - Nome")
        print("2 - CPF")
        print("3 - Email")
        print("4 - Telefone")
        print("5 - Endereços")
        print("6 - Produtos favoritos")
        print("--------------------------------")
        print("0 - Salvar e sair")
        print("================================")
        opcao=input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            try:
                usuarios.update_one({ "_id": usuario["_id"] },{ "$set": usuario })
                print("Usuário cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao editar usuário: {e}")
            break
        elif opcao == "1":
            nome = input("Insira o novo nome do usuário: ")
            if not validarNaoVazio(nome): print("Nome não pode estar em branco.")
            else: usuario["nome_usuario"] = nome
        elif opcao == "2":
            cpf = input("Insira o novo CPF do usuário: ")
            if not validarCPF(cpf): print("CPF inválido. Deve conter 11 dígitos numéricos.")
            else: usuario["cpf"] = cpf
        elif opcao == "3":
            email = input("Insira o email do usuário: ")
            if not validarEmail(email): print("Email inválido. Certifique-se de que contém '@' e '.'.")
            else: usuario["email_usuario"]= email
        elif opcao == "4":
            telefone = input("Insira o telefone do usuário: ")
            if not validarTelefone(telefone): print("Telefone inválido. Deve conter apenas dígitos e ter pelo menos 8 caracteres.")
            else: usuario["telefone_usuario"] = telefone
        elif opcao == "5": usuario["enderecos"] = gerenciarEnderecos(usuario["enderecos"])
        elif opcao == "6":
            if not usuario["favoritos"]:
                usuario["favoritos"] = []
            usuario["favoritos"] = gerenciarFavoritos(usuario["favoritos"])

def deletarUsuario():
    while True:
        nomeUsuario = input('Insira o nome do usuário desejado: ')
        achouUsuario = buscaUsuario(nomeUsuario, 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        while True:
            idUsuario = input('Insira o id do usuário desejado: ')
            achouUsuario = buscaUsuario(nomeUsuario, 'id', False)
            if achouUsuario == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                else: return
            usuarios.delete_one(achouUsuario)
        break
# PROCURAR CLIENTE ESPECÍFICO
def buscaUsuario(dadoProcurado, tipoDado, comCodigo):
    global usuarios
    if tipoDado == 'nome':
        listaUsuarios = usuarios.find({"nome_usuario": dadoProcurado}).sort("nome_usuario")
        count = 0
        primeiroUsuario= None
        for usuario in listaUsuarios:
            count+=1
            if count > 1 and primeiroUsuario==None:
                usuarioJson(usuario)                    
                print("===========================================")
                if comCodigo and "_id" in usuario:
                    print(f'Id: {usuario["_id"]}') 
                usuarioJson(usuario)
            elif primeiroUsuario != None:
                print("===========================================")
                if comCodigo and "_id" in primeiroUsuario:
                    print(f'Id: {primeiroUsuario["_id"]}') 
                usuarioJson(primeiroUsuario)
                print("===========================================")
                if comCodigo and "_id" in usuario:
                    print(f'Id: {usuario["_id"]}') 
                primeiroUsuario = None
            else:
                primeiroUsuario = usuario
        if primeiroUsuario != None:
            if comCodigo and "_id" in primeiroUsuario:
                print("===========================================")
                print(f'Id: {primeiroUsuario["_id"]}') 
                usuarioJson(primeiroUsuario)
        elif count == 0:
            print("Nenhum usuário encontrado!")
            return False
        print("===========================================")
        return True
    else:
        usuario = usuarios.find_one({"_id": ObjectId(dadoProcurado)})
        if usuario:
            print("Usuário encontrado!")
            return usuario
        else:
            print("Nenhum Usuário encontrado!")
            return None
    
# FORMATAÇÃO JSON CLIENTE
def usuarioJson(arquivoJson):
    if "nome_usuario" in arquivoJson:
        print(f'Nome: {arquivoJson["nome_usuario"]}')
    if "cpf" in arquivoJson:
        print(f'CPF: {arquivoJson["cpf"]}')
    if "email_usuario" in arquivoJson:
        print(f'Emai: {arquivoJson["email_usuario"]}')
    if "telefone_usuario" in arquivoJson:
        print(f'Telefone: {arquivoJson["telefone_usuario"]}')
    count = 0
    for endereco in arquivoJson["enderecos"]:
        count += 1
        print("-----------------------------------------------")
        print(f'{count}º Endereco:')
        enderecoJson(endereco)
    if count != 0:
        print("-----------------------------------------------")
    count = 0
    for favorito in arquivoJson["favoritos"]:
        count += 1
        print("-----------------------------------------------")
        print(f'{count}º Favorito:')
        produtoJson(favorito)
    if count != 0:
        print("-----------------------------------------------")