import re

def validarCPF(cpf):
    if not cpf.isnumeric() or len(cpf) != 11: return False
    def calcular_digito(cpf, posicoes):
        soma = 0
        for i, digito in enumerate(cpf[:posicoes]): soma += int(digito) * (posicoes + 1 - i)
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    return cpf[-2] == calcular_digito(cpf, 9) and cpf[-1] == calcular_digito(cpf, 10)

def validarCNPJ(cnpj):
    if not cnpj.isnumeric() or len(cnpj) != 14: return False
    def calcular_digito(cnpj, multiplicadores):
        soma = 0
        for i, multiplicador in enumerate(multiplicadores): soma += int(cnpj[i]) * multiplicador
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    multiplicadores_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multiplicadores_2 = [6] + multiplicadores_1
    return (cnpj[-2] == calcular_digito(cnpj, multiplicadores_1) and cnpj[-1] == calcular_digito(cnpj, multiplicadores_2))
def validarEmail(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None
def validarTelefone(telefone):
    regex = r'^\d{8,}$'
    return re.match(regex, telefone) is not None

def validarCEP(cep):
    if not cep.isnumeric() or len(cep) != 8: return False
    return True

def validarNaoVazio(valor): return bool(valor.strip())

def validarNumero(numero): return numero.isnumeric()

def validarFloat(numero):
    try:
        float(numero)
        return True
    except ValueError: return False