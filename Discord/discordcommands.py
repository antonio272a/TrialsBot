from Discord.verify import Verify
from Utils.iterator import LineRemove
from ApiBattlefy.__main__ import BattlefyAPI
import json


class AdminCommands:
    """
    PT-BR: Classe usada para utilizar os comandos de administrador, que no momento são para adição e remoção de
    canais na whitelist, por enquanto não existe comando para adicionar usuários moderadores, o único jeito é
    adicionando diretamente no documento users_whitelist.txt.

    EN-US: Class used to use admin commands, which are currently for adding and removing
    channels on the whitelist, for now there is no command to add moderators users, the only way is
    adding directly to the users_whitelist.txt document.
    """
    def __init__(self, user_id, channel_id):
        self.channel_whitelist = "./Docs/DocsDiscord/Whitelists/channel_whitelist.txt"
        self.user_whitelist = "./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt"
        self.user_id = user_id
        self.channel_id = str(channel_id)
        self.channel_whitelisted = Verify.verify_channel(self.channel_id)

    def add_channel_to_whitelist(self):
        """
        PT-BR: Confere se o canal está listado, caso não esteja, abre o arquivo como modo "a" e adicona o canal
        e uma quebra de linha.

        EN-US: Check if the channel is listed, if not, open the file as "a" mode and add the channel
        and a line break.
        """
        if not self.channel_whitelisted:
            with open(self.channel_whitelist, "a") as whitelist_doc:
                whitelist_doc.write(self.channel_id + "\n")
            return "Canal adicionado com sucesso"
        else:
            return "Canal já presente na whitelist"

    def remove_channel_from_whitelist(self):
        """
        PT-BR: Confere se o canal está listado, caso esteja, utiliza a classe LineRemove (criada para evitar problemas
        de MemoryError) para excluir somente o canal desejado, maiores detalhes sobre a classe no arquivo iterator.py

        EN-US: Check if the channel is listed, if it is, use the LineRemove class(created to avoid MemoryError problems)
        to remove only the desired channel, more details about the class in the iterator.py file
        """
        if self.channel_whitelisted:
            with open(self.channel_whitelist, "w") as whitelist_doc:
                for channel in LineRemove(self.channel_whitelist, self.channel_id):
                    if channel:
                        whitelist_doc.write(channel)
            whitelist_doc.close()
            return "Canal removido com sucesso"
        else:
            return "Canal não presente na Whitelist"


class DiscordCommands:
    """
    PT-BR: Por motivo de não conseguir retornar um objeto do tipo discord.Embed por meio de uma classe externa, essa
    classe, temporáriamente, retorna somente a string que será usada pelo arquivo principal para identificar que o
    comando é ".help"

    EN-US: Because of not being able to return an discord.Embed object through an external class, this
    class temporarily returns only the string that will be used by the main file to identify that the
    is ".help" command
    """

    def __init__(self):
        self.commands = ["help"]

    def help_command(self):
        return "help"


class BattlefyCommands:
    def __init__(self, command, tournament_id):
        self.command = command
        self.tournament_id = tournament_id
        self._api = BattlefyAPI()

    def check_command(self):
        if self.command == ".registrations":
            return self.on_registrations_close()
        elif self.command == ".brackets":
            return self.on_brackets_release()

    def on_registrations_close(self):
        self._api.save_tournament_participants(self.tournament_id)
        return 'Informação dos agentes livres salva com sucesso'

    def on_brackets_release(self):
        free_agents_discord = self._api.get_free_agents_discord(self.tournament_id)
        with open('./Docs/DocsBattlefy/free-agents-discord.json', 'w') as f:
            data = json.dumps(free_agents_discord)
            json.dump(data, f)
        return 'Brackets'
