import pyrez
import os


dev_id_hirez = os.environ.get('HIREZ_DEV_ID')
auth_key_hirez = os.environ.get('HIREZ_AUTH_KEY')
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
