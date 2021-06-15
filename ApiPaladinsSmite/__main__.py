from ApiPaladinsSmite.paladinsapi import PaladinsApi
from ApiPaladinsSmite.smiteapi import SmiteApi
from ApiPaladinsSmite.images import ImgPaladins, ImgSmite

"""
    PT-BR: Classes usadas para executar os comandos personalizados tratando o retorno da API, todos os métodos retornam
    uma string que é tratada no arquivo "trialsbot.py" para caso seja preciso enviar um arquivo.
    Para maiores detalhes sobre a API acesse os arquivos "smiteapi.py" ou "paladinsapi.py"
   
   EN-US: Classes used to execute custom commands handling API return, all methods return a string that is treated in 
   the "trialsbot.py" file in case a file needs to be send.
    For more details about the API, access the files "smiteapi.py" or "paladinsapi.py" 
"""


class Paladins:

    def __init__(self):
        self.call = PaladinsApi()

    def get_player_id_by_match(self, match_id):
        """
        :param match_id: |STR| or |INT|

        PT-BR: retorna uma lista com os nicks, campeão utilizado e id dos players
        Caso o player tenha conta privada, retorna o nick e o id com a string "Privado"

        EN-US: returns a list with nicknames, champion used and players ids
        If the player has a private account, it returns the nick and id with the string "Privado"
        """
        match_inf = self.call.get_match_inf(match_id)
        details_players = ""
        index = 0  # Index usado para separar os times
        for player in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
            if player["playerName"] == "":
                player_name = "Privado"  # Troca nome vazio
                player_id = "Privado"  # Troca Id 0
            else:
                player_name = player["playerName"]
                player_id = player["playerId"]
            details_players += "\n" + player["Win_Status"] + " - " + "Nick: " + player_name + " - " + "Campeão: " + \
                               player["Reference_Name"] + " - " + "id: " + player_id  # Adiciona stats na mensagem
            index += 1
            if index == 5:
                details_players += "\n" + "\n" + "--------------------" + "\n"
                # Se passar de 5 players, ele separa com a str acima para separar os times
        return details_players

    def get_player_id_by_name(self, player_name):
        """
        :param player_name: |STR|

        PT-BR: Retorna o id do player mesmo que a conta seja privada

        EN-US: Returns player id even if account is private
        """
        player_id = self.call.get_player_id_by_name(player_name)
        return player_id

    def get_replay_status(self, match_id):
        """
        :param match_id: |STR| or |INT|

        PT-BR: Verifica se a partida possui replay
        EN-US: check if the match has replay
        """
        match_inf = self.call.get_match_inf(match_id)  # Instancia informações da partida
        for player in match_inf:
            if player["hasReplay"] == "y":  # Confere se tem replay
                status_replay = "Possui Replay"
                break
            else:
                status_replay = "Não possui Replay"
        return status_replay

    def get_stats_file(self, match_id):
        """
        :param match_id: |STR| or |INT|

        PT-BR: Cria um arquvio "stats-paladins.txt" com todos os stats da partida listados em cada linha e retorna
        a string que o arquivo "trialsbot.py" irá usar para enviar o arquivo no discord.

        EN-US: Creates a "stats-paladins.txt" file with all match stats listed on each line and returns
        the string wich the "trialsbot.py" file will use to send the file on discord.
        """
        match_inf = self.call.get_match_inf(match_id)  # instancia informações da partida
        with open("./Docs/DocsPaladins/stats-paladins.txt", 'w', encoding="UTF-8") as log:
            for player in match_inf:  # Pra cada player dentro das infos
                log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
                for stat in player:  # Pra cada info dentro dos players
                    log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
        log.close()
        return "PaladinsFile"

    def get_image(self, match_id, winner_team, loser_team):
        """
        :param match_id: |STR| or |INT|
        :param winner_team: |STR|
        :param loser_team: |STR|

        PT-BR: cria a imagem usando o classe do arquivo "images.py" e retorna a string para o arquvivo "trialsbot.py"
        enviar a imagem no discord.

        EN-US: creates the image using the class from the file "images.py" and returns the string to the file
        "trialsbot.py" send the image on discord.
        """
        match_inf = self.call.get_match_inf(match_id)
        champions = self.call.get_champions()
        itens = self.call.get_itens()
        ImgPaladins(match_inf, champions, itens, winner_team, loser_team)
        return "PaladinsImage"


