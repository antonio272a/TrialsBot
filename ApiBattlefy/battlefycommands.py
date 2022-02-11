from ApiBattlefy.__main__ import *
import json


def on_registrations_close(tournament_id):
    save_tournament_participants(tournament_id)
    return 'Informação dos agentes livres salva com sucesso'


def on_brackets_release(tournament_id):
    free_agents_discord = get_free_agents_discord(tournament_id)
    with open('./Docs/DocsBattlefy/free-agents-discord.json', 'w') as f:
        data = json.dumps(free_agents_discord)
        json.dump(data, f)


async def get_member(client, name, discriminator):
    members = client.get_all_members()
    for member in members:
        if (member.discriminator == discriminator) and (member.name.upper() == name.upper()):
            return member.id


async def send_message_to_f_a(ctx, client):
    with open('./Docs/DocsBattlefy/free-agents-discord.json', 'r') as f:
        data = json.load(f)
        agents_list = json.loads(data)
    for player in agents_list:
        username, team = player
        name, discriminator = username.split('#')
        try:
            user_id = await get_member(client, name, discriminator)
            user = await client.fetch_user(user_id)
            await user.send(f"Boa tarde <@{user_id}>, hoje no camepeonato da Trials, você jogará no time {team}")
        except:
            await ctx.send(f'erro ao encontrar o jogador **{username}** do time **{team}**')