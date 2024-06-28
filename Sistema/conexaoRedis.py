import redis
import json
from bson import ObjectId
from datetime import datetime

def conectarRedis():
    cliente = redis.Redis(
        host='LINK HOST REDIS',
        port='PORTA REDIS',
        password='SENHA REDIS'
    )
    return cliente

def cacheResultado(chave, resultado):
    cliente = conectarRedis()  
    dadoJson = json.dumps(resultado, default=converterParaJson)
    cliente.set(chave, dadoJson)

def obterCache(chave):
    cliente = conectarRedis()
    resultado = cliente.get(chave)
    return json.loads(resultado, object_hook=converterParaObjeto) if resultado else None

def converterParaJson(objeto):
    if isinstance(objeto, ObjectId): return str(objeto)
    elif isinstance(objeto, datetime): return objeto.isoformat()
    else: raise TypeError(f"Objeto do tipo {type(objeto)} não é serializável.")

def converterParaObjeto(dicionario):
    for chave, valor in dicionario.items():
        if isinstance(valor, str):
            try: dicionario[chave] = datetime.fromisoformat(valor)
            except ValueError: pass
    return dicionario