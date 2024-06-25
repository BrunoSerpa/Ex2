from pymongo.mongo_client import MongoClient
import os
from bson.objectid import ObjectId
from conexaoMongo import conectar
from validacoes import validarNaoVazio, validarFloat
from formatacaoJson import produtoJson
from busca import buscarProduto, buscarVendedor

produtos = conectar().Produto

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