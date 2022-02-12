from ApiPaladinsSmite.paladinsapi import *


async def get_player_id_by_match(ctx, match_id, *_args):
    """
    :param match_id: |STR| or |INT|

    PT-BR: retorna uma lista com os nicks, campeão utilizado e id dos players
    Caso o player tenha conta privada, retorna o nick e o id com a string "Privado"

    EN-US: returns a list with nicknames, champion used and players ids
    If the player has a private account, it returns the nick and id with the string "Privado"
    """
    match_inf = get_match_inf(match_id)
    details_players = ""
    index = 0  # Index usado para separar os times
    for player in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
        if player["playerName"] == "":
            player_name = "Privado"  # Troca nome vazio
            player_id = "Privado"  # Troca Id 0
        else:
            player_name = player["playerName"]
            player_id = player["playerId"]
        details_players += "\n" + player["Win_Status"] + " - " + "Nick: " + player_name + " - " + "Campeão: " + \
                           player["Reference_Name"] + " - " + "id: " + player_id  # Adiciona stats na mensagem
        index += 1
        if index == 5:
            details_players += "\n" + "\n" + "--------------------" + "\n"
            # Se passar de 5 players, ele separa com a str acima para separar os times
    await ctx.send(details_players)


async def get_player_id_by_name(ctx, player_name, *_args):
    """
    :param player_name: |STR|

    PT-BR: Retorna o id do player mesmo que a conta seja privada

    EN-US: Returns player id even if account is private
    """
    player_id = request_player_id_by_name(player_name)
    await ctx.send(player_id)


async def get_replay_status(ctx, match_id, *_args):
    """
    :param match_id: |STR| or |INT|

    PT-BR: Verifica se a partida possui replay
    EN-US: check if the match has replay
    """
    match_inf = get_match_inf(match_id)  # Instancia informações da partida
    for player in match_inf:
        if player["hasReplay"] == "y":  # Confere se tem replay
            status_replay = "Possui Replay"
            break
        else:
            status_replay = "Não possui Replay"
    await ctx.send(status_replay)


async def get_stats_file(ctx, match_id, *_args):
    """
    :param match_id: |STR| or |INT|
    """
    match_inf = get_match_inf(match_id)  # instancia informações da partida
    with open("./Docs/DocsHirez/stats-paladins.txt", 'w', encoding="UTF-8") as log:
        for player in match_inf:  # Pra cada player dentro das infos
            log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
            for stat in player:  # Pra cada info dentro dos players
                log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
    log.close()
    with open("./Docs/DocsHirez/stats-paladins.txt", 'r') as file:  # Envia arquivo no discord
        await ctx.send(file=discord.File(file, "stats paladins.txt"))


async def get_image(ctx, match_id, winner_team, loser_team, *_args):
    """
    :param match_id: |STR| or |INT|
    :param winner_team: |STR|
    :param loser_team: |STR|
    :param ctx: discord event context
    """
    match_inf = get_match_inf(match_id)
    champions = get_champions()
    itens = get_itens()
    ImgPaladins(match_inf, champions, itens, winner_team or 'WIN', loser_team or 'LOS')
    with open("./Images/Createdimages/paladins.png", 'rb') as file:
        await ctx.channel.send(file=discord.File(file, "Image.png"))