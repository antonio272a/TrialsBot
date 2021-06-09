import pyrez


class SmiteApi:

    def __init__(self):
        self._dev_id_hirez = "3656"
        self._auth_key_hirez = "310114B6E36447369BBD3F35034995AC"
        self._smite_req = pyrez.SmiteAPI(devId=self._dev_id_hirez, authKey=self._auth_key_hirez)
        self._call_default_requests()

    def _call_default_requests(self):
        self.gods = self._smite_req.getGods()
        self.itens = self._smite_req.getItems()
        if not self.gods or not self.itens:
            self._call_default_requests()

    def get_match_inf(self, match_id):
        return self._smite_req.getMatch(match_id)

    def get_player_id_by_name(self, player_name):
        return self._smite_req.getPlayerId(player_name)

    def get_gods(self):
        return self.gods

    def get_itens(self):
        return self.itens