class Smite:

    def __init__(self):
        self.call = SmiteApi()

    def get_player_id_by_match(self, match_id):
        """
        :param match_id: |STR| or |INT|
        :return: |STR|

        PT-BR: retorna uma lista com os nicks, god utilizado e id dos players
        Caso o player tenha conta privada, tenta acessar o nick da conta da Hi-rez, já que esse nunca fica privado
        e é possível retornar o id do player por ele, caso não tenha conta Hi-rez vinculada retorna o nick e o id com
        a string "Privado"

        EN-US: returns a list of nicks, god used and player id
        If the player has a private account, try to access the nick of the Hi-rez account, as it is never private
        and it is possible to return the id of the player by it, if it doesn't have linked Hi-rez account returns
        the nick and id with the string "Privado"
        """
        match_inf = self.call.get_match_inf(match_id)
        details_players = ""
        index = 0  # Index usado para separar os times
        for player in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
            if not player["playerName"]:
                if player["hz_player_name"]:
                    player_name = player["hz_player_name"]
                    player_id = self.get_player_id_by_name(player_name)
                else:
                    player_name = "Privado"  # Troca nome vazio
                    player_id = "Privado"  # Troca Id 0
            else:
                player_name = player["playerName"]
                player_id = player["playerId"]
            details_players += "\n" + player["Win_Status"] + " - " + "Nick: " + player_name + " - " + "Campeão: " + \
                               player["Reference_Name"] + " - " + "id: " + player_id  # Adiciona stats na mensagem
            index += 1
            if index == 5:
                details_players += "\n" + "\n" + "--------------------" + "\n"
                # Se passar de 5 players, ele separa com a str acima para separar os times
        return details_players

    def get_player_id_by_name(self, player_name):
        """
        :param player_name: |STR|
        :return: |STR|

        PT-BR: Retorna o id do player mesmo que a conta seja privada
        Obs.: Pode ser usado o nick da conta da Hi-rez vinculada

        EN-US: Returns player id even if account is private
        Note: Linked Hirez account nick can be used
        """
        player_id = self.call.get_player_id_by_name(player_name)
        return player_id

    def get_replay_status(self, match_id):
        """
        :param match_id: |STR| or |INT|

        PT-BR: Verifica se a partida possui replay
        EN-US: check if the match has replay
        """
        match_inf = self.call.get_match_inf(match_id)  # Instancia informações da partida
        for player in match_inf:
            if player["hasReplay"] == "y":  # Confere se tem replay
                status_replay = "Possui Replay"
                break
            else:
                status_replay = "Não possui Replay"
        return status_replay

    def get_stats_file(self, match_id):
        """
        :param match_id: |STR| or |INT|

        PT-BR: Cria um arquvio "stats-smite.txt" com todos os stats da partida listados em cada linha e retorna
        a string que o arquivo "trialsbot.py" irá usar para enviar o arquivo no discord.

        EN-US: Creates a "stats-smite.txt" file with all match stats listed on each line and returns
        the string wich the "trialsbot.py" file will use to send the file on discord.
        """
        match_inf = self.call.get_match_inf(match_id)  # instancia informações da partida
        with open("./Docs/DocsSmite/stats-smite.txt", 'w', encoding="UTF-8") as log:
            for player in match_inf:  # Pra cada player dentro das infos
                log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
                for stat in player:  # Pra cada info dentro dos players
                    log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
        log.close()
        return "SmiteFile"

    def get_image(self, match_id, winner_team, loser_team):
        """
        :param match_id: |STR| or |INT|
        :param winner_team: |STR|
        :param loser_team: |STR|

        PT-BR: cria a imagem usando o classe do arquivo "images.py" e retorna a string para o arquvivo "trialsbot.py"
        enviar a imagem no discord.
        Obs.: as variáveis dos times não são usados por enquanto, mas já estão ai para possíveis mudanças futuras

        EN-US: creates the image using the class from the file "images.py" and returns the string to the file
        "trialsbot.py" send the image on discord.
        Note: the team variables are not used for now, but they are already there for possible future changes
        """
        match_inf = self.call.get_match_inf(match_id)
        gods = self.call.get_gods()
        itens = self.call.get_itens()
        ImgSmite(match_inf, gods, itens)
        return "SmiteImage"
