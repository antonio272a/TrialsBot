from ApiPaladinsSmite.smiteapi import *


async def get_player_id_by_match(ctx, match_id):
    """
    :param match_id: |STR| or |INT|
    :return: |STR|

    PT-BR: retorna uma lista com os nicks, god utilizado e id dos players
    Caso o player tenha conta privada, tenta acessar o nick da conta da Hi-rez, já que esse nunca fica privado
    e é possível retornar o id do player por ele, caso não tenha conta Hi-rez vinculada retorna o nick e o id com
    a string "Privado"

    EN-US: returns a list of nicks, god used and player id
    If the player has a private account, try to access the nick of the Hi-rez account, as it is never private
    and it is possible to return the id of the player by it, if it doesn't have linked Hi-rez account returns
    the nick and id with the string "Privado"
    """
    match_inf = get_match_inf(match_id)
    details_players = ""
    index = 0  # Index usado para separar os times
    for player in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
        if not player["playerName"]:
            if player["hz_player_name"]:
                player_name = player["hz_player_name"]
                player_id = get_player_id_by_name(player_name)
            else:
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


async def get_player_id_by_name(ctx, player_name):
    """
    :param player_name: |STR|
    :return: |STR|

    PT-BR: Retorna o id do player mesmo que a conta seja privada
    Obs.: Pode ser usado o nick da conta da Hi-rez vinculada

    EN-US: Returns player id even if account is private
    Note: Linked Hirez account nick can be used
    """
    await ctx.send(get_player_id_by_name(player_name))


async def get_replay_status(ctx, match_id, *args, **kwargs):
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


async def get_stats_file(ctx, match_id, *args, **kwargs):
    match_inf = get_match_inf(match_id)  # instancia informações da partida
    with open("./Docs/DocsHirez/stats-smite.txt", 'w', encoding="UTF-8") as log:
        for player in match_inf:  # Pra cada player dentro das infos
            log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
            for stat in player:  # Pra cada info dentro dos players
                log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
    log.close()
    with open("./Docs/DocsHirez/stats-smite.txt", 'r') as file:  # Envia arquivo no discord
        await ctx.send(file=discord.File(file, "stats smite.txt"))


async def get_image(ctx, match_id):
    match_inf = get_match_inf(match_id)
    gods = get_gods()
    itens = get_itens()
    ImgSmite(match_inf, gods, itens)
    with open("./Images/Createdimages/smite.png", 'rb') as file:
        await ctx.channel.send(file=discord.File(file, "Image.png"))
