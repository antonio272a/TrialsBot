import discord
from Discord.verify import Verify


class AdminCommands:

    def __init__(self, user_id, channel_id):
        self.channel_whitelist = "./Docs/DocsDiscord/Whitelists/channel_whitelist.txt"
        self.user_whitelist = "./Docs/DocsDiscord/Whitelists/user_id_whitelist.txt"
        self.user_id = user_id
        self.channel_id = str(channel_id)
        self.channel_whitelisted = Verify.verify_channel(self.channel_id)

    def add_channel_to_whitelist(self):
        if not self.channel_whitelisted:
            with open(self.channel_whitelist, "a") as whitelist_doc:
                whitelist_doc.write(self.channel_id + "\n")
            return "Canal adicionado com sucesso"
        else:
            return "Canal já presente na whitelist"

    def remove_channel_from_whitelis(self):
        if self.channel_whitelisted:
            with open(self.channel_whitelist, "r") as whitelist_doc:
                lines = whitelist_doc.readlines()  # retorna todos os Id's
                whitelist_doc.close()
            with open(self.channel_whitelist, "w") as whitelist_doc:
                for line in lines:
                    if line.strip("\n") != self.channel_id:  # Se a linha for igual à removida, não escreve
                        whitelist_doc.write(line)
            whitelist_doc.close()
            return "Canal removido com sucesso"
        else:
            return "Canal não presente na Whitelist"

class DiscordCommands:

    def __init__(self):
        self.commands = ["help"]

    def help_command(self):
        return "help"
