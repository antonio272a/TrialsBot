from ApiPaladinsSmite.paladinsapi import PaladinsApi
from ApiPaladinsSmite.smiteapi import SmiteApi
from ApiPaladinsSmite.images import ImgPaladins, ImgSmite


class Paladins:

    def __init__(self):
        self.call = PaladinsApi()

    def get_player_id_by_match(self, match_id):
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
        player_id = self.call.get_player_id_by_name(player_name)
        return player_id

    def get_replay_status(self, match_id):
        match_inf = self.call.get_match_inf(match_id)  # Instancia informações da partida
        for player in match_inf:
            if player["hasReplay"] == "y":  # Confere se tem replay
                status_replay = "Possui Replay"
                break
            else:
                status_replay = "Não possui Replay"
        return status_replay

    def get_stats_file(self, match_id):
        match_inf = self.call.get_match_inf(match_id)  # instancia informações da partida
        with open("./Docs/DocsPaladins/stats-paladins.txt", 'w', encoding="UTF-8") as log:
            for player in match_inf:  # Pra cada player dentro das infos
                log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
                for stat in player:  # Pra cada info dentro dos players
                    log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
        log.close()
        return "PaladinsFile"

    def get_image(self, match_id, winner_team, loser_team):
        match_inf = self.call.get_match_inf(match_id)
        champions = self.call.get_champions()
        itens = self.call.get_itens()
        ImgPaladins(match_inf, champions, itens, winner_team, loser_team)
        return "PaladinsImage"


class Smite:

    def __init__(self):
        self.call = SmiteApi()

    def get_player_id_by_match(self, match_id):
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
        player_id = self.call.get_player_id_by_name(player_name)
        return player_id

    def get_replay_status(self, match_id):
        match_inf = self.call.get_match_inf(match_id)  # Instancia informações da partida
        for player in match_inf:
            if player["hasReplay"] == "y":  # Confere se tem replay
                status_replay = "Possui Replay"
                break
            else:
                status_replay = "Não possui Replay"
        return status_replay

    def get_stats_file(self, match_id):
        match_inf = self.call.get_match_inf(match_id)  # instancia informações da partida
        with open("./Docs/DocsSmite/stats-smite.txt", 'w', encoding="UTF-8") as log:
            for player in match_inf:  # Pra cada player dentro das infos
                log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
                for stat in player:  # Pra cada info dentro dos players
                    log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
        log.close()
        return "SmiteFile"

    def get_image(self, match_id, winner_team, loser_team):
        match_inf = self.call.get_match_inf(match_id)
        gods = self.call.get_gods()
        itens = self.call.get_itens()
        ImgSmite(match_inf, gods, itens)
        return "SmiteImage"


