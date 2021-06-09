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
                if str(retorno) == "PaladinsFile":
                    await Comand.send_file(message, "paladins")
                elif str(retorno) == "PaladinsImage":
                    await Comand.send_image(message, "paladins")
                elif str(retorno) == "SmiteFile":
                    await Comand.send_file(message, "smite")
                elif str(retorno) == "SmiteImage":
                    await Comand.send_image(message, "smite")
                elif isinstance(retorno, type(discord.Embed())):
                    await message.channel.send(embed=retorno)
                else:
                    await message.channel.send(retorno)
            except:
                await message.channel.send("Ocorreu um erro, favor tentar novamente")

# Código para executar o Bot com as configurações pré-definidas
client.run(token)
