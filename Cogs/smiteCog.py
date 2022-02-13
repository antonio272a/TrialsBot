import discord
from discord.ext import commands
from Discord.verify import verify_channel
import ApiPaladinsSmite.smitecommands as smite


class Smite(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return verify_channel(ctx.channel.id)

    async def cog_command_error(self, ctx, error):
        if type(error) == commands.CheckFailure:
            await ctx.send('Esse canal não possui permissão para executar esse comando')
        else:
            await ctx.send('Algum erro ocorreu, favor conferir a formatação da mensagem e tente novamente')

    @commands.group(name="smite", invoke_without_command=True)
    async def smite_cmd(self, ctx):
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
    async def smite_img_cmd(self, ctx, match_id):
        await smite.get_image(ctx, match_id)

    @smite_cmd.command(name="id")
    async def smite_id_cmd(self, ctx, match_id):
        await smite.get_player_id_by_match(ctx, match_id)

    @smite_cmd.command(name="stats")
    async def smite_stats_cmd(self, ctx, match_id):
        await smite.get_stats_file(ctx, match_id)

    @smite_cmd.command(name="replay")
    async def smite_replay_cmd(self, ctx, match_id):
        await smite.get_replay_status(ctx, match_id)

    @smite_cmd.command(name="player_id")
    async def smite_player_id_cmd(self, ctx, player_name):
        await smite.get_player_id_by_name(ctx, player_name)

def setup(client):
    client.add_cog(Smite(client))
