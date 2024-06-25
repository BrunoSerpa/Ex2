from usuario import cadastrarUsuario, atualizarUsuario, deletarUsuario
from compras import fazerCompra, listarCompras
from validacoes import validarNaoVazio
import os

def exibirMenu(opcoes, titulo="Menu"):
    while True:
        print("================================")
        print(f"{titulo}")
        print("--------------------------------")
        for i, opcao in enumerate(opcoes, start=1): print(f"{i} - {opcao['descricao']}")
        print("--------------------------------")
        print("0 - Voltar")
        print("================================")
        opcao = input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            os.system('cls')
            print("Insira uma das opções!")
            continue
        if opcao == "0": break
        try:
            opcaoIndex = int(opcao) - 1
            if 0 <= opcaoIndex < len(opcoes):
                os.system('cls')
                opcoes[opcaoIndex]['acao']()
            else: print("Opção inválida!")
        except ValueError: print("Opção inválida!")
def menuUsuario():
    opcoes = [
        {"descricao": "Cadastar compra", "acao": fazerCompra},
        {"descricao": "Listar compras", "acao": listarCompras},
        {"descricao": "Atualizar usuario", "acao": atualizarUsuario},
        {"descricao": "Deletar usuario", "acao": deletarUsuario}
    ]
    exibirMenu(opcoes, "Gerenciar Usuários")
def home():
    opcoes = [
        {"descricao": "Gerenciar Usuarios", "acao": menuUsuario},
        {"descricao": "Cadastar usuario", "acao": cadastrarUsuario},
    ]
    exibirMenu(opcoes, "Menu Principal")

if __name__ == "__main__": home()