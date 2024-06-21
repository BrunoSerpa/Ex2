from pymongo.mongo_client import MongoClient
import os
from bson.objectid import ObjectId
from conexaoMongo import conectar
from validacoes import validarNaoVazio, validarFloat
from formatacaoJson import produtoJson
from busca import buscarProduto, buscarVendedor

produtos = conectar().Produto

def atualizarProdutos(produtos, idVendedor):
    vendedores = conectar().Vendedor
    try:
        vendedores.update_one({"_id": ObjectId(idVendedor)}, {"$set": {"produtos": produtos}})
        print("Produtos atualizados com sucesso")
        return True
    except Exception as e:
        print(f"Erro ao vincular o produto: {e}")
        input("Insira qualquer coisa para continuar...")
    return False

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not validacao(entrada):
            print(erroMensagem)
        else:
            return entrada

def cadastrarProduto(vendedor=None):
    os.system('cls')
    print("Cadastrando produto...")
    atualizaVendedor = False
    while not vendedor:
        atualizaVendedor = True
        achouVendedor = buscarVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if isinstance(achouVendedor, dict): vendedor = achouVendedor
        elif not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else:
            vendedor = buscarVendedor(input('Insira o id do vendedor desejado: '), 'id', False)
            if vendedor == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    nomeProduto = obterEntrada("Insira o nome do produto: ", validarNaoVazio, "Nome não pode estar em branco.")
    valorProduto = float(obterEntrada("Insira o valor do produto: R$", validarFloat, "O valor só pode ser um número."))
    produto = {
        "id_vendedor": vendedor["_id"],
        "nome_vendedor": vendedor["nome_vendedor"],
        "nome_produto": nomeProduto,
        "valor_produto": valorProduto
    }
    try:
        produtos.insert_one(produto)
        print("Produto cadastrado com sucesso!")
        vendedor["produtos"].append(produto)
        if atualizaVendedor:
            atualizarProdutos(vendedor["produtos"], vendedor["_id"])
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        input("Insira qualquer coisa para continuar...")
    return produto

def listarProduto():
    os.system('cls')
    print("Listando produtos...")
    if input("Deseja procurar um produto específico? (S/N)\n").upper() == 'S':
        while True:
            nomeProduto = input('Insira o nome do produto desejado: ')
            achouProduto = buscarProduto(nomeProduto, 'nome', False, True)
            if not achouProduto:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Produtos Existentes:')
        buscarProduto('', 'nome', False, True)

def atualizarProduto(produto=None):
    atualizaVendedor = False
    while not produto:
        atualizaVendedor = True
        os.system('cls')
        print("Editando produto...")
        achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
        if isinstance(achouProduto, dict): produto = achouProduto
        elif not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else:
            produto = buscarProduto(input('Insira o id do produto desejado: '), 'id', False)
            if not produto:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    produto["nome_produto"] = obterEntrada("Insira o novo nome do produto: ", validarNaoVazio, "Nome não pode estar em branco.")
    produto["valor_produto"] = float(obterEntrada("Insira o novo valor do produto: R$", validarFloat, "O valor só pode ser um número."))
    try:
        produtos.update_one({"_id": produto["_id"]}, {"$set": produto})
    except Exception as e:
        print(f"Erro ao atualizar o produto: {e}")
        input("Insira qualquer coisa para continuar...")
    if atualizaVendedor:
        vendedor = buscarVendedor(produto["id_vendedor"], 'id', False)
        if vendedor:
            produtos_vendedor = [produto if p["_id"] == produto["_id"] else p for p in vendedor["produtos"]]
            atualizarProdutos(produtos_vendedor, vendedor["_id"])
        print("Produto e vendedor atualizados com sucesso!")
    else: print("Produto atualizado com sucesso!")
    return produto

def deletarProduto(produto=None):
    atualizaVendedor = False
    while not produto:
        atualizaVendedor = True
        os.system('cls')
        print("Editando produto...")
        achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
        if isinstance(achouProduto, dict): produto = achouProduto
        elif not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else:
            produto = buscarProduto(input('Insira o id do produto desejado: '), 'id', False)
            if not produto:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    try:
        produtos.delete_one({"_id": produto["_id"]})
    except Exception as e:
        print(f"Erro ao deletar o produto: {e}")
        input("Insira qualquer coisa para continuar...")
    if atualizaVendedor:
        vendedor = buscarVendedor(produto["id_vendedor"], 'id', False)
        if vendedor:
            vendedor["produtos"] = [p for p in vendedor["produtos"] if p["_id"] != produto["_id"]]
            atualizarProdutos(vendedor["produtos"], vendedor["_id"])
        print("Produto deletado com sucesso! Produtos do vendedor atualizados!")
    else:
        print("Produto deletado com sucesso!")

def gerenciarProdutos(produtos, idVendedor):
    ids = []
    os.system('cls')
    print("Produtos Atuais:")
    if not produtos:
        print("Nenhum produto cadastrado!")
    else:
        for produto in produtos:
            ids.append(produto["_id"])
            print("================================")
            produtoJson(produto, True, False)
        print("================================")
    print("")
    print("================================")
    print("O que deseja fazer com os produtos?")
    print("--------------------------------")
    print("1 - Criar um novo Produto")
    if len(ids) > 0:
        print("2 - Editar um produto existente")
        print("3 - Deletar um produto existente")
    print("--------------------------------")
    print("0 - Voltar")
    print("================================")
    opcao = input("Insira uma opção: ")
    if opcao == '1':
        vendedor = buscarVendedor(idVendedor, 'id', False)
        if vendedor:
            novoProduto = cadastrarProduto(vendedor)
            if novoProduto: produtos.append(novoProduto)
    elif opcao in ['2', '3'] and len(ids) > 0:
        idProduto = input("Insira o id do produto desejado: ")
        try:
            idProduto = ObjectId(idProduto)
            produto = next((p for p in produtos if p["_id"] == idProduto), None)
            if not produto:
                print("ID inválido.")
                input("Insira qualquer coisa para continuar...")
            elif opcao == '2':
                produtoAtualizado = atualizarProduto(produto)
                produtos = [produtoAtualizado if p["_id"] == produtoAtualizado["_id"] else p for p in produtos]
            elif opcao == '3':
                if deletarProduto(produto): produtos.remove(produto)
        except Exception as e:
            print(f"Erro ao processar o ID: {e}")

    elif opcao != "0": print('Comando inválido.')
    return produtos