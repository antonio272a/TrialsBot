import discord
import pyrez
import asyncio
import json
from json import JSONEncoder
from imgcreation import create_stats_img
from iterator import DocIterator


# Código para resgatar o token do Bot
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Atribuindo o token à uma variavel
token = read_token()

# Código de requisição à API da Hirez
devId_Hirez = "3656"
authKey_Hirez = "310114B6E36447369BBD3F35034995AC"
paladins_req = pyrez.PaladinsAPI(devId=devId_Hirez, authKey=authKey_Hirez)
smite_req = pyrez.SmiteAPI(devId=devId_Hirez, authKey=authKey_Hirez)


# Código para gerar uma nova sessão da API
session_id_paladins = paladins_req._createSession()
session_id_smite = smite_req._createSession()

paladins_champions = paladins_req.getChampions()  # Instancia lista de campeões
paladins_itens = paladins_req.getItems()  # Instancia lista de itens
if paladins_itens is None:
    paladins_itens = paladins_req.getItems()
smite_gods = smite_req.getGods()
smite_itens = smite_req.getItems()

# Subindo o Bot no discord
client = discord.Client()

# Variáveis globais para print dos times nas imagens
winner_team = "[VKS]"
loser_team = "[GL]"


# Código quando é enviado uma mensagem ao Bot
@client.event
# Comandos
async def on_ready(): #Quando o bot fica pronto
    await client.change_presence(activity=discord.Game(name=".help"))
    print("Iniciado")


