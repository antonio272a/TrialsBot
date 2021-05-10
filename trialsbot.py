import discord
import pyrez
import asyncio
import json
from json import JSONEncoder
from imgcreation import CreatePaladinsStatsImg

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
async def on_ready():
    await client.change_presence(activity = discord.Game(name=".help"))

@client.event

async def on_message(message): #Ao receber mensagem

    if message.content == ".help":

        embed = discord.Embed(title="Central de Ajuda do TrialsBot", description='Alguns comandos para facilitar a moderação \n Lembrando que todos os comando devem ser seguidos por pelo jogo com o "-jogo", por exemplo: \n'
                                                                                 '.stats-paladins ou .stats-smite')
        embed.add_field(name=".stats", value="Retorna o arquivo de texto com todos os stats da partida")
        embed.add_field(name=".id", value="Retorna os Id's de todos os jogadores, com exceção dos perfil privados")
        embed.add_field(name=".replay", value="Renorna os players da partida pra conferência, junto com a informação de caso a partida tenha Replay ou não")
        embed.add_field(name=".image (Pré-alpha)", value="Retorna a imagem dos stats da partida")
        await message.channel.send(content=None, embed=embed)

    if message.content.find(".image") != -1: #Retona imagem dos resultados
        await message.channel.send(content="Comando recebido", embed=None) #Colocado sem função por agilidade no envio
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem) #Função para simplificar o código
        match_id = retorno[1]
        CriaPaladinsImagemStats(match_id) #3Cria as imagens e salva
        with open("./createdimages/Teste.png", 'rb') as file: #4Envia arquivo no discord
            await message.channel.send(file=discord.File(file, "Image.png"))
        file.close()

    if message.content.find(".stats") != -1: #Retorna stats.txt no discord
        await message.channel.send(content="Comando recebido", embed=None) #Colocado sem função por agilidade no envio
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem) #Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        PegarStats(match_id, game) #Retona os stas em um arquivo Stats.txt
        with open("Stats.txt", 'rb') as file:
            await message.channel.send(file=discord.File(file, "Stats.txt")) #4
        file.close()

    if message.content.find(".id") != -1: #Retorna resultado da partida e ID dos players
        await message.channel.send(content="Comando recebido", embed=None) #Colocado sem função por agilidade no envio
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem) #Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarId(match_id, game) #Retorna a mensagem já formulada para envio
        Envia_Msg(channelId, details_players) #Envia mensagem no canal remetente do discord

    if message.content.find(".replay") != -1: #Retorna se possui replay ou não
        await message.channel.send(content="Comando recebido", embed=None) #Colocado sem função por agilidade no envio
        mensagem = message.content
        channelId = message.channel.id
        retorno = RefatorandoCmdMods(channelId, mensagem) #Função para simplificar o código
        game = retorno[0]
        match_id = retorno[1]
        details_players = PegarReplay(match_id, game) #Retorna a mensagem já formulada para envio
        Envia_Msg(channelId, details_players) #Envia mensagem no canal remetente do discord

    if message.content.find(".addthischannel") != -1: #Adiciona o canal remetente na whitelist
        await message.channel.send("Comando recebido") #Colocado sem função por agilidade no envio
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id) #Confere o Id do User
        AddChannelIdWhitelist(channel_id, channel_id) #adiciona o canal à whitelist
        Envia_Msg(channel_id, "Canal adicionado com Sucesso") #Envia mensagem no canal remetente do discord

    if message.content.find(".removethischannel") != -1: #Remove o canal remetente da Whitelist
        await message.channel.send("Comando recebido") #Colocado sem função por agilidade no envio
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id) #Confere o Id do User
        RemoveChannelIdWhitelist(channel_id, channel_id) #Remove o canal da Whitelist
        Envia_Msg(channel_id, "Canal removido com sucesso") #Envia mensagem no canal remetente do discord

    if message.content.find(".removechannelid") != -1: #Remove o id de canal informado da whitelist
        await message.channel.send("Comando recebido") #Colocado sem função por agilidade no envio
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id) #Confere o Id do User
        removed_channel_id = ReconhecerComando(mensagem, ",removechannelid ") #Trata a mensagem para ficar só o ID do canal
        RemoveChannelIdWhitelist(channel_id, removed_channel_id) #Remove o canal da Whitelis
        Envia_Msg(channel_id, "Canal removido com sucesso") #Envia mensagem no canal remetente do discord

    if message.content.find(".addchannelid") != -1: #Adiciona o Id do canal informado à Whitelist
        await message.channel.send("Comando recebido") #Colocado sem função por agilidade no envio
        mensagem = message.content
        user_id = message.author.id
        channel_id = message.channel.id
        ConfereUserId(user_id, channel_id) #Confere o Id do User
        added_channel_id = ReconhecerComando(mensagem, ",addchannelid ") #Trata a mensagem para ficar só o ID do canal
        AddChannelIdWhitelist(channel_id, added_channel_id) #adiciona o canal à whitelist
        Envia_Msg(channel_id, "Canal adicionado com sucesso") #Envia mensagem no canal remetente do discord

    if message.content.find(".teste") != -1: #Testa se o Id de usuário está sendo conferido
        await message.channel.send(".addthischannel")

