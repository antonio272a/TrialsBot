import discord
from discord.ext import commands
import Discord.discordcommands as admin
import ApiBattlefy.battlefycommands as battlefy
import ApiPaladinsSmite.paladinscommands as paladins
import ApiPaladinsSmite.smitecommands as smite


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


# @client.event
# async def on_command(ctx):
#     await ctx.send('Comando Recebio')


@client.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send('Algum erro ocorreu, favor conferir a formatação da mensagem e tente novamente')


# ADMIN GROUP COMMANDS


@client.group(name='admin', invoke_without_command=True)
async def admin_cmd(ctx):
    embed = discord.Embed(title='Comandos Admin',
                          description="Grupo de comandos para a administração do Bot \n"
                          "Formato dos comandos: _**.admin subcomando <parâmetros>**_",
                          colour=16711680)
    embed.add_field(name='addthischannel',
                    value='Adiciona o canal atual na whitelist',
                    inline=False)
    embed.add_field(name='addchannelid <channel_id>',
                    value='Adiciona na whitelist o canal especificado como parâmetro',
                    inline=False)
    embed.add_field(name='removethischannel',
                    value='Remove o canal atual da whitelist',
                    inline=False)
    embed.add_field(name='removechannelid  <channel_id>',
                    value='Remove da whitelist o canal especificado como parâmetro',
                    inline=False)
    await ctx.send(embed=embed)


@admin_cmd.command(name="addthischannel")
async def admin_addthischannel(ctx):
    channel_id = ctx.channel.id
    await admin.add_channel_to_whitelist(ctx, channel_id)


@admin_cmd.command(name='addchannelid')
async def admin_addchannelid(ctx, channel_id):
    await admin.add_channel_to_whitelist(ctx, channel_id)


@admin_cmd.command(name='removethischannel')
async def admin_removethischannel(ctx):
    channel_id = ctx.channel.id
    await admin.remove_channel_from_whitelist(ctx, channel_id)


@admin_cmd.command(name='removechannelid')
async def admin_removechannel_id(ctx, channel_id):
    await admin.remove_channel_from_whitelist(ctx, channel_id)


# BATTLEFY GROUP COMMANDS


@client.group(name="battlefy", invoke_without_command=True)
async def battlefy_cmd(ctx):
    embed = discord.Embed(title='Coamndos Battlefy',
                          description='Grupo de comandos para interagir com a Api do Battlefy \n'
                                      'Formato dos comandos: _**.battlefy subcomando <parâmetros>**_',
                          colour=16711680)
    embed.add_field(name='closed <tournament_id>',
                    value='Salve os agentes livres inscritos no torneio especificado \n'
                          '**Obs.: Usar somente no fechamento das inscrições**',
                    inline=False)
    embed.add_field(name='release <tournament_id>',
                    value='Envia as mensagens para os agentes livres que estão em time \n'
                          '**Obs.:** Caso não encontre o discord de algum agente, o bot retorna um aviso',
                    inline=False)
    await ctx.send(embed=embed)


@battlefy_cmd.command(name="closed")
async def battlefy_closed_registrations(ctx, tournament_id):
    await battlefy.on_registrations_close(ctx, tournament_id)


@battlefy_cmd.command(name="release")
async def battlefy_brackets_release(ctx, tournament_id):
    await battlefy.on_brackets_release(ctx, client, tournament_id)


# PALADINS GROUP COMMANDS