@client.event
async def on_message(message):  # Ao receber mensagem

    if message.content == ".help":
        embed = discord.Embed(title="Central de Ajuda do TrialsBot",
                              description='Alguns comandos para facilitar a moderação \n Lembrando que todos os '
                                          'comando devem ser seguidos por pelo jogo com o "-jogo", por exemplo: \n '
                                          '.stats-paladins ou .stats-smite')
        embed.add_field(name=".stats", value="Retorna o arquivo de texto com todos os stats da partida")
        embed.add_field(name=".id", value="Retorna os Id's de todos os jogadores, com exceção dos perfil privados")
        embed.add_field(name=".playerid", value="Retorna o Id do nick enviado")
        embed.add_field(name=".replay",
                        value="Renorna os players da partida pra conferência, junto com a informação de caso a "
                              "partida tenha Replay ou não")
        embed.add_field(name=".image (Pré-alpha)", value="Retorna a imagem dos stats da partida")
        embed.add_field(name=".winner", value="define o time vencedor para colagem nas imagems (Máx de 3 letras)")
        embed.add_field(name=".loser", value="define o time perdedor para colagem nas imagems (Máx de 3 letras)")
        await message.channel.send(content=None, embed=embed)

    if message.content.find(".image") != -1:  # Retona imagem dos resultados
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        match_id = retorno[1]
        game = retorno[0]
        if game == paladins_req:
            cria_imagem(match_id, game)  # Cria as imagens e salva
            imagem = "Teste-paladins.png"
        elif game == smite_req:
            cria_imagem(match_id, game) # Cria as imagens e salva
            imagem = "Teste-smite.png"
        with open("./createdimages/" + imagem, 'rb') as file:  # Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "Image.png"))
        file.close()

    if message.content.find(".stats") != -1:  # Retorna stats.txt no discord
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        pegar_stats(match_id, game)  # Retona os stas em um arquivo Stats.txt
        with open("Stats.txt", 'rb') as file:
            await message.channel.send(file=discord.File(file, "Stats.txt"))  # Envia arquivo no discord
        file.close()

    if message.content.find(".id") != -1:  # Retorna resultado da partida e ID dos players
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        details_players = pegar_id(match_id, game)  # Retorna a mensagem já formulada para envio
        envia_msg(channel_id, details_players)  # Envia mensagem no canal remetente do discord

    if message.content.find(".playerid") != -1: #Retorna o ID do nick passado
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        game = retorno[0]
        player_name = retorno[1]
        player_id = game.getPlayerId(player_name)[0]["player_id"] #retorna já o ID da conta, sendo privada ou não
        player_info = "Nick: " + player_name + " - id: " + str(player_id)
        envia_msg(channel_id, player_info)  # Envia mensagem no canal remetente do discord

    if message.content.find(".replay") != -1:  # Retorna se possui replay ou não
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        details_players = pegar_replay(match_id, game)  # Retorna a mensagem já formulada para envio
        envia_msg(channel_id, details_players)  # Envia mensagem no canal remetente do discord

    if message.content.find(".addthischannel") != -1:  # Adiciona o canal remetente na whitelist
        await message.channel.send("Comando recebido")  # Colocado sem função por agilidade no envio
        user_id = message.author.id
        channel_id = message.channel.id
        confere_user_id(user_id, channel_id)  # Confere o Id do User
        add_channel_id_whitelist(channel_id, channel_id)  # adiciona o canal à whitelist
        envia_msg(channel_id, "Canal adicionado com Sucesso")  # Envia mensagem no canal remetente do discord

    if message.content.find(".removethischannel") != -1:  # Remove o canal remetente da Whitelist
        await message.channel.send("Comando recebido")  # Colocado sem função por agilidade no envio
        user_id = message.author.id
        channel_id = message.channel.id
        confere_user_id(user_id, channel_id)  # Confere o Id do User
        remove_channel_id_whitelist(channel_id, channel_id)  # Remove o canal da Whitelist
        envia_msg(channel_id, "Canal removido com sucesso")  # Envia mensagem no canal remetente do discord

    if message.content.find(".removechannelid") != -1:  # Remove o id de canal informado da whitelist
        await message.channel.send("Comando recebido")  # Colocado sem função por agilidade no envio
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        confere_user_id(user_id, channel_id)  # Confere o Id do User
        removed_channel_id = reconhecer_comando(mensagem,
                                                ",removechannelid ")  # Trata a mensagem para ficar só o ID do canal
        remove_channel_id_whitelist(channel_id, removed_channel_id)  # Remove o canal da Whitelis
        envia_msg(channel_id, "Canal removido com sucesso")  # Envia mensagem no canal remetente do discord

    if message.content.find(".addchannelid") != -1:  # Adiciona o Id do canal informado à Whitelist
        await message.channel.send("Comando recebido")  # Colocado sem função por agilidade no envio
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        confere_user_id(user_id, channel_id)  # Confere o Id do User
        added_channel_id = ReconhecerComando(mensagem, ",addchannelid ")  # Trata a mensagem para ficar só o ID do canal
        add_channel_id_whitelist(channel_id, added_channel_id)  # adiciona o canal à whitelist
        envia_msg(channel_id, "Canal adicionado com sucesso")  # Envia mensagem no canal remetente do discord

    if message.content.find(".winner") != -1: #Define o time vencedor (Variável global)
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        time = "[" + retorno[1] + "]"
        global winner_team
        winner_team = time
        await message.channel.send(content="Time vencedor definido")

    if message.content.find(".loser") != -1: #Define o time perdedor (Variável global)
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        time = "[" + retorno[1] + "]"
        global loser_team
        loser_team = time
        await message.channel.send(content="Time perdedor definido")

    if message.content.find(".teste") != -1:  # Testa se o Id de usuário está sendo conferido
        await message.channel.send(content=".removethischannel")


"""
Funções para sequencia de funções/comandos repetidos:

1 - refatorando_cmd_mods
2 - reconhecer_comando
3 - reconhece_jogo
"""

def refatorando_cmd_mods(channel_id, mensagem):
    confere_disc_id(channel_id)  # Confere o Id do canal
    retorno = reconhece_jogo(channel_id, mensagem)  # Retorna a requisição do jogo e a string do comando sem o match_id
    game = retorno[0]
    comando = retorno[1]
    match_id = reconhecer_comando(mensagem, comando)  # Retira o comando da mensagem, sobrando só o match_id
    retorno = [game, match_id]
    return retorno


