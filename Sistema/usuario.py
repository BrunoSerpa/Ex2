from pymongo.mongo_client import MongoClient
import os
# CONEXÃO COM A COLEÇÃO DE CLIENTE
from conexaoMongo import conectar
usuarios = conectar().Usuario

# VALIDAÇÕES
from validacoes import validarNaoVazio, validarCPF, validarEmail, validarTelefone

# FORMATAÇÃO
from formatacaoJson import usuarioJson, enderecoJson, produtoJson

# BUSCAS
from busca import buscaUsuario

# ENDEREÇO
from endereco import cadastrarEnderecos, gerenciarEnderecos
# FAVORITO
from favoritos import gerenciarFavoritos

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
        buscaUsuario('', 'nome', False)

# FUNÇÃO ATUALIZAR
def atualizarUsuario():
    os.system('cls')
    print("Editando usuário...")
    while True:
        achouUsuario = buscaUsuario(input('Insira o nome do usuário desejado: '), 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        elif not isinstance(achouUsuario, dict):
            while True:
                usuario = buscaUsuario(input('Insira o id do usuário desejado: '), 'id', False)
                if usuario == None:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                    else: return
                break
        else: usuario = achouUsuario 
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
        elif opcao == "5":
            if not usuario["enderecos"]: usuario["enderecos"] = []
            usuario["enderecos"] = gerenciarEnderecos(usuario["enderecos"])
        elif opcao == "6":
            if not usuario["favoritos"]: usuario["favoritos"] = []
            usuario["favoritos"] = gerenciarFavoritos(usuario["favoritos"])
def deletarUsuario():
    while True:
        achouUsuario = buscaUsuario(input('Insira o nome do usuário desejado: '), 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        while True:
            achouUsuario = buscaUsuario(input('Insira o id do usuário desejado: '), 'id', False)
            if achouUsuario == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                else: return
            try:
                usuarios.delete_one(achouUsuario)
                print("Usuário deletado com sucesso!")
            except Exception as e:
                print(f"Erro ao deletar usuário: {e}")
            break
            print(" ")
            break
        break
    
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
    count1 = 0
    for favorito in arquivoJson["favoritos"]:
        count1 += 1
        print("-----------------------------------------------")
        print(f'{count1}º Favorito:')
        produtoJson(favorito, False)
    if count != 0 or count1 != 0:
        print("-----------------------------------------------")