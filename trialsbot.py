import discord
from discord.ext import commands
from Discord.discordcommands import *
from ApiBattlefy.battlefycommands import *


# Código para resgatar o token do Bot
def read_token():
    with open("./Docs/DocsDiscord/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Atribuindo o token à uma variavel
token = read_token()

# Subindo o Bot no discord
intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='.')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".help"))  # Coloca a atividade do bot
    print("Ready")


@client.command(pass_context=True)
async def admin(ctx, command, param=""):
    admin_commands = {
        'addthischannel': add_channel_to_whitelist,
        'removethischannel': remove_channel_from_whitelist,
        'removechannelid': remove_channel_from_whitelist,
        'addchannelid': add_channel_to_whitelist
    }
    channel_id = param or ctx.channel.id
    try:
        result = admin_commands[command](channel_id)
        await ctx.send(result)
    except:
        await ctx.send('Algum erro ocorreu, favor converir a formatação da mensagem')


@client.command(pass_context=True)
async def battlefy(ctx, command, tournament_id):
    batltefy_commands = {
        'closed': on_registrations_close,
        'release': on_brackets_release
        }
    message = batltefy_commands[command](tournament_id)
    if message:
        await ctx.send(message)
    else:
        await send_message_to_f_a(ctx, client)
        await ctx.send('mensagens enviadas')


@client.command(pass_context=True)
async def paladins(ctx, command, param=""):
    pass

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
