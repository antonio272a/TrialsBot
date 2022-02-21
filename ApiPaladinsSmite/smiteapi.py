import pyrez
import os


dev_id_hirez = os.environ.get('HIREZ_DEV_ID')
auth_key_hirez = os.environ.get('HIREZ_AUTH_KEY')
smite_req = pyrez.SmiteAPI(devId=dev_id_hirez, authKey=auth_key_hirez)


def get_match_inf(match_id: str):
    return smite_req.getMatch(match_id)


def get_player_id_by_name(player_name: str):
    return smite_req.getPlayerId(player_name)


def get_gods():
    gods = smite_req.getGods()
    if not gods:
        get_gods()
    else:
        return gods


def get_itens():
    itens = smite_req.getItems()
    if not itens:
        get_itens()
    else:
        return itens
