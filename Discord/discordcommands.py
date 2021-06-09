import Discord
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
        embed = discord.Embed(title="Central de Ajuda do TrialsBot",
                              description='Alguns comandos para facilitar a moderação \n Lembrando que todos os '
                                          'comando devem ser seguidos por pelo jogo com o "-jogo", por exemplo: \n '
                                          '.stats-paladins ou .stats-smite')
        embed.add_field(name=".stats", value="Retorna o arquivo de texto com todos os stats da partida")
        embed.add_field(name=".id", value="Retorna os Id's de todos os jogadores, com exceção dos perfil privados")
        embed.add_field(name=".playerid", value="Retorna o Id do nick enviado")
        embed.add_field(name=".replay",
                        value="Renorna os players da partida pra conferência, junto com a informação de caso a "
                              "partida tenha Replay ou não")
        embed.add_field(name=".image (Pré-alpha)", value="Retorna a imagem dos stats da partida")
        embed.add_field(name=".winner", value="define o time vencedor para colagem nas imagems (Máx de 3 letras)")
        embed.add_field(name=".loser", value="define o time perdedor para colagem nas imagems (Máx de 3 letras)")
        return embed
