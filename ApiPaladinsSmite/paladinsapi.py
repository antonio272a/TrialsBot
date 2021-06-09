import pyrez


class PaladinsApi:

    def __init__(self):
        self._dev_id_hirez = "3656"
        self._auth_key_hirez = "310114B6E36447369BBD3F35034995AC"
        self._paladins_req = pyrez.PaladinsAPI(devId=self._dev_id_hirez, authKey=self._auth_key_hirez)
        self._call_default_requests()

    def _call_default_requests(self):
        self.champions = self._paladins_req.getChampions()
        self.itens = self._paladins_req.getItems()
        if not self.champions or not self.itens:
            self._call_default_requests()

    def get_match_inf(self, match_id):
        return self._paladins_req.getMatch(match_id)

    def get_player_id_by_name(self, player_name):
        return self._paladins_req.getPlayerId(player_name)

    def get_champions(self):
        return self.champions

    def get_itens(self):
        return self.itens