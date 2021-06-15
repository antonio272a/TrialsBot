import pyrez


class SmiteApi:
    """
        PT-BR: Classe usada para acessar a API do Smite através do wrapper Pyrez.
        Obs.: nunca instancie os champions ou itens no construtor da classe, isso atrasa desnecessáriamente qualquer
        outro comando além do ".image"
        Obs.2: Os comandos para retornar os gods e os itens tem a conferência com o if pois eventualmente eles podem
        retornar vazios por erro na API, gerando um erro no bot.

        EN-US: Class used to access the Smite API through the Pyrez wrapper.
        Note: never instantiate champions or items in the class constructor, this unnecessarily delays any
        another command besides ".image"
        Note 2: The commands to return the gods and items have the check with the if because eventually they can
        return empty by error on the API, generating an error on the bot.

        https://github.com/luissilva1044894/Pyrez
        """

    def __init__(self):
        self._dev_id_hirez = "3656"
        self._auth_key_hirez = "310114B6E36447369BBD3F35034995AC"
        self._smite_req = pyrez.SmiteAPI(devId=self._dev_id_hirez, authKey=self._auth_key_hirez)

    def get_match_inf(self, match_id):
        return self._smite_req.getMatch(match_id)

    def get_player_id_by_name(self, player_name):
        return self._smite_req.getPlayerId(player_name)

    def get_gods(self):
        gods = self._smite_req.getGods()
        if not gods:
            self.get_gods()
        else:
            return gods

    def get_itens(self):
        itens = self._smite_req.getItems()
        if not itens:
            self.get_itens()
        else:
            return itens
