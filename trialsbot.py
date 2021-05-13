import discord
import pyrez
import asyncio
import json
from json import JSONEncoder
from imgcreation import create_paladins_stats_img
from iterator import DocIterator


# Código para resgatar o token do Bot
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Atribuindo o token a uma variavel
token = read_token()

# Código de requisição à API da Hirez
devId_Hirez = "3656"
authKey_Hirez = "310114B6E36447369BBD3F35034995AC"
paladins_req = pyrez.PaladinsAPI(devId=devId_Hirez, authKey=authKey_Hirez)
smite_req = pyrez.SmiteAPI(devId=devId_Hirez, authKey=authKey_Hirez)

# Código para gerar uma nova sessão da API
session_id_paladins = paladins_req._createSession()
session_id_smite = smite_req._createSession()

champions = paladins_req.getChampions()  # Instancia lista de campeões
itens = paladins_req.getItems()  # Instancia lista de itens

# Subindo o Bot no discord
client = discord.Client()

# Variáveis globais para print de imagem
winner_team = "[VKS]"
loser_team = "[GL]"


# Código quando é enviado uma mensagem ao Bot
@client.event
# Comandos
async def on_ready():
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
        embed.add_field(name=".replay",
                        value="Renorna os players da partida pra conferência, junto com a informação de caso a "
                              "partida tenha Replay ou não")
        embed.add_field(name=".image (Pré-alpha)", value="Retorna a imagem dos stats da partida")
        await message.channel.send(content=None, embed=embed)

    if message.content.find(".image") != -1:  # Retona imagem dos resultados
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        match_id = retorno[1]
        cria_paladins_imagem_stats(match_id)  # Cria as imagens e salva
        with open("./createdimages/Teste.png", 'rb') as file:  # Envia arquivo no discord
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

    if message.content.find(".winner") != -1:
        await message.channel.send(content="Comando recebido", embed=None)  # Colocado sem função por agilidade no envio
        mensagem = message.content
        channel_id = message.channel.id
        retorno = refatorando_cmd_mods(channel_id, mensagem)  # Função para simplificar o código
        time = "[" + retorno[1] + "]"
        global winner_team
        winner_team = time
        await message.channel.send(content="Time vencedor definido")

    if message.content.find(".loser") != -1:
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


# Funções
def refatorando_cmd_mods(channel_id, mensagem):
    confere_disc_id(channel_id)  # Confere o Id do canal
    retorno = reconhece_jogo(channel_id, mensagem)  # Retorna a requisição e a str do comando sem o match_id
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
    comandos = [".id", ".stats", ".replay", ".image", ".winner", ".loser"]
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


def pegar_id(match_id, game):
    match_inf = game.getMatch(match_id)  # Instancia as informações da partida
    details_players = ""
    index = 0  # Index usado para separar os times
    for details in match_inf:  # Confere se a conta do player é privada, nome retorna vazio
        if details["playerName"] == "":
            player_name = "Privado"  # Troca nome vazio
            player_id = "Privado"  # Troca Id 0
        else:
            player_name = details["playerName"]
            player_id = details["playerId"]
        details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + player_name + " - " + "Campeão: " + \
                           details["Reference_Name"] + " - " + "id: " + player_id  # Adiciona stats na mensagem
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


def envia_msg(channel_id, mensagem):
    # Função para facilitar o envio de mensagens pelo bot por meio de funções não assíncronas
    channel = client.get_channel(channel_id)
    client.loop.create_task(channel.send(mensagem))


def envia_arquivo():  # Em desenvolvimento
    pass


def cria_paladins_imagem_stats(match_id):
    global champions
    global itens
    global winner_team
    global loser_team
    teams_list = [winner_team, loser_team]
    icons_id_list = []
    stats_list = []
    match_inf = paladins_req.getMatch(match_id)  # Instancia os stats da partida
    stats_reference_1 = ["playerName", "Gold_Earned"]
    stats_reference_2 = ["Kills_Player", "Deaths", "Assists"]
    stats_reference_3 = ["Killing_Spree", "Objective_Assists", "Damage_Player", "Damage_Mitigated", "Healing"]

    # Acima é a lista dos stats que serão passados para colagem
    for player in match_inf:  # Pra cada jogador, adiciona Id de champ na lista
        kda_stat = ""
        index = 0
        icons_id_list.append(player["ChampionId"])
        for stat_1 in stats_reference_1:  # Pra cada stat na referência, adiciona o stat na lista
            stats_list.append(player[stat_1])
        for stat_2 in stats_reference_2:
            if index != 1:
                kda_stat += str(player[stat_2])
            else:
                kda_stat += "/" + str(player[stat_2]) + "/"
            index += 1
        stats_list.append(kda_stat)
        for stat_3 in stats_reference_3:
            stats_list.append(player[stat_3])
    # Passa as infos pra outro arquivo montar a imagem
    create_paladins_stats_img(icons_id_list, stats_list, teams_list, champions, itens)


# Código para executar o Bot com as configurações pré-definidas
client.run(token)
