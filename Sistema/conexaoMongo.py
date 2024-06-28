import pymongo

def conectar():
    cliente = pymongo.MongoClient(
        "LINK SERVER MONGO"
    )
    return cliente.Mercado_Livre