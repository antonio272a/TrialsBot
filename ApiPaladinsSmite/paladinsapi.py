import pyrez


class PaladinsApi:

    """
    PT-BR: Classe usada para acessar a API do paladins através do wrapper Pyrez.
    Obs.: nunca instancie os champions ou itens no construtor da classe, isso atrasa desnecessáriamente qualquer
    outro comando além do ".image"
    Obs.2: Os comandos para retornar os campeões e os itens tem a conferência com o if pois eventualmente eles podem
    retornar vazios por erro na API, gerando um erro no bot.

    EN-US: Class used to access the paladins API through the Pyrez wrapper.
    Note: never instantiate champions or items in the class constructor, this unnecessarily delays any
    another command besides ".image"
    Note 2: The commands to return the champions and items have the check with the if because eventually they can
    return empty by error on the API, generating an error on the bot.

    https://github.com/luissilva1044894/Pyrez
    """

    def __init__(self):
        self._dev_id_hirez = "3656"
        self._auth_key_hirez = self._get_hirez_auth_key()
        self._paladins_req = pyrez.PaladinsAPI(devId=self._dev_id_hirez, authKey=self._auth_key_hirez)

    @staticmethod
    def _get_hirez_auth_key():
        with open('./Docs/ApiTokens/hirezApiToken', 'r') as f:
            return f.readline()

    def get_match_inf(self, match_id):
        return self._paladins_req.getMatch(match_id)

    def get_player_id_by_name(self, player_name):
        player = self._paladins_req.getPlayerId(player_name)[0]
        return f"Nick: {player['Name']} - Id: {player['player_id']}  "

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
