from pymongo.mongo_client import MongoClient
import os
from conexaoMongo import conectar
from conexaoRedis import cacheResultado, obterCache
from validacoes import validarNaoVazio, validarCPF, validarEmail, validarTelefone
from formatacaoJson import usuarioJson, enderecoJson, produtoJson
from busca import buscarUsuario
from endereco import cadastrarEnderecos, gerenciarEnderecos
from favoritos import gerenciarFavoritos
from compras import fazerCompra
usuarios = conectar().Usuario

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not validacao(entrada): print(erroMensagem)
        else: return entrada

def cadastrarUsuario():
    os.system('cls')
    print("Cadastrando um usuário...")    
    nome = obterEntrada("Insira o nome do usuário: ", validarNaoVazio, "Nome não pode estar em branco.")
    cpf = obterEntrada("Insira o CPF do usuário: ", validarCPF, "CPF inválido. Deve conter 11 dígitos numéricos.")
    email = obterEntrada("Insira o email do usuário: ", validarEmail, "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = obterEntrada("Insira o telefone do usuário: ", validarTelefone, "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
    enderecos = cadastrarEnderecos()
    novoUsuario = {
        "nome_usuario": nome,
        "cpf": cpf,
        "email_usuario": email,
        "telefone_usuario": telefone,
        "enderecos": enderecos,
        "favoritos": [],
        "compras": []
    }
    try:
        usuarios.insert_one(novoUsuario)
        print("Usuário cadastrado com sucesso!")
        cacheResultado(f'usuario:id:{novoUsuario["_id"]}', novoUsuario)
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        input("Insira qualquer coisa para continuar...")

def atualizarUsuario(usuario = None):
    os.system('cls')
    print("Editando usuário...")
    if not usuario:
        print("Nenhum usuário foi encontrado!")
        return
    chaveCache = f"usuario:id:{usuario.get('_id')}"
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
        print("7 - Fazer compras")
        print("--------------------------------")
        print("0 - Salvar e sair")
        print("================================")
        opcao = input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            print("Insira uma das opções!")
            continue
        if opcao == "0":
            try:
                usuarios.update_one({"_id": usuario["_id"]}, {"$set": usuario})
                cacheResultado(chaveCache, usuario)
                print("Usuário atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao editar usuário: {e}")
                input("Insira qualquer coisa para continuar...")
            break
        elif opcao == "1": usuario["nome_usuario"] = obterEntrada("Insira o novo nome do usuário: ", validarNaoVazio, "Nome não pode estar em branco.")
        elif opcao == "2": usuario["cpf"] = obterEntrada("Insira o novo CPF do usuário: ", validarCPF, "CPF inválido. Deve conter 11 dígitos numéricos.")
        elif opcao == "3": usuario["email_usuario"] = obterEntrada("Insira o email do usuário: ", validarEmail, "Email inválido. Certifique-se de que contém '@' e '.'.")
        elif opcao == "4": usuario["telefone_usuario"] = obterEntrada("Insira o telefone do usuário: ", validarTelefone, "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
        elif opcao == "5": usuario["enderecos"] = gerenciarEnderecos(usuario.get("enderecos", []))
        elif opcao == "6": usuario["favoritos"] = gerenciarFavoritos(usuario.get("favoritos", []))
        elif opcao == "7":
            novaCompra = fazerCompra(usuario)
            if novaCompra:
                if "compras" in usuario: usuario["compras"].append(novaCompra)
                else: usuario["compras"] = [novaCompra]

def deletarUsuario():
    while True:
        dadoProcurado = input('Insira o nome do usuário desejado: ')
        chaveCache = f"usuario:nome:{dadoProcurado}"
        usuario = obterCache(chaveCache)
        if not usuario:
            achouUsuario = buscarUsuario(dadoProcurado, 'nome', True)
            if not achouUsuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            usuario = buscarUsuario(input('Insira o id do usuário desejado: '), 'id', False)
            if not usuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
            cacheResultado(chaveCache, usuario)
        break
    try:
        usuarios.delete_one(usuario)
        print("Usuário deletado com sucesso!")
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        input("Insira qualquer coisa para continuar...")