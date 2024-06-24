def enderecoJson(arquivoJson):
    if "rua" in arquivoJson and "numero" in arquivoJson and "descricao" in arquivoJson and "bairro" in arquivoJson:
        print(f'{arquivoJson["rua"]}, {arquivoJson["numero"]} ({arquivoJson["descricao"]}) - {arquivoJson["bairro"]}')
    if "cidade" in arquivoJson and "estado" in arquivoJson and "pais" in arquivoJson:
        print(f'{arquivoJson["cidade"]} - {arquivoJson["estado"]} ({arquivoJson["pais"]})')
    if "cep" in arquivoJson:
        print(f'CEP: {formatar_cep(arquivoJson["cep"])}')

def produtoJson(arquivoJson, comCodigo=False, comVendedor=False):
    if comCodigo and "_id" in arquivoJson: print(f'Id: {arquivoJson["_id"]}')
    if "nome_produto" in arquivoJson: print(f'Produto: {arquivoJson["nome_produto"]}')
    if "valor_produto" in arquivoJson: print(f'Valor: R${arquivoJson["valor_produto"]:.2f}')
    if comVendedor and "nome_vendedor" in arquivoJson: print(f'Vendedor: {arquivoJson["nome_vendedor"]}')
    if comVendedor and "cnpj" in arquivoJson: print(f'CNPJ: {arquivoJson["cnpj"]}')

def vendedorJson(arquivoJson, comCodigo=False):
    if comCodigo and "_id" in arquivoJson: print(f'Id: {arquivoJson["_id"]}')
    if "nome_vendedor" in arquivoJson: print(f'Nome: {arquivoJson["nome_vendedor"]}')
    if "cnpj" in arquivoJson: print(f'CNPJ: {formatar_cnpj(arquivoJson["cnpj"])}')
    if "email_vendedor" in arquivoJson: print(f'Email: {arquivoJson["email_vendedor"]}')
    if "telefone_vendedor" in arquivoJson: print(f'Telefone: {formatar_telefone(arquivoJson["telefone_vendedor"])}')
    if "enderecos" in arquivoJson:
        count = 0
        for endereco in arquivoJson["enderecos"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Endereco:')
            enderecoJson(endereco)
    if "produtos" in arquivoJson:
        count = 0
        for produto in arquivoJson["produtos"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Produto:')
            produtoJson(produto, False)
    if "vendas" in arquivoJson:
        count = 0
        for venda in arquivoJson["vendas"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Venda:')
            comprasJson(venda, True, False, comCodigo)
    if "enderecos" in arquivoJson or "produtos" in arquivoJson or "vendas" in arquivoJson: print("-----------------------------------------------")


def usuarioJson(arquivoJson, comCodigo=False):
    if comCodigo and "_id" in arquivoJson: print(f'Id: {arquivoJson["_id"]}')
    if "nome_usuario" in arquivoJson: print(f'Nome: {arquivoJson["nome_usuario"]}')
    if "cpf" in arquivoJson: print(f'CPF: {formatar_cpf(arquivoJson["cpf"])}')
    if "email_usuario" in arquivoJson: print(f'Email: {arquivoJson["email_usuario"]}')
    if "telefone_usuario" in arquivoJson: print(f'Telefone: {formatar_telefone(arquivoJson["telefone_usuario"])}')
    if "enderecos" in arquivoJson:
        count = 0
        for endereco in arquivoJson["enderecos"]:
            count += 1
            print("-----------------------------------------------")
            print(f'{count}º Endereço:')
            enderecoJson(endereco)
    if "favoritos" in arquivoJson:
        count1 = 0
        for produto in arquivoJson["favoritos"]:
            count1 += 1
            print("-----------------------------------------------")
            print(f'{count1}º Produto Favorito:')
            produtoJson(produto, False)
    if "compras" in arquivoJson:
        count2 = 0
        for compra in arquivoJson["compras"]:
            count2 += 1
            print("-----------------------------------------------")
            print(f'{count2}º Compra:')
            comprasJson(compra, False, True, comCodigo)
    if "enderecos" in arquivoJson or "favoritos" in arquivoJson: print("-----------------------------------------------")
        
def comprasJson(arquivoJson, comCliente=False, comVendedor=False, comCodigo=False):
    print("Data da Compra:", arquivoJson.get("data_compra"))
    if comCliente:
        if comCodigo: print("Código do Cliente:", arquivoJson.get("cod_cliente"))
        print("Nome do Cliente:", arquivoJson.get("nome_cliente"))
        print("CPF do Cliente:", arquivoJson.get("cpf"))
        print("Endereço do Cliente:")
        enderecoJson(arquivoJson.get("endereco_cliente"))
    if comVendedor:
        if comCodigo: print("Código do Vendedor:", arquivoJson.get("cod_vendedor"))
        print("Nome do Vendedor:", arquivoJson.get("nome_vendedor"))
        print("CNPJ do Vendedor:", arquivoJson.get("cnpj"))
        print("Endereço do Vendedor:")
        enderecoJson(arquivoJson.get("endereco_vendedor"))
    print("Produtos:")
    for produto in arquivoJson.get("produtos", []): produtoJson(produto)
    print("Valor Total:", arquivoJson.get("valor_total"))
    
def formatar_telefone(telefone):
    if len(telefone) == 8: return f'{telefone[0:4]}-{telefone[4:8]}'
    if len(telefone) == 9: return f'{telefone[0:5]}-{telefone[5:9]}'
    if len(telefone) == 10: return f'({telefone[0:2]}) {telefone[2:6]}-{telefone[6:10]}'
    if len(telefone) == 11: return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}'
    else: return telefone

def formatar_cpf(cpf):
    if len(cpf) == 11: return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    else: return cpf

def formatar_cnpj(cnpj):
    if len(cnpj) == 14: return f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    else: return cnpj
    
def formatar_cep(cep):
    if len(cep) == 8: return f'{cep[0:5]}-{cep[5:9]}'
    else: return cep