import pyrez
import discord
from ApiPaladinsSmite.images import ImgPaladins
import os




def get_hirez_auth_key():
    with open('./Docs/ApiTokens/hirezApiToken.txt', 'r') as f:
        return f.readline()


dev_id_hirez = "3656"
auth_key_hirez = get_hirez_auth_key()
paladins_req = pyrez.PaladinsAPI(devId=dev_id_hirez, authKey=auth_key_hirez)


def get_match_inf(match_id):
    return paladins_req.getMatch(match_id)


def request_player_id_by_name(player_name):
    player = paladins_req.getPlayerId(player_name)[0]
    return f"Nick: {player['Name']} - Id: {player['player_id']}  "


def get_champions():
    champions = paladins_req.getChampions()
    if not champions:
        get_champions()
    else:
        return champions


def get_itens():
    itens = paladins_req.getItems()
    if not itens:
        get_itens()
    else:
        return itens
