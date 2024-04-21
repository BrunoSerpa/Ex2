from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
# CONEXÃO COM A COLEÇÃO DE PRODUTO
from conexaoMongo import conectar
global produtos
produtos = conectar().Produto

def buscarProduto(dadoProcurado, tipoDado, comCodigo):
    global produtos
    if tipoDado == 'nome':
        listaProdutos = produtos.find({"nome_produto": dadoProcurado}).sort("nome_produto")
        count = 0
        primeiroProduto= None
        for produto in listaProdutos:
            count+=1
            if count > 1 and primeiroProduto==None:
                print("===========================================")
                if comCodigo and "_id" in produto:
                    print(f'Id: {produto["_id"]}') 
                produtoJson(produto)
            elif primeiroProduto != None:
                print("===========================================")
                if comCodigo and "_id" in primeiroProduto:
                    print(f'Id: {primeiroProduto["_id"]}') 
                produtoJson(primeiroProduto)
                primeiroProduto = None
                print("===========================================")
                if comCodigo and "_id" in produto:
                    print(f'Id: {produto["_id"]}') 
            else:
                primeiroProduto = produto
        if primeiroProduto != None:
            print("===========================================")
            if comCodigo and "_id" in primeiroProduto:
                print(f'Id: {primeiroProduto["_id"]}') 
            produtoJson(primeiroProduto)
        elif count == 0:
            print("Nenhum usuário encontrado!")
            return False
        print("===========================================")
        return True
    else:
        produto = produtos.find_one({"_id": ObjectId(dadoProcurado)})
        if produto:
            print("Usuário encontrado!")
            return produto
        else:
            print("Nenhum Usuário encontrado!")
            return None

def produtoJson(arquivoJson):
    if "nome_produto" in arquivoJson:
        print(f'Nome: {arquivoJson["nome_produto"]}')
    if "valor_produto" in arquivoJson:
        print(f'Valor: R${arquivoJson["valor_produto"]:.2f}')