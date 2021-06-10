import pyrez


class PaladinsApi:

    def __init__(self):
        self._dev_id_hirez = "3656"
        self._auth_key_hirez = "310114B6E36447369BBD3F35034995AC"
        self._paladins_req = pyrez.PaladinsAPI(devId=self._dev_id_hirez, authKey=self._auth_key_hirez)

    def get_match_inf(self, match_id):
        return self._paladins_req.getMatch(match_id)

    def get_player_id_by_name(self, player_name):
        return self._paladins_req.getPlayerId(player_name)

    def get_champions(self):
        champions = self._paladins_req.getChampions()
        if not champions:
            self.get_champions()
        else:
            return champions

    def get_itens(self):
        itens = self._paladins_req.getItems()
        if not itens:
            self.get_itens()
        else:
            return itens
