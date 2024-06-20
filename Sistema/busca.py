from conexaoMongo import conectar
from formatacaoJson import usuarioJson, vendedorJson, produtoJson
from bson.objectid import ObjectId

def buscarDocumento(colecao, filtro, sort=None):
    documentos = colecao.find(filtro).sort(sort) if sort else colecao.find(filtro)
    documentos = list(documentos)
    return documentos if documentos else None

def buscarPorId(colecao, objectId): return colecao.find_one({"_id": ObjectId(objectId)})

def buscarUsuario(dadoProcurado, tipoDado, comCodigo=False):
    usuarios = conectar().Usuario
    if tipoDado == 'nome':
        filtro = {} if dadoProcurado == '' else {"nome_usuario": dadoProcurado}
        listaUsuarios = buscarDocumento(usuarios, filtro, "nome_usuario")
        if not listaUsuarios:
            print("Nenhum usuário encontrado!")
            return False
        for usuario in listaUsuarios:
            print("===========================================")
            usuarioJson(usuario, comCodigo=comCodigo)
        print("===========================================")
        return listaUsuarios if len(listaUsuarios) > 1 else listaUsuarios[0]
    return buscarPorId(usuarios, dadoProcurado)

def buscarVendedor(dadoProcurado, tipoDado, comCodigo=False):
    vendedores = conectar().Vendedor
    if tipoDado == 'nome':
        filtro = {} if dadoProcurado == '' else {"nome_vendedor": dadoProcurado}
        listaVendedores = buscarDocumento(vendedores, filtro, "nome_vendedor")
        if not listaVendedores:
            print("Nenhum vendedor encontrado!")
            return False
        for vendedor in listaVendedores:
            print("===========================================")
            vendedorJson(vendedor, comCodigo)
        print("===========================================")
        return listaVendedores if len(listaVendedores) > 1 else listaVendedores[0]
    return buscarPorId(vendedores, dadoProcurado)

def buscarProduto(dadoProcurado, tipoDado, comCodigo=False, comVendedor=False):
    produtos = conectar().Produto
    if tipoDado == 'nome':
        filtro = {} if dadoProcurado == '' else {"nome_produto": dadoProcurado}
        listaProdutos = buscarDocumento(produtos, filtro, "nome_produto")
        if not listaProdutos:
            print("Nenhum produto encontrado!")
            return False
        for produto in listaProdutos:
            print("===========================================")
            produtoJson(produto, comCodigo=comCodigo, comVendedor=comVendedor)
        print("===========================================")
        return listaProdutos if len(listaProdutos) > 1 else listaProdutos[0]
    return buscarPorId(produtos, dadoProcurado)