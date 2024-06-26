from formatacaoJson import produtoJson
from busca import buscarProduto
from bson.objectid import ObjectId

def exibirFavoritos(favoritos):
    if not favoritos:
        print("Nenhum produto nos favoritos!")
    else:
        for favorito in favoritos:
            print("================================")
            produtoJson(favorito, True, True)
        print("================================")

def obterIdProduto(prompt):
    while True:
        try:
            return ObjectId(input(prompt))
        except Exception as e:
            print("Erro ao processar a entrada. Certifique-se de inserir um ID válido.")
            print(e)

def gerenciarFavoritos(cliente=None):
    if not cliente:
        print("Usuário não autenticado!")
        return
    favoritos = cliente["favoritos"]
    print("Favoritos Atuais:")
    exibirFavoritos(favoritos)
    
    print('O que deseja fazer com os favoritos?')
    print('1 - Adicionar um produto')
    if favoritos:
        print('2 - Remover um produto')
    print('0 - Voltar')
    
    opcao = input('Insira a opção desejada: ')
    if opcao == "0": 
        return favoritos
    elif opcao == "1": 
        return adicionarFavorito(favoritos)
    elif opcao == "2" and favoritos: 
        return removerFavorito(favoritos)
    
    print('Comando incorreto! :(')
    return favoritos

def adicionarFavorito(favoritos):
    while True:
        achouProduto = buscarProduto(input("Insira o nome do produto desejado: "), "nome", True, True)
        if not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S':
                continue
        elif isinstance(achouProduto, dict):
            favoritos.append(achouProduto)
        else:
            produto = buscarProduto(input("Insira o id do produto desejado: "), "id", False, True)
            if produto:
                favoritos.append(produto)
            else:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S':
                    continue
                return favoritos
        break
    return favoritos

def removerFavorito(favoritos):
    exibirFavoritos(favoritos)
    idProduto = obterIdProduto("Insira o ID do produto desejado para remoção: ")
    for favorito in favoritos:
        if favorito["_id"] == idProduto:
            favoritos.remove(favorito)
            print("Produto removido com sucesso da lista de favoritos.")
            return favoritos
    print("O ID inserido não corresponde a nenhum produto na lista de favoritos.")
    return favoritos