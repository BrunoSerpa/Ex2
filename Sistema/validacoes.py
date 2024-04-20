# FUNÇÕES DE VALIDAÇÃO
def validarCPF(cpf):
    if len(cpf) != 11 or not cpf.isnumeric():
        return False
    return True

def validarEmail(email):
    if '@' not in email and '.' not in email:
        return False
    return True

def validarTelefone(telefone):
    if not telefone.isnumeric() or len(telefone) < 8:
        return False
    return True

def validarNaoVazio(valor):
    if not valor.strip():
        return False
    return True

def validarNumero(numero):
    if not numero.isnumeric():
        return False
    return True