import discord
from discord.ext import commands
from Discord.verify import verify_user
import Discord.discordcommands as admin


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return verify_user(ctx.message.author.id)

    async def cog_command_error(self, ctx, error):
        if type(error) == commands.CheckFailure:
            await ctx.send('Você não possui permissão para fazer esse commando')
        else:
            await ctx.send('Algum erro ocorreu, favor conferir a formatação da mensagem e tente novamente')

    @commands.group(name='admin', invoke_without_command=True)
    async def admin_cmd(self, ctx):
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
    async def admin_addthischannel(self, ctx):
        channel_id = ctx.channel.id
        await admin.add_channel_to_whitelist(ctx, channel_id)

    @admin_cmd.command(name='addchannelid')
    async def admin_addchannelid(self, ctx, channel_id):
        await admin.add_channel_to_whitelist(ctx, channel_id)

    @admin_cmd.command(name='removethischannel')
    async def admin_removethischannel(self, ctx):
        channel_id = ctx.channel.id
        await admin.remove_channel_from_whitelist(ctx, channel_id)

    @admin_cmd.command(name='removechannelid')
    async def admin_removechannel_id(self, ctx, channel_id):
        await admin.remove_channel_from_whitelist(ctx, channel_id)


def setup(client):
    client.add_cog(Admin(client))
