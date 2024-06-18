from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
# CONEXÃO COM A COLEÇÃO DE PRODUTO
from conexaoMongo import conectar
global produtos
produtos = conectar().Produto
from validacoes import validarNaoVazio, validarFloat
from busca import buscarProduto, buscaVendedor
from formatacaoJson import produtoJson

def atualizandoProdutosVendedor(produtos, idVendedor):
    vendedores= conectar().Vendedor
    try:
        atualizou = vendedores.update_one({"_id": ObjectId(idVendedor)}, {"$set": {"produtos": produtos}})
        print("Produto atualizados com sucesso")
        return True
    except Exception as e:
        print(f"Erro ao vincular o produto: {e}")
    return False

def cadastrarProduto(vendedor):
    os.system('cls')
    print("Cadastrando produto...")
    arrumaVendedor = False
    if not vendedor:
        while True:
            achouVendedor = buscaVendedor(input('Insira o nome do vendedor: '), 'nome', True)
            if not achouVendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                return
            elif isinstance(achouVendedor, dict):
                vendedor = achouVendedor 
            elif not isinstance(achouVendedor, dict):
                while True:
                    vendedor = buscaVendedor(input('Insira o id do vendedor desejado: '), 'id', False)
                    if vendedor == None:
                        if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                        else: return
                    break
            arrumaVendedor = True
            break
    while True:
        nomeProduto=input("Insira o nome do produto: ")
        if not validarNaoVazio(nomeProduto): 
            print("Nome não pode estar em branco.")
            continue
        break
    while True:
        valorProduto = input("Insira o valor do produto: R$")
        if not validarFloat(valorProduto): 
            print("O valor só pode ser um número.")
            continue
        valorProduto = float(valorProduto)
        break
    produto = {
        "id_vendedor": vendedor["_id"],
        "nome_vendedor": vendedor["nome_vendedor"],
        "nome_produto": nomeProduto,
        "valor_produto": valorProduto
    }
    try:
        produtos.insert_one(produto)
        print("Produto cadastrado com sucesso!")
        if arrumaVendedor:
            vendedor["produtos"] = [*vendedor["produtos"]]
            vendedor["produtos"].append(produto)
            if not atualizandoProdutosVendedor(vendedor["produtos"], vendedor["_id"]):
                produtos.delete_one({ "_id": produto["_id"] })
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
    return produto

# FUNÇÃO LISTAR
def listarProduto():
    os.system('cls')
    print("Listando produtos...")
    if input("Deseja procurar um produto específico? (S/N)\n").upper() == 'S':
        while True:
            nomeProduto = input('Insira o nome do produto desejado: ')
            achouProduto = buscarProduto(nomeProduto, 'nome', False)
            if not achouProduto:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Produtos Existentes:')
        listaProdutos = produtos.find().sort("nome_produto")
        count = 0
        for produto in listaProdutos:
            count += 1
            print("===========================================")
            produtoJson(produto)
        if count == 0:
            print("Nenhum produto cadastrado!")
        else:
            print("===========================================")

def deletarProduto(produto):
    arrumaVendedor = False
    if not produto:
        while True:
            achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
            if not achouProduto:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                return
            elif isinstance(achouProduto, dict):
                produto = achouProduto 
            elif not isinstance(produto, dict):
                while True:
                    produto = buscarProduto(input('Insira o id do produto desejado: '), 'id', False, True)
                    if produto == None:
                        if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                        else: return
                    break
            break
        arrumaVendedor = True
    try:
        produtos.delete_one({ "_id": produto["_id"] })
        print("Produto deletado com sucesso!!")
        if arrumaVendedor:
            vendedor = buscaVendedor(produto["id_vendedor"], 'id', False)
            listaProdutos = [*vendedor["produtos"]]
            listaProdutos.remove(produto)
            if not atualizandoProdutosVendedor(listaProdutos, produto["id_vendedor"]):
                produtos.insert_one(produto)
        return True
    except Exception as e:
        print(f"Erro ao deletar o produto: {e}")
        return False

def gerenciarProdutos(produtos, idVendedor):
    ids=[]
    print("Produtos Atuais:")
    if not produtos: 
        print("Nenhum produto cadastrado!")
    else:
        for produto in produtos:
            print("================================")
            print(f'Código Produto: {produto["_id"]}')
            ids.append(produto["_id"])
            produtoJson(produto)
        print("================================")
    print('O que deseja fazer com os produtos?')
    print('1 - Criar um novo Produto')
    if produtos:
        print('2 - Editar um produto existente')
        print('3 - Deletar um produto existente')
    print('0 - Voltar')
    opcao = int(input('Insira a opção desejada: '))
    if opcao == 0:
        return produtos
    elif opcao == 1:
        novoproduto = cadastrarProduto(idVendedor)
        if novoproduto:
            produtos.append(novoproduto)
        return produtos
    elif produtos:  
        if opcao == 2:
            idProduto = ObjectId(input("Insira o id do objeto:"))
            if idProduto in ids: 
                for produto in produtos:
                    if produto["_id"] == idProduto:
                        produto = atualizarProduto(produto)
            return produtos
        elif opcao == 3:
            idProduto = ObjectId(input("Insira o id do objeto:"))
            if idProduto in ids: 
                for produto in produtos:
                    if produto["_id"] == idProduto:
                        deletou = deletarProduto(produto)
                        if deletou: produtos.remove(produto)
            return produtos
    print('Comando incorreto! :(')
    return produtos

def atualizarProduto(produto):
    arrumarVendedor = False
    while True:
        if not produto:
            achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True)
            if not achouProduto:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': 
                    continue
                else: 
                    return
            produto = buscaVendedor(input('Insira o id do produto desejado: '), 'id', False)
            if produto == None:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': 
                    continue
                else: 
                    return
            arrumarVendedor = True
            break
    while True:
        nomeProduto=input("Insira o nome do produto: ")
        if not validarNaoVazio(nomeProduto): 
            print("Nome não pode estar em branco.")
            continue
        break
    while True:
        valorProduto = input("Insira o valor do produto: R$")
        if not validarFloat(valorProduto): 
            print("O valor só pode ser um número.")
            continue
        valorProduto = float(valorProduto)
        break
    produto["nome_produto"]=nomeProduto
    produto["valor_produto"]=valorProduto
    try:
        produtos.update_one({ "_id": produto["_id"] },{ "$set": produto })
        print("Produto atualizado com sucesso!!")
        if arrumarVendedor: 
            atualizarProduto(produto, "editar")
    except Exception as e:
        print(f"Erro ao atualizar o produto: {e}")
    return produto