from datetime import datetime
import os
from busca import buscarCompra
from conexaoMongo import conectar
from conexaoRedis import cacheResultado, obterCache
from validacoes import validarNaoVazio, validarNumero
from busca import buscarUsuario, buscarVendedor
from formatacaoJson import produtoJson, enderecoJson, comprasJson
compras = conectar().Compras
vendedores = conectar().Vendedor
usuarios = conectar().Usuario

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not validacao(entrada): print(erroMensagem)
        else: return entrada

def fazerCompra(cliente=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Fazendo compras...")
    if not cliente: return
    if not cliente.get("enderecos"):
        print("Cadastre um endereço no cliente antes de fazer uma compra!")
        return
    enderecosCliente = cliente["enderecos"]
    enderecoCliente = None
    if len(enderecosCliente) > 1:
        while not enderecoCliente:
            print("Para onde devemos enviar o produto?")
            for endereco in enderecosCliente:
                print("================================")
                print(f'Código Endereço: {endereco["cod_endereco"]}')
                enderecoJson(endereco)
            print("================================\n")
            codigoEndereco = obterEntrada("Insira o código do endereço: ", validarNumero, "Número inválido. Deve conter apenas dígitos numéricos.")
            for i, endereco in enumerate(enderecosCliente):
                if endereco["cod_endereco"] == int(codigoEndereco):
                    enderecoCliente = endereco
                    break
            if not enderecoCliente:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
                else: continue
            break
    else: enderecoCliente = enderecosCliente[0]
    vendedor = None
    while not vendedor:
        dadoProcurado = input('Insira o nome do vendedor: ')
        chaveCacheVendedor = f"vendedor:nome:{dadoProcurado}"
        vendedor = obterCache(chaveCacheVendedor)
        if not vendedor: achouVendedor = buscarVendedor(dadoProcurado, 'nome', True)
        if isinstance(achouVendedor, dict): vendedor = achouVendedor
        elif not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: vendedor = buscarVendedor(input('Insira o id do vendedor: '), 'id', False)
        if not vendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        cacheResultado(chaveCacheVendedor, vendedor)
    if not vendedor.get("enderecos"):
        print("Cadastre pelo menos um endereço no vendedor antes de fazer uma compra!")
        return
    enderecosVendedor = vendedor["enderecos"]
    enderecoVendedor = None
    if len(enderecosVendedor) > 1:
        while not enderecoVendedor:
            print("De onde será enviado o produto?")
            for endereco in enderecosVendedor:
                print("================================")
                print(f'Código Endereço: {endereco["cod_endereco"]}')
                enderecoJson(endereco)
            print("================================\n")
            codigoEndereco = obterEntrada("Insira o código do endereço: ", validarNumero, "Número inválido. Deve conter apenas dígitos numéricos.")
            for i, endereco in enumerate(enderecosVendedor):
                if endereco["cod_endereco"] == int(codigoEndereco):
                    enderecoVendedor = endereco
                    break
            if not enderecoVendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
                else: continue
            break
    else: enderecoVendedor = enderecosVendedor[0]
    produtosVendedor = vendedor.get("produtos", [])
    produtos = []
    valorTotal = 0
    if len(produtosVendedor) > 1:
        while len(produtosVendedor) > 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Escolha os produtos a serem comprados:")
            for i, produto in enumerate(produtosVendedor, start=1):
                print(f"{i} - Produto {i}:")
                produtoJson(produto)
                print("---------------------------")        
            posicao = obterEntrada("Insira a posição do produto desejado: ", validarNumero, "Insira um número válido para a posição do produto!")
            posicao = int(posicao)
            if 1 <= posicao <= len(produtosVendedor):
                produtoEscolhido = produtosVendedor[posicao - 1]
                produtos.append(produtoEscolhido)
                produtosVendedor.remove(produtoEscolhido)
                valorTotal += produtoEscolhido["valor_produto"]
                if len(produtosVendedor) == 1:
                    if input("Deseja comprar o último produto? (S/N)\n").upper() == 'S':
                        produtoEscolhido = produtosVendedor[0]
                        produtos.append(produtoEscolhido)
                        produtosVendedor.remove(produtoEscolhido)
                        valorTotal += produtoEscolhido["valor_produto"]
                        break
                if input("Deseja comprar mais algum produto? (S/N)\n").upper() != 'S': break
            else: print("Posição de produto inválida!")
    elif len(produtosVendedor) == 1:
        produtos.append(produtosVendedor[0])
        valorTotal = produtosVendedor[0]["valor_produto"]
    else:
        print("Cadastre pelo menos um produto no vendedor antes de fazer uma compra!")
        return
    codCliente = cliente["_id"]
    nomeCliente = cliente["nome_usuario"]
    cpf = cliente["cpf"]
    codVendedor = vendedor["_id"]
    nomeVendedor = vendedor["nome_vendedor"]
    cnpj = vendedor["cnpj"]
    compra = {
        "data_compra": datetime.utcnow(),
        "cod_cliente": codCliente,
        "nome_cliente": nomeCliente,
        "cpf": cpf,
        "endereco_cliente": enderecoCliente,
        "cod_vendedor": codVendedor,
        "nome_vendedor": nomeVendedor,
        "cnpj": cnpj,
        "endereco_vendedor": enderecoVendedor,
        "produtos": produtos,
        "valor_total": valorTotal
    }
    try:
        compras.insert_one(compra)   
        usuarios.update_one(
            {"_id": codCliente},
            {"$push": {"compras": compra}}
        )
        vendedores.update_one(
            {"_id": codVendedor},
            {"$push": {"vendas": compra}}
        )
        for produto in produtos:
            vendedores.update_one(
                {"_id": codVendedor},
                {"$pull": {"produtos": {"_id": produto["_id"]}}}
            )        
        chave_cache_compra = f"compra:cod_cliente:{codCliente}"
        cacheResultado(chave_cache_compra, compra)
        print("Compra realizada com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar a compra: {e}")
        return
    return compra

def listarCompras(cliente=None):
    if not cliente:
        print("Usuário não autenticado!")
        return
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Listando compras...")
    compras = cliente["compras"]
    if not compras: print("Nenhuma compra encontrada neste usuário.")
    else:
        print("Compras do usuário:")
        for compra in compras:
            print("===========================================")
            comprasJson(compra,comVendedor=True)
        print("===========================================")