def reconhecer_comando(mensagem, content):
    input_comando = mensagem
    output_comando = input_comando.replace(content, "")  # Retira o comando, deixando somente o Id enviado
    return output_comando


def reconhece_jogo(channel_id, mensagem):
    comandos = [".id", ".playerid", ".stats", ".replay", ".image", ".winner", ".loser"]
    jogos = {"smite": smite_req, "paladins": paladins_req}
    for jogo in jogos:  # Percorre a lista de jogos instanciados acima
        if mensagem.find(jogo) != -1:  # Se achar o jogo dentro da mensagem
            game = jogos[jogo]  # requisição do jogo guardada dentro da variável game
            str_jogo = jogo  # str do jogo que vai ser usada para limpar a mensagem em seguida
            break
        else:
            game = "Error"  # Se não achar o jogo no comando, a variável fica com Str Error
            str_jogo = ""  # para poder levantar o erro em seguida
    for command in comandos:  # Percorre a lista de comandos
        if mensagem.find(command) != -1:  # Se achar o comando dentro da mensagem
            str_comando = command
            comando = str_comando + "-" + str_jogo + " "  # str que será retirada da mensagem para extrair o Id
            break
    mensagem = "Comando incorreto, o comando sempre deve ser acompanhado pelo jogo, detalhes em .help"
    retorno = [game, comando]
    if game == "Error":  # Se o jogo não for encontrado na mensagem, ele retorna um aviso pro User e um erro
        envia_msg(channel_id, mensagem)
        raise LookupError("Comando não acompanhado pelo jogo")

    return retorno


"""
Comandos para conferência de permissões:

1 - confere_id
2 - confere_user_id
3 - confere_disc_id
4 - raise_user_error
5 - raise_channel_error
"""

def confere_id(arquivo, used_id):
    response = False
    for loop in DocIterator(arquivo, used_id):  # Percorre os Id's
        if loop:  # Se retornar True (id presente no doc)
            response = True
            break
    return response


def confere_user_id(user_id, channel_id):
    response = confere_id("./whitelists/user_id_whitelist.txt", user_id)
    raise_user_error(channel_id, response)  # Caso seja False, essa função sobe um erro


def confere_disc_id(channel_id):
    response = confere_id("./whitelists/channel_whitelist.txt", channel_id)
    raise_channel_error(channel_id, response)  # Caso seja False, essa função sobe um erro


def raise_user_error(channel_id, response):
    # Recebe True ou False dos comandos, caso seja False, avisa o usuário do Erro e levanta erro)
    mensagem = "Você não tem permissão para usar esse comando"
    if not response:
        envia_msg(channel_id, mensagem)
        raise ValueError("Usuário sem permissão")


def raise_channel_error(channel_id, response):
    # Recebe True ou False dos comandos, caso seja False, avisa o usuário do Erro e levanta erro)
    mensagem = "Não é permitido enviar comandos nesse canal"
    if not response:
        envia_msg(channel_id, mensagem)
        raise ValueError("Canal fora da Whitelist")


"""
Comandos para adicionar permissão para canais ou users:

1 - add_channel_id_whitelist
2 - remove_channel_id_whitelist
"""

def add_channel_id_whitelist(channel_id, added_channel_id):
    canal_presente = confere_id("./whitelists/channel_whitelist.txt", added_channel_id)  # Confere canais na lista
    if canal_presente:
        envia_msg(channel_id, "Canal já presente na Whitelist")  # Avisa o usuário
        raise ValueError("Canal já presente na Whitelist")  # Levanta erro para evitar a duplicação de Id's
    else:
        with open("./whitelists/channel_whitelist.txt", "a") as whitelist_doc:
            whitelist_doc.write(str(added_channel_id) + "\n")  # Caso contrário, adiciona o Id
        whitelist_doc.close()


