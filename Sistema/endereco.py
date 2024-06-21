from validacoes import validarNaoVazio, validarNumero, validarCEP
from formatacaoJson import enderecoJson

def obterEntrada(mensagem, validacao, erroMensagem):
    while True:
        entrada = input(mensagem)
        if not validacao(entrada): print(erroMensagem)
        else: return entrada

def gerarNovoCodigo(enderecos):
    cod_endereco = 0
    codigos_existentes = {endereco['cod_endereco'] for endereco in enderecos}
    while cod_endereco in codigos_existentes:
        cod_endereco += 1
    return cod_endereco

def obterEndereco(codEndereco):
    cep = obterEntrada("Insira o CEP: ", validarCEP, "CEP inválido. Deve conter 8 dígitos numéricos.")
    pais = obterEntrada("Insira o país: ", validarNaoVazio, "País não pode estar em branco.")
    estado = obterEntrada("Insira o estado: ", validarNaoVazio, "Estado não pode estar em branco.")
    cidade = obterEntrada("Insira a cidade: ", validarNaoVazio, "Cidade não pode estar em branco.")
    bairro = obterEntrada("Insira o bairro: ", validarNaoVazio, "Bairro não pode estar em branco.")
    rua = obterEntrada("Insira a rua: ", validarNaoVazio, "Rua não pode estar em branco.")
    numero = obterEntrada("Insira o número: ", validarNumero, "Número inválido. Deve conter apenas dígitos numéricos.")
    descricao = obterEntrada("Insira a descrição: ", validarNaoVazio, "Descrição não pode estar em branco.")
    endereco = {
        "cod_endereco": codEndereco,
        "cep": cep,
        "pais": pais,
        "estado": estado,
        "cidade": cidade,
        "bairro": bairro,
        "rua": rua,
        "numero": numero,
        "descricao": descricao
    }
    return endereco

def cadastrarEnderecos():
    enderecos=[]
    while True:
        codigoEndereco = gerarNovoCodigo(enderecos)
        enderecos = cadastrarEndereco(enderecos, codigoEndereco)
        if input("Deseja cadastrar mais algum endereço? (S/N)\n").upper() != 'S': break
    return enderecos

def cadastrarEndereco(enderecos, codigoEndereco):
    enderecos.append(obterEndereco(codigoEndereco))
    return enderecos

def editarEndereco(enderecos):
    codigoEndereco = obterEndereco("Insira o código do endereço: ", validarNumero, "Número inválido. Deve conter apenas dígitos numéricos.")
    for i, endereco in enumerate(enderecos):
        if endereco["cod_endereco"] == int(codigoEndereco):
            enderecos[i] = obterEndereco(endereco["cod_endereco"])
            return enderecos
    print("O código inserido não foi encontrado!")
    return enderecos

def excluirEndereco(enderecos):
    codigoEndereco = obterEntrada("Insira o código do endereço: ", validarNumero, "Número inválido. Deve conter apenas dígitos numéricos.")
    for i, endereco in enumerate(enderecos):
        if endereco["cod_endereco"] == int(codigoEndereco):
            del enderecos[i]
            print("Endereço excluído com sucesso!")
            return enderecos
    print("O código inserido não foi encontrado!")
    return enderecos

def gerenciarEnderecos(enderecos):
    print("Endereços Atuais:")
    if not enderecos: print("Nenhum endereço cadastrado!")
    else:
        for endereco in enderecos:
            print("================================")
            print(f'Código Endereço: {endereco["cod_endereco"]}')
            enderecoJson(endereco)
        print("================================\n")
    print('O que deseja fazer com os endereços?')
    print("--------------------------------")
    print('1 - Criar um novo endereço')
    if enderecos:
        print('2 - Editar um endereço existente')
        print('3 - Deletar um endereço existente')
    print("--------------------------------")
    print('0 - Voltar')
    print("================================")
    opcao = obterEntrada("Insira a opção desejada: ", validarNumero, "Opção inválida. Deve conter apenas dígitos numéricos.")
    if opcao == "1": return cadastrarEndereco(enderecos, gerarNovoCodigo(enderecos))
    elif opcao == "2" and enderecos: return editarEndereco(enderecos)
    elif opcao == "3" and enderecos: return excluirEndereco(enderecos)
    elif opcao != "0": print('Opção inválida.')
    return enderecos