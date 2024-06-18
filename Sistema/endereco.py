# VALIDAÇÕES
from validacoes import validarNaoVazio, validarNumero

from formatacaoJson import enderecoJson

# FUNÇÃO OBTER ENDEREÇO
def obterEndereco(cod_endereco):
    endereco = {
        "cod_endereco": cod_endereco,
        "cep": input("Insira o CEP: "),
        "pais": input("Insira o país: "),
        "estado": input("Insira o estado: "),
        "cidade": input("Insira a cidade: "),
        "bairro": input("Insira o bairro: "),
        "rua": input("Insira a rua: "),
        "numero": input("Insira o número: "),
        "descricao": input("Insira a descrição: ")
    }
    return endereco if all(validarNaoVazio(str(valor)) for valor in endereco.values()) else None


# FUNÇÃO CADASTRAR ENDEREÇOS
def cadastrarEnderecos():
    enderecos = []
    while True:
        endereco = obterEndereco(len(enderecos))
        if endereco:
            enderecos.append(endereco)
        else:
            count-=1
            print("Todos os campos do endereço devem ser preenchidos.")
        if input("Deseja cadastrar mais algum endereço? (S/N)\n").upper() != 'S':
            break
    return enderecos

# FUNÇÃO CADASTRAR NOVO ENDEREÇO
def cadastrarEndereco(enderecos, idEndereco):
    endereco = obterEndereco(idEndereco)
    if endereco:
        enderecos.append(endereco)
    else:
        print("Todos os campos do endereço devem ser preenchidos.")
    return enderecos

# FUNÇÃO EDITAR ENDEREÇO
def editarEndereco(enderecos):
    codigoEndereco = obterCodigoEndereco()
    if not codigoEndereco: return enderecos
    achou = False
    novosEnderecos = []
    for endereco in enderecos:
        if endereco["cod_endereco"] == codigoEndereco:
            achou = True
            novoEndereco = obterEndereco(codigoEndereco)
            if novoEndereco: endereco = novoEndereco
            else: print("Todos os campos do endereço devem ser preenchidos.")
        novosEnderecos.append(endereco)
    if not achou: print("o código inserido não foi encontrado!.")
    return novosEnderecos

# FUNÇÃO EXCLUIR ENDEREÇO
def excluirEndereco(enderecos):
    codigoEndereco = obterCodigoEndereco()
    if not codigoEndereco: return enderecos
    enderecoExcluido  = False
    for endereco in enderecos:
        if endereco["cod_endereco"] == codigoEndereco:
            enderecos.remove(endereco)
            print("Endereço excluído com sucesso!")
            enderecoExcluido = True
            continue
    if not enderecoExcluido: print("o código inserido não foi encontrado.")
    return enderecos

        
# GERENCIAR ENDEREÇOS:
def gerenciarEnderecos(enderecos):
    enderecos = [*enderecos]
    print("Endereços Atuais:")
    if len(enderecos) == 0: print("Nenhum endereço cadastrado!")
    else:
        for endereco in enderecos:
            print("================================")
            print(f'Código Endereço: {endereco["cod_endereco"]}')
            enderecoJson(endereco)
        print("================================")
    print('O que deseja fazer com os endereços?')
    print('1 - Criar um novo endereço')
    if len(enderecos) != 0:
        print('2 - Editar um endereço existente')
        print('3 - Deletar um endereço existente')
    print('0 - Voltar')
    opcao = input('Insira a opção desejada: ')
    if opcao == "0": return enderecos
    elif opcao == "1": return cadastrarEndereco(enderecos, len(enderecos))
    elif enderecos:
        if opcao == "2":
            return editarEndereco(enderecos)
        elif opcao == "3":
            return excluirEndereco(enderecos)
    print('Comando incorreto! :(')
    return enderecos