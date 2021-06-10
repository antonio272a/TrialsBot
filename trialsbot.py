import discord
import pyrez
from Discord.__main__ import Comand


# Código para resgatar o token do Bot
def read_token():
    with open("./Docs/DocsDiscord/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Atribuindo o token à uma variavel
token = read_token()

# Subindo o Bot no discord
client = discord.Client()



# Código quando é enviado uma mensagem ao Bot
@client.event
# Comandos
async def on_ready():  # Quando o bot fica pronto
    await client.change_presence(activity=discord.Game(name=".help"))
    print("Ready")


@client.event
async def on_message(message):  # Ao receber mensagem

    if message.author.id != 838267456296189983:
        if message.content.startswith("."):
            try:
                await message.channel.send("Comando recebido")
                retorno = Comand(message)
                if str(retorno) == "help":
                    await message.channel.send(embed=_help_command())
                elif str(retorno) == "PaladinsFile":
                    await Comand.send_file(message, "paladins")
                elif str(retorno) == "PaladinsImage":
                    await Comand.send_image(message, "paladins")
                elif str(retorno) == "SmiteFile":
                    await Comand.send_file(message, "smite")
                elif str(retorno) == "SmiteImage":
                    await Comand.send_image(message, "smite")
                else:
                    await message.channel.send(retorno)
            except:
                await message.channel.send("Ocorreu um erro, favor tentar novamente")

def _help_command():
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
    embed.add_field(name=".image", value="Retorna a imagem dos stats da partida. Caso seja paladins, envie os times"
                                         "junto da mensagem no formato \".image-paladins (id) WIN LOS \", com o "
                                         "\"WIN\" e \"LOS\" sendo as siglas dos times")
    return embed
# Código para executar o Bot com as configurações pré-definidas
client.run(token)