#Funções
def RefatorandoCmdMods(channel_id, mensagem):
    ConfereDiscId(channel_id) #Confere o Id do canal
    retorno = ReconheceJogo(channel_id, mensagem) #Retorna a requisição e a str do comando sem o match_id
    game = retorno[0]
    comando = retorno[1]
    match_id = ReconhecerComando(mensagem, comando) #Retira o comando da mensagem, sobrando só o match_id
    retorno = [game, match_id]
    return retorno

def ReconhecerComando(mensagem, content):
    input_comando = mensagem
    output_comando = input_comando.replace(content, "") #Retira o comando, deixando somente o Id enviado
    return output_comando

def ReconheceJogo (channel_id, mensagem):
    comandos = [".id", ".stats", ".replay", ".image"]
    jogos = {"smite": smite_req, "paladins": paladins_req}
    for jogo in jogos: #Percorre a lista de jogos instanciados acima
        if mensagem.find(jogo) != -1: #Se achar o jogo dentro da mensagem
            game = jogos[jogo] #requisição do jogo guardada dentro da variável game
            str_jogo = jogo #str do jogo que vai ser usada para limpar a mensagem em seguida
            break
        else:
            game = "Error" #Se não achar o jogo no comando, a variável fica com Str Error
            str_jogo = "" #para poder levantar o erro em seguida
    for command in comandos: #Percorre a lista de comandos
        if mensagem.find(command) != -1: #Se achar o comando dentro da mensagem
            str_comando = command
            comando = str_comando + "-" + str_jogo + " " #str que será retirada da mensagem para extrair o Id
            break
    mensagem = "Comando incorreto, o comando sempre deve ser acompanhado pelo jogo, detalhes em .help"
    retorno = [game, comando]
    if game == "Error": #Se o jogo não for encontrado na mensagem, ele retorna um aviso pro User e um erro
        Envia_Msg(channel_id, mensagem)
        raise LookupError("Comando não acompanhado pelo jogo")

    return retorno

def PegarId(match_id, game):
    match_inf = game.getMatch(match_id) #Instancia as informações da partida
    details_players = ""
    index = 0 #Index usado para separar os times
    for details in match_inf: #Confere se a conta do player é privada, nome retorna vazio
        if details["playerName"] == "":
            playerName = "Privado" #Troca nome vazio
        else:
            playerName = details["playerName"]
        if details["playerId"] == "0": #Confere se a conta é privada, Id retorna 0
            playerId = "Privado" #Troca Id 0
        else:
            playerId = details["playerId"]
        details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + playerName + " - " + "Campeão: " + \
                            details["Reference_Name"] + " - " + "id: " + playerId #Adiciona stats na mensagem
        index += 1
        if index == 5: details_players += "\n" + "\n" + "--------------------" + "\n"
        #Se passar de 5 players, ele separa com a str acima para separar os times
    return details_players

def PegarReplay(match_id, game):
    match_inf = game.getMatch(match_id) #Instancia informações da partida
    details_players = ""
    index = 0 #index para separar os times
    for details in match_inf:
        if details["playerName"] == "": #Confere se a conta do player é privada, nome retorna vazio
            playerName = "Privado" #Troca nome vazio
        else:
            playerName = details["playerName"]
        if details["playerId"] == "0": #Confere se a conta é privada, Id retorna 0
            playerId = "Privado" #Troca Id 0
        else:
            playerId = details["playerId"]
        details_players += "\n" + details["Win_Status"] + " - " + "Nick: " + playerName #Passa quem venceu e os nicks
        index += 1
        if index == 5: details_players += "\n" + "\n" + "--------------------" + "\n" #Separa os times
    for details in match_inf:
        if details["hasReplay"] == "y": #Confere se tem replay
            stats_replay = "Possui Replay"
            break
        else:
            stats_replay = "Não possui Replay"
    details_players += "\n" + stats_replay #Adiciona a informação se tem replay ou não
    return details_players

def PegarStats(match_id, game):
    match_inf = game.getMatch(match_id) #instancia informações da partida
    with open("Stats.txt", 'w', encoding="UTF-8") as log:
        for lista in match_inf: #Pra cada player dentro das infos
            log.write('\n' + '\n' + '************************************' + '\n') #Separa os players
            for dict in lista: #Pra cada info dentro dos players
                log.write('\n' + str(dict) + ' - ' + str(lista[dict])) #escreve info no doc
    log.close()

def ConfereUserId(user_id, channel_id):
    whitelist = []
    with open("./whitelists/user_id_whitelist.txt", "r") as whitelist_doc:
        for linha in whitelist_doc.readlines(): #Percorre as linhas do doc de Whitelist
            nova_linha = linha.replace("\n", "") #Trata a linha do doc
            whitelist.append(nova_linha) #Adiciona a linha do doc na lista
        whitelist_doc.close()
    for channel in whitelist: #Pra cada User presente no doc
        if channel == str(user_id): #Confere se o Id do Usuario está na Whitelist
            response = True #Se tiver, retorna True
            break
        else:
            response = False #Se não tiver, retorna False
    RaiseUserError(channel_id, response) #Caso seja False, essa função sobe um erro

