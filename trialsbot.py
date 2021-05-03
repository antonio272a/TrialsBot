import discord
import pyrez
import asyncio

#Código para resgatar o token do Bot
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

#Atribuindo o token a uma variavel
token = read_token()

#Código de requisição à API da Hirez
devId_Hirez = "3656"
authKey_Hirez = "310114B6E36447369BBD3F35034995AC"
paladins_req = pyrez.PaladinsAPI(devId=devId_Hirez, authKey=authKey_Hirez)
smite_req = pyrez.SmiteAPI(devId=devId_Hirez, authKey=authKey_Hirez)

#Código para gerar uma nova sessão da API
sessionId_Paladins = paladins_req._createSession()
sessionId_Smite = smite_req._createSession()

#Subindo o Bot no discord
client = discord.Client()

#Código quando é enviado uma mensagem ao Bot
@client.event

#Comandos
async def on_message(message):
    if message.content == ".help":

        embed = discord.Embed(title="Central de Ajuda do TrialsBot", description='Alguns comandos para facilitar a moderação \n Lembrando que todos os comando devem ser seguidos por pelo jogo com o "-jogo", por exemplo: \n'
                                                                                 '.stats-paladins ou .stats-smite')
        embed.add_field(name=".stats", value="Retorna o arquivo de texto com todos os stats da partida")
        embed.add_field(name=".id", value="Retorna os Id's de todos os jogadores, com exceção dos perfil privados")
        embed.add_field(name=".replay", value="Renorna os players da partida pra conferência, junto com a informação de caso a partida tenha Replay ou não")
        await message.channel.send(content=None, embed=embed)

    if message.content.find(".stats") != -1: #Retorna stats.txt no discord
        await message.channel.send(content="Comando recebido", embed=None)
        mensagem = message.content
        channelId = message.channel.id
        retorno = Refatorando(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        PegarStats(match_id, game)
        with open("teste.txt", 'rb') as file:
            await message.channel.send(file=discord.File(file, "Stats.txt"))

    if message.content.find(".id") != -1: #Retorna resultado da partida e ID dos players
        await message.channel.send(content="Comando recebido", embed=None)
        mensagem = message.content
        channelId = message.channel.id
        retorno = Refatorando(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarId(match_id, game)
        Envia_Msg(channelId, details_players)

    if message.content.find(".replay") != -1: #Retorna se possui replay ou não
        await message.channel.send(content="Comando recebido", embed=None)
        mensagem = message.content
        channelId = message.channel.id
        retorno = Refatorando(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarReplay(match_id, game)
        Envia_Msg(channelId, details_players)

    if message.content.find(".teste") != -1:
        print("comando recebido")
        id = message.channel.id
        response = ConfereDiscId(id)
        if not response: raise ValueError("Server fora da Whitelist")
        print(response)

#Funções

def Refatorando(channelId, mensagem ):
    response = ConfereDiscId(channelId)
    RaiseChannelError(channelId, response)
    retorno = ReconheceJogo(channelId, mensagem)
    game = retorno[0]
    comando = retorno[1]
    match_id = ReconhecerComando(mensagem, comando)
    retorno = [game, match_id]
    return retorno

def ReconhecerComando(mensagem, content):
    input_comando = mensagem
    output_comando = input_comando.replace(content, "")
    return output_comando

def ReconheceJogo (channel_id, mensagem):
    comandos = [".id", ".stats", ".replay"]
    jogos = {"smite": smite_req, "paladins": paladins_req}
    for jogo in jogos:
        if mensagem.find(jogo) != -1:
            game = jogos[jogo]
            str_jogo = jogo
            break
        else:
            game = "Error"
            str_jogo = ""
    for command in comandos:
        if mensagem.find(command) != -1:
            str_comando = command
            comando = str_comando + "-" + str_jogo + " "
            break
    retorno = [game, comando]
    mensagem = "Comando incorreto, o comando sempre deve ser acompanhado pelo jogo, detalhes em .help"
    if game == "Error":
        Envia_Msg(channel_id, mensagem)
        raise LookupError("Comando não acompanhado pelo jogo")

    return retorno

def PegarId(match_id, game):
    match_inf = game.getMatch(match_id)
    with open("ids.txt", "w") as ids:
        details_players = ""
        index = 0
        for details in match_inf:
            if details["playerName"] == "":
                playerName = "Privado"
            else:
                playerName = details["playerName"]
            if details["playerId"] == "0":
                playerId = "Privado"
            else:
                playerId = details["playerId"]
            details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + playerName + " - " + "Campeão: " + \
                               details["Reference_Name"] + " - " + \
                               "id: " + playerId
            index += 1
            if index == 5: details_players += "\n" + "\n" + "--------------------" + "\n"
        return details_players

def PegarReplay(match_id, game):
    match_inf = game.getMatch(match_id)
    with open("ids.txt", "w") as ids:
        details_players = ""
        index = 0

        for details in match_inf:
            if details["playerName"] == "":
                playerName = "Privado"
            else:
                playerName = details["playerName"]
            if details["playerId"] == "0":
                playerId = "Privado"
            else:
                playerId = details["playerId"]
            details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + playerName
            index += 1
            if index == 5: details_players += "\n" + "\n" + "--------------------" + "\n"
        for details in match_inf:
            if details["hasReplay"] == "y":
                stats_replay = "Possui Replay"
                break
            else:
                stats_replay = "Não possui Replay"
        details_players += "\n" + stats_replay
    return details_players

def PegarStats(match_id, game):
    match_inf = game.getMatch(match_id)
    with open("teste.txt", 'w+', encoding="UTF-8") as log:
        for lista in match_inf:
            log.write('\n' + '\n' + '************************************' + '\n')
            for dict in lista:
                log.write('\n' + str(dict) + ' - ' + str(lista[dict]))
    log.close()

def ConfereDiscId(channel_id):
    whitelist = []
    with open ("server_whitelist.txt", "r+") as whitelist_doc:
        for linha in whitelist_doc.readlines():
            nova_linha = linha.replace("\n", "")
            whitelist.append(nova_linha)
        whitelist_doc.close()
    for channel in whitelist:
        if channel == str(channel_id):
            response = True
            break
        else: response = False
    return response

def RaiseChannelError(channelId, response):
    mensagem = "Não é permitido enviar comandos nesse canal"
    if response == False:
        Envia_Msg(channelId, mensagem)
        raise ValueError("Canal fora da Whitelist")

def Envia_Msg(channelId, mensagem):
    channel = client.get_channel(channelId)
    client.loop.create_task(channel.send(mensagem))

def Envia_Arquivo(channel_id, arquvio):
    pass

#Código para executar o Bot com as configurações pré-definidas
client.run(token)