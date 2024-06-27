from usuario import cadastrarUsuario, atualizarUsuario
from favoritos import gerenciarFavoritos
from busca import buscarUsuario
from compras import fazerCompra, listarCompras
from validacoes import validarNaoVazio
import os

usuarioAtual = None

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
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Insira uma das opções!")
            continue
        if opcao == "0": break
        try:
            opcaoIndex = int(opcao) - 1
            if 0 <= opcaoIndex < len(opcoes):
                os.system('cls' if os.name == 'nt' else 'clear')
                if usuarioAtual: opcoes[opcaoIndex]['acao'](usuarioAtual)
                else:
                    opcoes[opcaoIndex]['acao']()
            else:
                print("Opção inválida!")
        except ValueError:
            print("Opção inválida!")

def menuUsuario():
    opcoes = [
        {"descricao": "Atualizar Dados", "acao": atualizarUsuario},
        {"descricao": "Meus Favoritos", "acao": gerenciarFavoritos},
        {"descricao": "Minhas compras", "acao": listarCompras},
        {"descricao": "Fazer compra", "acao": fazerCompra},
    ]
    exibirMenu(opcoes, "Gerenciar Usuários")

def login():
    global usuarioAtual
    while not usuarioAtual:
        nome_usuario = input('Insira o nome do usuário desejado: ')
        achouUsuario = buscarUsuario(nome_usuario, 'nome', True)
        if not achouUsuario:
            resposta = input("Nenhum usuário encontrado. Deseja procurar novamente? (S/N)\n")
            if resposta.upper() != 'S': return
        elif isinstance(achouUsuario, dict): usuarioAtual = achouUsuario
        else:
            id_usuario = input('Insira o ID do usuário desejado: ')
            usuario = buscarUsuario(id_usuario, 'id', False)
            if not usuario:
                resposta = input("Usuário não encontrado. Deseja procurar novamente? (S/N)\n")
                if resposta.upper() != 'S': return
            else: usuarioAtual = usuario
    menuUsuario()

def home():
    opcoes = [
        {"descricao": "Login", "acao": login},
        {"descricao": "Cadastar usuario", "acao": cadastrarUsuario},
    ]
    exibirMenu(opcoes, "Menu Principal")

if __name__ == "__main__": home()