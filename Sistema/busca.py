# CONEXÃO COM A COLEÇÃO DE CLIENTE
from conexaoMongo import conectar
from bson.objectid import ObjectId
from formatacaoJson import usuarioJson, vendedorJson, produtoJson
        
def buscaUsuario(dadoProcurado, tipoDado, comCodigo):
    usuarios = conectar().Usuario
    if tipoDado == 'nome':
        if dadoProcurado == '':
            listaUsuarios = usuarios.find().sort("nome_usuario")
        else:
            listaUsuarios = usuarios.find({"nome_usuario": dadoProcurado}).sort("nome_usuario")
        count = 0
        listaUsuarios = [*listaUsuarios]
        if len(listaUsuarios) == 0:
            print("Nenhum usuário encontrado!")
            return False
        elif len(listaUsuarios) == 1:
            usuario = listaUsuarios[0]
            print("===========================================")
            if comCodigo and "_id" in usuario:
                print(f'Id: {usuario["_id"]}') 
            usuarioJson(usuario)
            print("===========================================")
            return usuario
        else:
            for usuario in listaUsuarios:
                print("===========================================")
                if comCodigo and "_id" in usuario:
                    print(f'Id: {usuario["_id"]}') 
                usuarioJson(usuario)
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

def buscaVendedor(dadoProcurado, tipoDado, comCodigo):
    vendedores = conectar().Vendedor
    if tipoDado == 'nome':
        if dadoProcurado == '':
            listaVendedores = vendedores.find().sort("nome_vendedor")
        else:
            listaVendedores = vendedores.find({"nome_vendedor": dadoProcurado}).sort("nome_vendedor")
        count = 0
        listaVendedores = [*listaVendedores]
        if len(listaVendedores) == 0:
            print("Nenhum usuário encontrado!")
            return False
        elif len(listaVendedores) == 1:
            vendedor = listaVendedores[0]
            print("===========================================")
            if comCodigo and "_id" in vendedor:
                print(f'Id: {vendedor["_id"]}') 
            vendedorJson(vendedor)
            print("===========================================")
            return vendedor
        else:
            for vendedor in listaVendedores:
                print("===========================================")
                if comCodigo and "_id" in vendedor:
                    print(f'Id: {vendedor["_id"]}') 
                vendedorJson(vendedor)
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

def buscarProduto(dadoProcurado, tipoDado, comCodigo, comVendedor):
    produtos = conectar().Produto
    if tipoDado == 'nome':
        if dadoProcurado == '':
            listaProdutos = produtos.find().sort("nome_produto")
        else:
            listaProdutos = produtos.find({"nome_produto": dadoProcurado}).sort("nome_produto")
        count = 0
        listaProdutos = [*listaProdutos]
        if len(listaProdutos) == 0:
            print("Nenhum produto encontrado!")
            return False
        elif len(listaProdutos) == 1:
            produto = listaProdutos[0]
            print("===========================================")
            if comCodigo and "_id" in produto:
                print(f'Id: {produto["_id"]}') 
            produtoJson(produto, comVendedor)
            print("===========================================")
            return produto
        else:
            for produto in listaProdutos:
                print("===========================================")
                if comCodigo and "_id" in produto:
                    print(f'Id: {produto["_id"]}') 
                produtoJson(produto, comVendedor)
            print("===========================================")
            return True
    else:
        produto = produtos.find_one({"_id": ObjectId(dadoProcurado)})
        if produto:
            print("Produto encontrado!")
            return produto
        else:
            print("Nenhum produto encontrado!")
            return None