import discord
from Discord.verify import Verify
from ApiPaladinsSmite.__main__ import Paladins, Smite
from Discord.discordcommands import AdminCommands


class Comand:

    def __init__(self, message):
        self.message_content = message.content
        self.channel_id = message.channel.id
        self.user_id = message.author.id
        self.user_has_acess = Verify.verify_user(self.user_id)
        self.channel_permited = Verify.verify_channel(self.channel_id)
        self.admin_commands = {".addthischannel", ".removethischannel", ".addchannelid", ".removechannelid"}
        self.api_commands = {".id", ".playerid", ".stats", ".replay", ".image", ".teste"}
        self.retorno = self._main()

    def __str__(self):
        return self.retorno

    def _main(self):
        if self.message_content.split()[0] in self.admin_commands:
            if self.user_has_acess:
                for admin_command in self.admin_commands:
                    if self.message_content.find(admin_command) != -1:
                        self.command = admin_command
                return self._execute_admin_command()
            else:
                return "Erro: Usuário sem permissão"
        elif (self.message_content.split("-")[0] or self.message_content.split()[0]) in self.api_commands:
            if self.channel_permited:
                self._set_games()
                if not self._get_command():
                    return self._execute_api_command()
                else:
                    return self.error_message
            else:
                return "Erro: canal fora da Whitelist"
        else:
            pass

    def _get_command(self):
        for game_key in self.games:  # Percorre a lista de jogos instanciados acima
            if self.message_content.find(game_key) != -1:  # Se achar o jogo dentro da mensagem
                self.game = self.games[game_key]  # requisição do jogo guardada dentro da variável game
                break
            else:
                self.game = "Error"  # Se não achar o jogo no comando, a variável fica com Str Error
                self.error_message = "Erro: " \
                                     "Comando incorreto, o comando sempre deve ser acompanhado pelo jogo, detalhes em .help"
        for command in self.api_commands:  # Percorre a lista de comandos
            if self.message_content.find(command) != -1:  # Se achar o comando dentro da mensagem
                if command == ".image":
                    self._set_teams()
                self.command = command
                break
        if self.game == "Error":  # Se o jogo não for encontrado na mensagem, ele retorna um aviso pro User e um erro
            return True

    def _execute_api_command(self):
        if self.command == ".image":
            self._set_teams()
            return self.game.get_image(self.message_content.split()[1], self.winner_team, self.loser_team)
        elif self.command == ".id":
            return self.game.get_player_id_by_match(self.message_content.split()[1])
        elif self.command == ".playerid":
            return self.game.get_player_id_by_name(self.message_content[self.message_content.find(" "):])
        elif self.command == ".replay":
            return self.game.get_replay_status(self.message_content.split()[1])
        elif self.command == ".stats":
            return self.game.get_stats_file(self.message_content.split()[1])

    def _set_teams(self):
        try:
            self.winner_team = self.message_content.split()[2]
            self.loser_team = self.message_content.split()[3]
        except:
            self.winner_team = ""
            self.loser_team = ""

    def _set_games(self):
        self.games = {"smite": Smite(), "paladins": Paladins()}

    def _execute_admin_command(self):
        if self.command == ".addthischannel":
            return AdminCommands(self.user_id, self.channel_id).add_channel_to_whitelist()
        elif self.command == ".removethischannel":
            return AdminCommands(self.user_id, self.channel_id).remove_channel_from_whitelis()
        elif self.command == ".addchannelid":
            try:
                channel_id = self.message_content.split()[1]
                return AdminCommands(self.user_id, channel_id).add_channel_to_whitelist()
            except:
                return "Algum erro ocorreu, favor conferir a formatação da mensagem"
        elif self.command == ".removechannelid":
            try:
                channel_id = self.message_content.split()[1]
                return AdminCommands(self.user_id, channel_id).remove_channel_from_whitelis()
            except:
                return "Algum erro ocorreu, favor conferir a formatação da mensagem"

    @staticmethod
    async def send_image(message, imagem):
        with open("./Images/Createdimages/" + imagem + ".png", 'rb') as file:  # Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "Image.png"))


    @staticmethod
    async def send_file(message, filename):
        with open("./Docs/Docs" + filename.capitalize() + "/stats-" + filename + ".txt", 'r') as file:  # Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "stats " + filename + ".txt"))



