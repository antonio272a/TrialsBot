import discord
from discord.ext import commands
from Discord.verify import verify_channel
import ApiPaladinsSmite.paladinscommands as paladins


class Paladins(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return verify_channel(ctx.channel.id)

    async def cog_command_error(self, ctx, error):
        if type(error) == commands.CheckFailure:
            await ctx.send('Esse canal não possui permissão para executar esse comando')
        else:
            await ctx.send('Algum erro ocorreu, favor conferir a formatação da mensagem e tente novamente')

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('tested')

    @commands.group(name="paladins", invoke_without_command=True)
    async def paladins_cmd(self, ctx):
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
    async def paladins_img_cmd(self, ctx, match_id, team_1='', team_2=''):
        await paladins.get_image(ctx, match_id, team_1, team_2)

    @paladins_cmd.command(name="id")
    async def paladins_id_cmd(self, ctx, match_id):
        await paladins.get_player_id_by_match(ctx, match_id)

    @paladins_cmd.command(name="stats")
    async def paladins_stats_cmd(self, ctx, match_id):
        await paladins.get_stats_file(ctx, match_id)

    @paladins_cmd.command(name="replay")
    async def paladins_replay_cmd(self, ctx, match_id):
        await paladins.get_replay_status(ctx, match_id)

    @paladins_cmd.command(name="player_id")
    async def paladins_player_id_cmd(self, ctx, player_name):
        await paladins.get_player_id_by_name(ctx, player_name)


def setup(client):
    client.add_cog(Paladins(client))
