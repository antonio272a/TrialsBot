import pyrez
import discord
from ApiPaladinsSmite.images import ImgSmite


def get_hirez_auth_key():
    with open('./Docs/ApiTokens/hirezApiToken.txt', 'r') as f:
        return f.readline()


dev_id_hirez = "3656"
auth_key_hirez = get_hirez_auth_key()
smite_req = pyrez.SmiteAPI(devId=dev_id_hirez, authKey=auth_key_hirez)


def get_match_inf(match_id):
    return smite_req.getMatch(match_id)


def get_player_id_by_name(player_name):
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