@client.group(name="paladins", invoke_without_command=True)
async def paladins_cmd(ctx):
    embed = discord.Embed(title='Comandos Paladins',
                          description='Grupo de comandos para interagir com a Api do Paladins \n'
                                      'Formato dos comandos: _**.paladins subcomando <parâmetros>**_',
                          colour=16711680)
    embed.add_field(name='id <match_id>',
                    value='Retorna uma lista de todos os id\'s dos jogadores presentes na partida de acordo com o '
                          'id passado como parâmetro. \n'
                          '**Obs.:** Não retorna Id\'s de contas privadas',
                    inline=False)
    embed.add_field(name='image <match_id> <team_1> <team_2>',
                    value='Retorna uma imagem de final de partida de acordo com o id passado como parâmetro \n'
                          'os parâmetros "team_1" e "team_2" são as siglas dos times que ficarão ao lado dos nomes '
                          'dos jogadores \n'
                          '**Obs.:** Caso as siglas dos times não sejam passadas, serão usadas as siglas "WIN" e "LOS"',
                    inline=False)
    embed.add_field(name='player_id <player_name>',
                    value='Retorna o id do jogador de acordo com o nick especificado',
                    inline=False)
    embed.add_field(name='replay <match_id>',
                    value='Retorna um texto indicando se a partida do id passado como parâmetro possui replay gravado '
                          'no servidor da Hi-rez',
                    inline=False)
    embed.add_field(name='stats <match_id>',
                    value='retorna um documento de texto com todos os stats da partida especificada',
                    inline=False)
    await ctx.send(embed=embed)


@paladins_cmd.command(name="image")
async def paladins_img_cmd(ctx, match_id, team_1='', team_2=''):
    await paladins.get_image(ctx, match_id, team_1, team_2)


@paladins_cmd.command(name="id")
async def paladins_id_cmd(ctx, match_id):
    await paladins.get_player_id_by_match(ctx, match_id)


@paladins_cmd.command(name="stats")
async def paladins_stats_cmd(ctx, match_id):
    await paladins.get_stats_file(ctx, match_id)


@paladins_cmd.command(name="replay")
async def paladins_replay_cmd(ctx, match_id):
    await paladins.get_replay_status(ctx, match_id)


@paladins_cmd.command(name="player_id")
async def paladins_player_id_cmd(ctx, player_name):
    await paladins.get_player_id_by_name(ctx, player_name)


# SMITE GROUP COMMANDS


@client.group(name="smite", invoke_without_command=True)
async def smite_cmd(ctx):
    embed = discord.Embed(title='Comandos Smite',
                          description='Grupo de comandos para interagir com a Api do Smite \n'
                                      'Formato dos comandos: _**.smite subcomando <parâmetros>**_',
                          colour=16711680)
    embed.add_field(name='id <match_id>',
                    value='Retorna uma lista de todos os id\'s dos jogadores presentes na partida de acordo com o '
                          'id passado como parâmetro. \n'
                          '**Obs.:** Não retorna Id\'s de contas privadas',
                    inline=False)
    embed.add_field(name='image <match_id>',
                    value='Retorna uma imagem de final de partida de acordo com o id passado como parâmetro',
                    inline=False)
    embed.add_field(name='player_id <player_name>',
                    value='Retorna o id do jogador de acordo com o nick especificado',
                    inline=False)
    embed.add_field(name='replay <match_id>',
                    value='Retorna um texto indicando se a partida do id passado como parâmetro possui replay gravado '
                          'no servidor da Hi-rez',
                    inline=False)
    embed.add_field(name='stats <match_id>',
                    value='retorna um documento de texto com todos os stats da partida especificada',
                    inline=False)
    await ctx.send(embed=embed)


@smite_cmd.command(name="image")
async def smite_img_cmd(ctx, match_id):
    await smite.get_image(ctx, match_id)


@smite_cmd.command(name="id")
async def smite_id_cmd(ctx, match_id):
    await smite.get_player_id_by_match(ctx, match_id)


@smite_cmd.command(name="stats")
async def smite_stats_cmd(ctx, match_id):
    await smite.get_stats_file(ctx, match_id)


@smite_cmd.command(name="replay")
async def smite_replay_cmd(ctx, match_id):
    await smite.get_replay_status(ctx, match_id)


@smite_cmd.command(name="player_id")
async def smite_player_id_cmd(ctx, player_name):
    await smite.get_player_id_by_name(ctx, player_name)


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
