import discord
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
    await client.change_presence(activity=discord.Game(name=".help"))  # Coloca a atividade do bot
    print("Ready")


@client.event
async def on_message(message):  # Ao receber mensagem

    """
    PT-BR: Esse arquivo é para a execução do bot de discord e para receber as mensagens.
    O "try" conferindo o retorno é para os casos que a mensagem para ser enviada de volta sejam arquvios
    (.png ou .txt) já que não é possível puxar funções assíncronas de dentro de uma classe.
    Nesses casos a classe retorna uma string específica.
    Sobre o .help:
    Não é possível (pelo menos que eu ainda tenha conseguido) retornar um objeto discord.Embed pela classe,
    então o Embed está sendo criado nesse mesmo arquivo por enquanto.

    EN-US: This file is for running the discord bot and for receiving messages.
    The "try" checking the return is for cases where the message to be sent back is files
    (.png or .txt) as it is not possible to pull asynchronous functions from within a class.
    In these cases the class returns a specific string.
    About .help:
    It's not possible (at least I've still managed to) return a discord.Embed object by the class,
    so Embed is being created in that same file for now.
    """

    if message.author.id != 838267456296189983:  # Confere se a mensagem não é do próprio bot
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
                                      '.stats-paladins ou .stats-smite',
                          colour=16711680)
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