def remove_channel_id_whitelist(channel_id, removed_channel_id):
    canal_presente = confere_id("./whitelists/channel_whitelist.txt", removed_channel_id)  # Confere canais na lista
    if not canal_presente:  # Se o canal não estiver na whitelist
        envia_msg(channel_id, "Canal não presente na Whitelist")
        raise ValueError("Canal não presente na Whitelist")
    else:
        with open("./whitelists/channel_whitelist.txt", "r") as whitelist_doc:
            lines = whitelist_doc.readlines()  # retorna todos os Id's
            whitelist_doc.close()
        with open("./whitelists/channel_whitelist.txt", "w") as whitelist_doc:
            for line in lines:
                if line.strip("\n") != str(removed_channel_id):  # Se a linha for igual à removida, não escreve
                    whitelist_doc.write(line)
        whitelist_doc.close()


"""
Comandos para facilitar o envio de mensagens/arquivos no discord, podendo ser usados fora
de funções assíncronas

1 - envia_msg
2 - envia_arquivo (Desenvolvimento)
"""

def envia_msg(channel_id, mensagem):
    # Função para facilitar o envio de mensagens pelo bot por meio de funções não assíncronas
    channel = client.get_channel(channel_id)
    client.loop.create_task(channel.send(mensagem))


def envia_arquivo():  # Em desenvolvimento
    pass


"""
Comandos relacionados à API da Hirez com retorno em texto (serve para Paladins e Smite):
Obs.: O jogo é diferenciado pela variável game, que é a requisição do jogo usado

1 - pegar_id
2 - pegar_replay
3 - pegar_stats (Retorno em arquivo .txt)
"""

def pegar_id(match_id, game):
    match_inf = game.getMatch(match_id)  # Instancia as informações da partida
    details_players = ""
    index = 0  # Index usado para separar os times
    for player in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
        if game == paladins_req:
            if player["playerName"] == "":
                player_name = "Privado"  # Troca nome vazio
                player_id = "Privado"  # Troca Id 0
            else:
                player_name = player["playerName"]
                player_id = player["playerId"]

        elif game == smite_req:
            player_name = player["hz_player_name"]
            player_id = player["playerId"]
            if player_id == "0":
                player_id = str(smite_req.getPlayerId(player_name)[0]["player_id"])

        details_players += "\n" + player["Win_Status"] + " - " + "Nick: " + player_name + " - " + "Campeão: " + \
                            player["Reference_Name"] + " - " + "id: " + player_id  # Adiciona stats na mensagem
        index += 1
        if index == 5:
            details_players += "\n" + "\n" + "--------------------" + "\n"
        # Se passar de 5 players, ele separa com a str acima para separar os times
    return details_players


def pegar_replay(match_id, game):
    match_inf = game.getMatch(match_id)  # Instancia informações da partida
    details_players = ""
    index = 0  # index para separar os times
    for details in match_inf:
        if details["playerName"] == "":  # Confere se a conta do player é privada, nome retorna vazio
            player_name = "Privado"  # Troca nome vazio
        else:
            player_name = details["playerName"]
        details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + player_name  # Passa quem venceu e os nicks
        index += 1
        if index == 5:
            details_players += "\n" + "\n" + "--------------------" + "\n"  # Separa os times
    for details in match_inf:
        if details["hasReplay"] == "y":  # Confere se tem replay
            stats_replay = "Possui Replay"
            break
        else:
            stats_replay = "Não possui Replay"
    details_players += "\n" + stats_replay  # Adiciona a informação se tem replay ou não
    return details_players


def pegar_stats(match_id, game):
    match_inf = game.getMatch(match_id)  # instancia informações da partida
    with open("Stats.txt", 'w', encoding="UTF-8") as log:
        for player in match_inf:  # Pra cada player dentro das infos
            log.write('\n' + '\n' + '************************************' + '\n')  # Separa os players
            for stat in player:  # Pra cada info dentro dos players
                log.write('\n' + str(stat) + ' - ' + str(player[stat]))  # escreve info no doc
    log.close()


"""
Comandos relacionados à API da Hirez com retorno em imagem (serve para Paladins e Smite):
Obs.: O jogo é diferenciado pela variável game, que é a requisição do jogo usado

Funções criadas por motivo de melhor sintaxe:
    1 - cria_kda_stats (Função criada por motivo de melhor sintaxe)
    2 - cria_stats_list

Funções que encaminham as informações para o arquivo de criação de imagem (imgcreation.py)
    1 - cria_imagem
"""

