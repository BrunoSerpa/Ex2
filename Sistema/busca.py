from conexaoMongo import conectar
from formatacaoJson import usuarioJson, vendedorJson, produtoJson, comprasJson
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

def buscarCompra(dadoProcurado, tipoDado, comCodigo=False):
    compras = conectar().Compras
    if tipoDado == 'nome_cliente':
        filtro = {} if dadoProcurado == '' else {"nome_cliente": dadoProcurado}
        listaCompras = buscarDocumento(compras, filtro, [("data_compra", 1)])
        if not listaCompras:
            print("Nenhuma compra encontrada!")
            return False
        for compra in listaCompras:
            print("===========================================")
            comprasJson(compra, False, True, comCodigo)
        print("===========================================")
        return listaCompras if len(listaCompras) > 1 else listaCompras[0]
    elif tipoDado == 'cod_cliente':
        compra = compras.find_one({"cod_cliente": ObjectId(dadoProcurado)})
        if compra:
            print("===========================================")
            comprasJson(compra, False, True, comCodigo)
            print("===========================================")
        else:
            print("Compra não encontrada!")
        return compra
    elif tipoDado == 'nome_vendedor':
        filtro = {} if dadoProcurado == '' else {"nome_vendedor": dadoProcurado}
        listaCompras = buscarDocumento(compras, filtro, [("data_compra", 1)])
        if not listaCompras:
            print("Nenhuma compra encontrada!")
            return False
        for compra in listaCompras:
            print("===========================================")
            comprasJson(compra, True, False, comCodigo)
        print("===========================================")
        return listaCompras if len(listaCompras) > 1 else listaCompras[0]
    elif tipoDado == 'cod_vendedor':
        compra = compras.find_one({"cod_vendedor": ObjectId(dadoProcurado)})
        if compra:
            print("===========================================")
            comprasJson(compra, True, False, comCodigo)
            print("===========================================")
        else:
            print("Compra não encontrada!")
        return compra