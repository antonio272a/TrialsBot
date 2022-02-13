import os
import discord
from discord.ext import commands


# Código para resgatar o token do Bot
def read_token():
    with open("./Docs/DocsDiscord/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Atribuindo o token à uma variavel
token = read_token()

# Subindo o Bot no discord
intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='.', help_command=None, case_insensitive=True)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".help"))  # Coloca a atividade do bot
    print("Ready")

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')


@client.command(pass_context=True, name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="Central de Ajuda do TrialsBot",
                          description='Alguns comandos para facilitar a moderação \n Lembrando que todos os '
                                      'comando estão separados por categoria, para maiores informações '
                                      'coloque os comandos base para maiores informações ex.: **.admin**',
                          colour=16711680)
    embed.add_field(name=".admin", value="Grupo de comandos separado para a administração do Bot", inline=False)
    embed.add_field(name=".battlefy", value="Comandos para interagir com os torneios do Battlefy", inline=False)
    embed.add_field(name=".paladins", value="Comandos para interagir com a API do Paladins", inline=False)
    embed.add_field(name=".smite", value="Comandos para interagir com a API do Smite", inline=False)
    await ctx.send(embed=embed)


client.run(token)