def cria_kda_stats(player, kda_list):
    index = 0  # index para saber qual informação do kda está sendo usada
    kda_stat = ""
    for stat in kda_list:
        if index != 1:  # Se não for o do meio, só printa o stat
            kda_stat += str(player[stat])
        else:  # Se for o do meio, printa as barras junto
            kda_stat += "/" + str(player[stat]) + "/"
        index += 1
    return kda_stat


def cria_stats_list(match_inf, stats_reference_1, stats_reference_2, stats_reference_3):
    stats_list = []
    for player in match_inf:  # Pra cada jogador
        if type(stats_reference_1) == list:    # confere se é lista ou string
            for stat_1 in stats_reference_1:  # Pra cada stat na referência, adiciona o stat na lista
                stats_list.append(player[stat_1])
        else:
            stats_list.append(player[stats_reference_1])  # se for str, só adiciona na lista
        stats_list.append(cria_kda_stats(player, stats_reference_2))  # Forma o texto do KDA e coloca na lista
        for stat_3 in stats_reference_3:
            stats_list.append(player[stat_3])  # Coloca o resto dos stats depois do KDA
    return stats_list


def cria_imagem(match_id, game):
    # Instancia todas as listas e variáveis que os jogos vão precisar
    global smite_gods, smite_itens, paladins_champions, paladins_itens, winner_team, loser_team
    icons_id_list = []
    nicks_list = []
    teams_list = [winner_team, loser_team]

    # Caso seja Paladins
    if game == paladins_req:
        match_inf = paladins_req.getMatch(match_id)  # Instancia os stats da partida
        stats_reference_1 = ["playerName", "Gold_Earned"]
        stats_reference_2 = ["Kills_Player", "Deaths", "Assists"]
        stats_reference_3 = ["Killing_Spree", "Objective_Assists", "Damage_Player", "Damage_Mitigated", "Healing"]
        # Acima são as listas dos stats que serão passados para colagem

        for player in match_inf:  # Pra cada jogador
            icons_id_list.append(player["ChampionId"])  # adiciona Id do champ na lista

            # Cria a lista de stats
            stats_list = cria_stats_list(match_inf, stats_reference_1, stats_reference_2, stats_reference_3)

        # Passa as infos pra outro arquivo montar a imagem
        create_stats_img("paladins", icons_id_list, nicks_list, stats_list, teams_list,
                         paladins_champions, paladins_itens)

    # Caso seja smite
    elif game == smite_req:
        match_inf = smite_req.getMatch(match_id)
        stats_reference_1 = "Final_Match_Level"
        stats_reference_2 = ["Kills_Player", "Deaths", "Assists"]
        stats_reference_3 = ["Gold_Earned", "Gold_Per_Minute", "Damage_Player", "Damage_Bot", "Damage_Taken",
                             "Damage_Mitigated", "Structure_Damage", "Healing", "Wards_Placed"]
        # Acima são as listas dos stats que serão passados para colagem

        for player in match_inf:  # Pra cada jogador
            icons_id_list.append(player["GodId"])  # adiciona Id do god na lista
            if not player["playerName"]:
                if not player["hz_player_name"]:
                    player_name = ""
                else:
                    player_name = player["hz_player_name"]
            else:
                try:
                    player_name = player["playerName"][player["playerName"].find("]") + 1:]
                except:
                    player_name = player["playerName"]
            nicks_list.append(player_name)

        # Cria a lista de stats
        stats_list = cria_stats_list(match_inf, stats_reference_1, stats_reference_2, stats_reference_3)

        # Passa as infos pra outro arquivo montar a imagem
        create_stats_img("smite", icons_id_list, nicks_list, stats_list, teams_list,
                         smite_gods, smite_itens)


# Código para executar o Bot com as configurações pré-definidas
client.run(token)
