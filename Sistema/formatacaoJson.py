def enderecoJson(arquivoJson):
    if "rua" in arquivoJson and "numero" in arquivoJson and "descricao" in arquivoJson and "bairro" in arquivoJson:
        print(f'{arquivoJson["rua"]}, {arquivoJson["numero"]} ({arquivoJson["descricao"]}) - {arquivoJson["bairro"]}')
    if "cidade" in arquivoJson and "estado" in arquivoJson and "pais" in arquivoJson:
        print(f'{arquivoJson["cidade"]} - {arquivoJson["estado"]} ({arquivoJson["pais"]})')
    if "cep" in arquivoJson:
        print(f'CEP: {arquivoJson["cep"]}')

def produtoJson(arquivoJson, comVendedor):
    if comVendedor:
        if "nome_vendedor" in arquivoJson:
            print(f'Vendedor: {arquivoJson["nome_vendedor"]}')
        if "cnpj_vendedor" in arquivoJson:
            print(f'CNPJ: {arquivoJson["cnpj"]}')
    if "nome_produto" in arquivoJson:
        print(f'Produto: {arquivoJson["nome_produto"]}')
    if "valor_produto" in arquivoJson:
        print(f'Valor: R${arquivoJson["valor_produto"]:.2f}')

def vendedorJson(arquivoJson):
    if "nome_vendedor" in arquivoJson: print(f'Nome: {arquivoJson["nome_vendedor"]}')
    if "cnpj" in arquivoJson: print(f'CPF: {arquivoJson["cnpj"]}')
    if "email_vendedor" in arquivoJson: print(f'Emai: {arquivoJson["email_vendedor"]}')
    if "telefone_vendedor" in arquivoJson: print(f'Telefone: {arquivoJson["telefone_vendedor"]}')
    if "enderecos" in arquivoJson:
        count = 0
        for endereco in arquivoJson["enderecos"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Endereco:')
            enderecoJson(endereco)
    if "produtos" in arquivoJson:
        count1 = 0
        for produto in arquivoJson["produtos"]:
            count1 += 1
            print("-----------------------------------------------")
            print(f'{count1}º Produto:')
            produtoJson(produto, False)
    if count != 0 or count1 != 0: print("-----------------------------------------------")

def usuarioJson(arquivoJson):
    if "nome_usuario" in arquivoJson: print(f'Nome: {arquivoJson["nome_usuario"]}')
    if "cpf" in arquivoJson: print(f'CPF: {arquivoJson["cpf"]}')
    if "email_usuario" in arquivoJson: print(f'Emai: {arquivoJson["email_usuario"]}')
    if "telefone_usuario" in arquivoJson: print(f'Telefone: {arquivoJson["telefone_usuario"]}')
    if "enderecos" in arquivoJson:
        count = 0
        for endereco in arquivoJson["enderecos"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Endereco:')
            enderecoJson(endereco)
    if "favoritos" in arquivoJson:
        count1 = 0
        for produto in arquivoJson["favoritos"]:
            count1 += 1
            print("-----------------------------------------------")
            print(f'{count1}º produto favorito:')
            produtoJson(produto, True)
    if count != 0 or count1 != 0: print("-----------------------------------------------")
    
def comprasJson(arquivoJson, comCliente, comVendedor):
    if comCliente:
        if "nome_usuario" in arquivoJson: print(f'Nome: {arquivoJson["nome_usuario"]}')
        if "cpf" in arquivoJson: print(f'Nome: {arquivoJson["cpf"]}')
        if "endereco_usuario" in arquivoJson:
            print("Endereco Usuário:")
            enderecoJson(arquivoJson["endereco_cliente"])
    if comVendedor:
        if "nome_vendedor" in arquivoJson: print(f'Nome: {arquivoJson["nome_vendedor"]}')
        if "cnpj" in arquivoJson: print(f'Nome: {arquivoJson["cnpj"]}')
        if "endereco_vendedor" in arquivoJson:
            print("Endereco Vendedor:")
            enderecoJson(arquivoJson["endereco_vendedor"])
    produtosVendidos=[*arquivoJson["produtos"]]
    if len(produtosVendidos)==1:
        print("Produto:")
        print("-----------------------------------------------")
        produtoJson(produtosVendidos[0])
        print("-----------------------------------------------")
    else:
        print("Produtos vendidos:")
        for produto in produtosVendidos:
            print("-----------------------------------------------")
            produtoJson(produto)
        print("-----------------------------------------------")
    if "promocao" in arquivoJson:
        print(f'Valor promoção: {arquivoJson["promocao"]}')
    if "valor_total" in arquivoJson:
        print(f'Valor total: {arquivoJson["valor_total"]}')