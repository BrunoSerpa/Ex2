from produtos import buscarProduto, produtoJson
from bson.objectid import ObjectId

# GERENCIAR FAVORITOS:
def gerenciarFavoritos(favoritos):
    count = 0
    print("Favoritos Atuais:")
    if not favoritos: print("Nenhum produto nos favoritos!")
    else:
        for favorito in favoritos:
            count+=1
            print("================================")
            if "cod_produto" in favorito:
                print(f'Código Produto: {favorito["cod_produto"]}')
            produtoJson(favorito)
        print("================================")
    print('O que deseja fazer com os favoritos?')
    print('1 - Adicionar um produto')
    if favoritos:
        print('2 - Remover um produto')
    print('0 - Voltar')
    opcao = int(input('Insira a opção desejada: '))
    if opcao == 0:
        return favoritos
    elif opcao == 1:
        return adicionarFavorito(favoritos)
    elif favoritos and opcao == 2:
        return removerFavorito(favoritos)
    print('Comando incorreto! :(')
    return favoritos

def adicionarFavorito(favoritos):
    buscarProduto(input("Insira o nome do produto desejado:"), "nome", True)
    novoFavorito = buscarProduto(input("Insira o codigo do produto desejado:"), "id", False)
    if novoFavorito:
        if favoritos:
            favoritos.append(novoFavorito)
        else:
            favoritos=[novoFavorito]
    return favoritos

def removerFavorito(favoritos):
    ids = []
    for favorito in favoritos:
        if "_id" in favorito:
            print(f'Id: {favorito["_id"]}')
            ids.append(favorito["_id"])
        produtoJson(favorito)
    idProduto = ObjectId(input("Insira o id do produto desejado:"))
    if idProduto in ids:
        favoritos = [favorito for favorito in favoritos if favorito["_id"] != idProduto]
    return favoritos