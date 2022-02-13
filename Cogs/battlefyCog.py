import discord
from discord.ext import commands
from Discord.verify import verify_channel
import ApiBattlefy.battlefycommands as battlefy


class Battlefy(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        if ctx.subcommand_passed:
            return verify_channel(ctx.channel.id)
        return True

    async def cog_command_error(self, ctx, error):
        if type(error) == commands.CheckFailure:
            await ctx.send('Esse canal não possui permissão para executar esse comando')
        else:
            await ctx.send('Algum erro ocorreu, favor conferir a formatação da mensagem e tente novamente')

    @commands.group(name="battlefy", invoke_without_command=True)
    async def battlefy_cmd(self, ctx):
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
    async def battlefy_closed_registrations(self, ctx, tournament_id):
        await battlefy.on_registrations_close(ctx, tournament_id)

    @battlefy_cmd.command(name="release")
    async def battlefy_brackets_release(self, ctx, tournament_id):
        await battlefy.on_brackets_release(ctx, self.client, tournament_id)


def setup(client):
    client.add_cog(Battlefy(client))
