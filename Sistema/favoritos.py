from formatacaoJson import produtoJson
from busca import buscarProduto
from bson.objectid import ObjectId

# GERENCIAR FAVORITOS:
def gerenciarFavoritos(favoritos):
    favoritos = [*favoritos]
    print("Favoritos Atuais:")
    if len(favoritos) == 0: print("Nenhum produto nos favoritos!")
    else:
        for favorito in favoritos:
            print("================================")
            produtoJson(favorito, True)
        print("================================")
    print('O que deseja fazer com os favoritos?')
    print('1 - Adicionar um produto')
    if len(favoritos) != 0:
        print('2 - Remover um produto')
    print('0 - Voltar')
    opcao = input('Insira a opção desejada: ')
    if opcao == "0": return favoritos
    elif opcao == "1": return adicionarFavorito(favoritos)
    elif len(favoritos) != 0:
        if opcao == "2": return removerFavorito(favoritos)
    print('Comando incorreto! :(')
    return favoritos

def adicionarFavorito(favoritos):
    while True:
        achouProduto = buscarProduto(input("Insira o nome do produto desejado:"), "nome", True, True)
        if not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
        elif not isinstance(achouProduto, dict):
            while True:
                produto = buscarProduto(input("Insira o id do produto desejado: "), "id", False, False)
                if produto == None:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                    else: return favoritos
                favoritos.append(produto)
                break
        else: favoritos.append(achouProduto)
        break
    return favoritos

def removerFavorito(favoritos):
    ids = [favorito["_id"] for favorito in favoritos]
    for favorito in favoritos:
        print(f'Id: {favorito["_id"]}')
        produtoJson(favorito, True)
    while True:
        try:
            idProduto = ObjectId(input("Insira o ID do produto desejado para remoção: "))
            if idProduto not in ids:
                print("O ID inserido não corresponde a nenhum produto na lista de favoritos. Tente novamente.")
                continue
            else:
                favoritos = [favorito for favorito in favoritos if favorito["_id"] != idProduto]
                print("Produto removido com sucesso da lista de favoritos.")
                break
        except Exception as e:
            print("Erro ao processar a entrada. Certifique-se de inserir um ID válido.")
            print(e)
            continue
    return favoritos