def ConfereDiscId(channel_id):
    DiscIdWhitelist = []
    with open("./whitelists/channel_whitelist.txt", "r+") as whitelist_doc:
        for linha in whitelist_doc.readlines(): #Percorre as linhas do doc de Whitelist
            nova_linha = linha.replace("\n", "") #Trata a linha do doc
            DiscIdWhitelist.append(nova_linha) #Adiciona a linha do doc na lista
        whitelist_doc.close()
    for channel in DiscIdWhitelist: #Pra cada Canal presente no doc
        if channel == str(channel_id): #Confere se o Id do canal está na Whitelist
            response = True #Se tiver, retorna True
            break
        else: response = False #Se não tiver, retorna False
    RaiseChannelError(channel_id, response) #Caso seja False, essa função sobe um erro

def AddChannelIdWhitelist(channel_id, added_channelid):
    DiscIdWhitelist = [] #Até o comentário seguinte, o código só confere se o Id já está presente na lista para maiores detalhes confira os comandos ConfereDiscID ou ConfereUserId
    with open("./whitelists/channel_whitelist.txt", "r") as whitelist_doc:
        for linha in whitelist_doc.readlines():
            nova_linha = linha.replace("\n", "")
            DiscIdWhitelist.append(nova_linha)
        whitelist_doc.close()
    for channel in DiscIdWhitelist:
        if channel == str(added_channelid):
            response = True
            break
        else: response = False
    if response: #Se retornar True (Canal já presente na whitelist)
        Envia_Msg(channel_id, "Canal já presente na Whitelist") #Avisa o usuário
        raise ValueError("Canal já presente na Whitelist") #Levanta erro para evitar a duplicação de Id's
    with open("./whitelists/channel_whitelist.txt", "a") as whitelist_doc:
        whitelist_doc.write(str(added_channelid) + "\n") #Caso contrário, adiciona o Id

def RemoveChannelIdWhitelist(channel_id, removed_channe_id):
    index = 0  #Index para saber qual linha excluir
    with open("./whitelists/channel_whitelist.txt", "r") as whitelist_doc:
        new_whitelist = whitelist_doc.readlines() #cria lista com todas as linhas do doc
        whitelist_doc.close()
    for linha in new_whitelist: #pra cada linha(Id) na lista nova
        if linha.strip("\n") == str(removed_channe_id): #se a linha for igual ao Id a ser removido
            del new_whitelist[index] #Deleta o Id da lista
            response = True
            break
        else:
            index += 1
            response = False
    if not response: #Caso o canal não esteja na Whitelist
        mensagem = "Canal não está na Whitelist"
        Envia_Msg(channel_id, mensagem) #avisa o usuário
        raise ValueError("Canal não encontrado na Whitelist") #Levanta erro
    with open ("./whitelists/channel_whitelist.txt", "w") as whitelist_doc:
        for linha in new_whitelist: #Caso contrário, ele escreve por cima do Doc antigo com a lista sem o Id removido.
            whitelist_doc.write(linha)
    whitelist_doc.close()

def RaiseUserError(channel_id, response):
    #Recebe True ou False dos comandos, caso seja False, avisa o usuário do Erro e levanta erro)
    mensagem = "Você não tem permissão para usar esse comando"
    if not response:
        Envia_Msg(channel_id, mensagem)
        raise ValueError("Usuário sem permissão")

def RaiseChannelError(channelId, response):
    #Recebe True ou False dos comandos, caso seja False, avisa o usuário do Erro e levanta erro)
    mensagem = "Não é permitido enviar comandos nesse canal"
    if not response:
        Envia_Msg(channelId, mensagem)
        raise ValueError("Canal fora da Whitelist")

def Envia_Msg(channelId, mensagem):
    #Função para facilitar o envio de mensagens pelo bot por meio de funções não assíncronas
    channel = client.get_channel(channelId)
    client.loop.create_task(channel.send(mensagem))

def Envia_Arquivo(channel_id, arquvio): #Em desenvolvimento
    pass

def CriaPaladinsImagemStats(match_id):
    champions = paladins_req.getChampions() #Instancia lista de campeões
    itens = paladins_req.getItems() #Instancia lista de itens
    iconsId_list = []
    stats_list = []
    match_inf = paladins_req.getMatch(match_id) #Instancia os stats da partida
    stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned", "Damage_Player", "Healing"]
    #Acima é a lista dos stats que serão passados para colagem
    for player in match_inf: #Pra cada jogador, adiciona Id de champ na lista
        iconsId_list.append(player["ChampionId"])
        for stat in stats_reference: #Pra cada stat na referência, adiciona o stat na lista
            stats_list.append(player[stat])
    CreatePaladinsStatsImg(iconsId_list, stats_list, champions, itens) #Passa as infos pra outro arquivo montar a imagem

#Código para executar o Bot com as configurações pré-definidas
client.run(token)