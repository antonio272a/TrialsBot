import discord
import pyrez
import asyncio
import json
from json import JSONEncoder


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

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
        retorno = RefatorandoCmdMods(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        PegarStats(match_id, game)
        with open("teste.txt", 'rb') as file:
            await message.channel.send(file=discord.File(file, "Stats.txt"))

    if message.content.find(".id") != -1: #Retorna resultado da partida e ID dos players
        await message.channel.send(content="Comando recebido", embed=None)
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarId(match_id, game)
        Envia_Msg(channelId, details_players)

    if message.content.find(".replay") != -1: #Retorna se possui replay ou não
        await message.channel.send(content="Comando recebido", embed=None)
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem)
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarReplay(match_id, game)
        Envia_Msg(channelId, details_players)

    if message.content.find(".addthischannel") != -1:
        await message.channel.send("Comando recebido")
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id)
        AddChannelIdWhitelist(channel_id, channel_id)
        Envia_Msg(channel_id, "Canal adicionado com Sucesso")

    if message.content.find(".removethischannel") != -1:
        await message.channel.send("Comando recebido")
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id)
        RemoveChannelIdWhitelist(channel_id, channel_id)
        Envia_Msg(channel_id, "Canal removido com sucesso")

    if message.content.find(".removechannelid") != -1:
        await message.channel.send("Comando recebido")
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id)
        removed_channel_id = ReconhecerComando(mensagem, ".removechannelid ")
        RemoveChannelIdWhitelist(channel_id, removed_channel_id)
        Envia_Msg(channel_id, "Canal removido com sucesso")

    if message.content.find(".addchannelid") != -1:
        await message.channel.send("Comando recebido")
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id)
        added_channel_id = ReconhecerComando(mensagem, ".addchannelid ")
        AddChannelIdWhitelist(channel_id, added_channel_id)
        Envia_Msg(channel_id, "Canal adicionado com sucesso")

    if message.content.find(".teste") != -1:
        await message.channel.send(".addthischannel")

#Funções
def RefatorandoCmdMods(channel_id, mensagem ):
    ConfereDiscId(channel_id)
    retorno = ReconheceJogo(channel_id, mensagem)
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

def ConfereUserId(user_id, channel_id):
    whitelist = []
    with open("user_id_whitelist.txt", "r") as whitelist_doc:
        for linha in whitelist_doc.readlines():
            nova_linha = linha.replace("\n", "")
            whitelist.append(nova_linha)
        whitelist_doc.close()
    for channel in whitelist:
        if channel == str(user_id):
            response = True
            break
        else:
            response = False
    RaiseUserError(channel_id, response)

def ConfereDiscId(channel_id):
    DiscIdWhitelist = []
    with open ("channel_whitelist.txt", "r+") as whitelist_doc:
        for linha in whitelist_doc.readlines():
            nova_linha = linha.replace("\n", "")
            DiscIdWhitelist.append(nova_linha)
        whitelist_doc.close()
    for channel in DiscIdWhitelist:
        if channel == str(channel_id):
            response = True
            break
        else: response = False
    RaiseChannelError(channel_id, response)

def AddChannelIdWhitelist(channel_id, added_channelid):
    DiscIdWhitelist = []
    with open("channel_whitelist.txt", "r") as whitelist_doc:
        for linha in whitelist_doc.readlines():
            nova_linha = linha.replace("\n", "")
            DiscIdWhitelist.append(nova_linha)
        whitelist_doc.close()
    for channel in DiscIdWhitelist:
        if channel == str(added_channelid):
            response = True
            break
        else: response = False
    if response:
        Envia_Msg(channel_id, "Canal já presente na Whitelist")
        raise ValueError("Canal já presente na Whitelist")
    with open("channel_whitelist.txt", "a") as whitelist_doc:
        whitelist_doc.write(str(added_channelid) + "\n")

def RemoveChannelIdWhitelist(channel_id, removed_channe_id):
    index = 0
    with open("channel_whitelist.txt", "r") as whitelist_doc:
        new_whitelist = whitelist_doc.readlines()
        whitelist_doc.close()
    for linha in new_whitelist:
        if linha.strip("\n") == str(removed_channe_id):
            del new_whitelist[index]
            response = True
            break
        else:
            index += 1
            response = False
    if not response:
        mensagem = "Canal não está na Whitelist"
        Envia_Msg(channel_id, mensagem)
        raise ValueError("Canal não encontrado na Whitelist")
    with open ("channel_whitelist.txt", "w") as whitelist_doc:
        for linha in new_whitelist:
            whitelist_doc.write(linha)
    whitelist_doc.close()

def RaiseUserError(channel_id, response):
    mensagem = "Você não tem permissão para usar esse comando"
    if not response:
        Envia_Msg(channel_id, mensagem)
        raise ValueError("Usuário sem permissão")

def RaiseChannelError(channelId, response):
    mensagem = "Não é permitido enviar comandos nesse canal"
    if not response:
        Envia_Msg(channelId, mensagem)
        raise ValueError("Canal fora da Whitelist")

def Envia_Msg(channelId, mensagem):
    channel = client.get_channel(channelId)
    client.loop.create_task(channel.send(mensagem))

def Envia_Arquivo(channel_id, arquvio): #Em desenvolvimento
    pass



'''match_inf = paladins_req.getMatch(1086507338)
#print(CustomEncoder().encode(match_inf))
match_infJSONData = json.dumps(match_inf, indent=4, cls=CustomEncoder)
print(type(match_infJSONData))
match_infJSON = json.loads(match_infJSONData)
print(match_infJSON)
print(type(match_infJSON))
with open("StatsJson.txt", "w") as jsonFile:
    json.dump(match_infJSON, jsonFile)'''

#Código para executar o Bot com as configurações pré-definidas
client.run(token)