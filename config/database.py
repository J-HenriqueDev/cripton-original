from pymongo import MongoClient
from config import secrets


try:
 client = MongoClient(secrets.MONGO_URI)
 db = client.cryptobeta.guilds
 newdb = client.cryptobeta.new
 client.server_info()
 print('DATABASE [mongodb] CONECTADA')
except Exception as e:
 print(f'DATABASE [mongodb] ERROR: {e}')

def novo_usuario(membro_id):
    """ Vai criar um novo usário. """
    user = {
        'id': membro_id,
        'reputacao':0
    }
    return newdb.insert_one(user)


def verificar(usuario_id):
    """ Vai verificar se o usuário já está salvo, se não vai chamar o função novo_usuario() e cria um novo registro."""
    _user = newdb.find_one({'id':usuario_id})
    if _user == None:
        novo_usuario(usuario_id)
    else:
        return True

def setar_reputacao(usuario_id,pontos_rep):
    """ Vai setar os pontos do usário. O operado $set é do mongodb para reescrever.
       Parâmetros:
           usuario_id : o id do usário do servidor, tem que ser int.
    """
    user = {
        'id':usuario_id
    }
    reps = {
       "$set":{
           "reputacao":pontos_rep
       }
    }
    return newdb.update_one(user,reps)

def buscar(usuario_id,chave):
    """ Para buscar o usuario.
        Parâmetros:
           usuario_id : o id do usário do servidor, tem que ser int.
           chave : o valor de busca no banco no momento moedas ou reputação tem que ser string.
           exemplo: buscar(id,"coins")
    """
    _user = newdb.find_one({'id':usuario_id})
    _buscar = _user[f'{chave}']
    if _buscar == None:
        return False
    else:
        return _buscar

def criar_server(guild_id: int):
     db.insert_one({'id': guild_id,
                    'channel': None,
                    'toggle': False,
                    'mute_role':None,
                    'dj_role':None,
                    'prefixo':"c."})

def verificar_server(guild_id):
    guild = db.find_one({'id':guild_id})
    if guild ==None:
        criar_server(guild_id)
        return guild
    else:
        return True


def setar_canal(guild_id: int, canal_id: int):
     db.update_one({'id': guild_id}, {'$set': {'channel': canal_id}})
     return True

def ativar_togle(guild_id:int,ativado:bool):
    db.update_one({'id':guild_id},{'$set':{'toggle':ativado}})
    return True

def buscar_togle(guild_id):
    guild =db.find_one({'id':guild_id})
    togle = guild['toggle']
    return togle

def buscar_prefixo(guild_id):
    _guild = db.find_one({'id':guild_id})
    if _guild == None:
        return "c."
    else:
      _prefixo = _guild['prefixo']
      return _prefixo

def setar_prefixo(guild_id,novo_prefixo:str):
    _guild = db.find_one({'id': guild_id})
    if _guild == None:
        criar_server(guild_id)
        db.update_one({'id': guild_id}, {'$set': {'prefixo': novo_prefixo}})
        return False
    else:
      db.update_one({'id': guild_id}, {'$set': {'prefixo': novo_prefixo}})
      return True


def set_mute_role(server_id: int, role_id: int):
    db.update_one({'id': server_id}, {'$set': {'mute_role': role_id}})
    return True


def get_mute_role(server_id: int):
    try:
        gg = db.find_one({'id': server_id})
        op = gg['mute_role']
        return op
    except:
        return None

def set_dj_role(server_id: int, role_id: int):
    db.update_one({'id': server_id}, {'$set': {'dj_role': role_id}})
    return True


def get_dj_role(server_id: int):
    try:
        gg = db.find_one({'id': server_id})
        op = gg['dj_role']
        return op
    except:
        return None