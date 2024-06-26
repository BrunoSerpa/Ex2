from conexaoMongo import conectar
from conexaoRedis import cacheResultado, obterCache
from formatacaoJson import usuarioJson, vendedorJson, produtoJson, comprasJson
from bson.objectid import ObjectId

def buscarDocumento(colecao, filtro, sort=None):
    documentos = colecao.find(filtro).sort(sort) if sort else colecao.find(filtro)
    documentos = list(documentos)
    return documentos if documentos else None

def buscarPorId(colecao, objectId): return colecao.find_one({"_id": ObjectId(objectId)})

def buscarUsuario(dadoProcurado, tipoDado, comCodigo=False):
    usuarios = conectar().Usuario
    filtro = {}
    if tipoDado == 'nome': filtro = {"nome_usuario": {"$regex": dadoProcurado, "$options": "i"}} if dadoProcurado else {}
    elif tipoDado == 'id': filtro = {"_id": ObjectId(dadoProcurado)}
    chaveCache = f"usuario:{str(filtro)}"
    resultadoCache = obterCache(chaveCache)
    if resultadoCache: return resultadoCache
    listaUsuarios = buscarDocumento(usuarios, filtro, "nome_usuario" if tipoDado == 'nome' else None)
    if not listaUsuarios:
        print("Nenhum usuário encontrado!")
        return False
    cacheResultado(chaveCache, listaUsuarios)
    for usuario in listaUsuarios:
        print("===========================================")
        usuarioJson(usuario, comCodigo=comCodigo)
    print("===========================================")
    return listaUsuarios if len(listaUsuarios) > 1 else listaUsuarios[0]

def buscarVendedor(dadoProcurado, tipoDado, comCodigo=False):
    vendedores = conectar().Vendedor
    filtro = {}
    if tipoDado == 'nome': filtro = {"nome_vendedor": {"$regex": dadoProcurado, "$options": "i"}} if dadoProcurado else {}
    elif tipoDado == 'id': filtro = {"_id": ObjectId(dadoProcurado)}
    chaveCache = f"vendedor:{str(filtro)}"
    resultadoCache = obterCache(chaveCache)
    if resultadoCache: return resultadoCache
    listaVendedores = buscarDocumento(vendedores, filtro, "nome_vendedor" if tipoDado == 'nome' else None)
    if not listaVendedores:
        print("Nenhum vendedor encontrado!")
        return False
    cacheResultado(chaveCache, listaVendedores)
    for vendedor in listaVendedores:
        print("===========================================")
        vendedorJson(vendedor, comCodigo=comCodigo)
    print("===========================================")
    return listaVendedores if len(listaVendedores) > 1 else listaVendedores[0]

def buscarProduto(dadoProcurado, tipoDado, comCodigo=False, comVendedor=False):
    produtos = conectar().Produto
    filtro = {}
    if tipoDado == 'nome': filtro = {"nome_produto": {"$regex": dadoProcurado, "$options": "i"}} if dadoProcurado else {}
    elif tipoDado == 'id': filtro = {"_id": ObjectId(dadoProcurado)}
    chaveCache = f"produto:{str(filtro)}"
    resultadoCache = obterCache(chaveCache)
    if resultadoCache: return resultadoCache
    listaProdutos = buscarDocumento(produtos, filtro, "nome_produto" if tipoDado == 'nome' else None)
    if not listaProdutos:
        print("Nenhum produto encontrado!")
        return False
    cacheResultado(chaveCache, listaProdutos)
    for produto in listaProdutos:
        print("===========================================")
        produtoJson(produto, comCodigo=comCodigo, comVendedor=comVendedor)
    print("===========================================")
    return listaProdutos if len(listaProdutos) > 1 else listaProdutos[0]

def buscarCompra(dadoProcurado, tipoDado, comCodigo=False):
    compras = conectar().Compras
    filtro = {}
    if tipoDado == 'nome_cliente': filtro = {"nome_cliente": {"$regex": dadoProcurado, "$options": "i"}} if dadoProcurado else {}
    elif tipoDado == 'cod_cliente': filtro = {"cod_cliente": ObjectId(dadoProcurado)}
    elif tipoDado == 'nome_vendedor': filtro = {"nome_vendedor": {"$regex": dadoProcurado, "$options": "i"}} if dadoProcurado else {}
    elif tipoDado == 'cod_vendedor': filtro = {"cod_vendedor": ObjectId(dadoProcurado)}
    chaveCache = f"compra:{str(filtro)}"
    resultadoCache = obterCache(chaveCache)
    if resultadoCache: return resultadoCache
    listaCompras = buscarDocumento(compras, filtro, [("data_compra", 1)] if 'data_compra' in filtro else None)
    if not listaCompras:
        print("Nenhuma compra encontrada!")
        return False
    cacheResultado(chaveCache, listaCompras)
    for compra in listaCompras:
        print("===========================================")
        comprasJson(compra, tipoDado in ['nome_vendedor', 'cod_vendedor'], tipoDado in ['nome_cliente', 'cod_cliente'], comCodigo)
    print("===========================================")
    return listaCompras if len(listaCompras) > 1 else listaCompras[0]