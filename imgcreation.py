from PIL import Image, ImageDraw, ImageFont
import urllib
import urlopen
import io


"""
Funções que transformam a URL em Imagem:

1 - forma_img_1x1 - (Para colagens quadradas, ex.: 96x96px
2 - forma_img 2x1 - (Para colagens com proporção 2x1, ex.: colagem dos ícones do Paladins 96x48px
"""


def forma_img_1x1(url):
    header = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, None, header)
    url = urllib.request.urlopen(req, timeout=100)
    imgbytes = io.BytesIO(url.read())
    img = Image.open(imgbytes)
    return img


def forma_img_2x1(url):
    header = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, None, header)
    url = urllib.request.urlopen(req, timeout=100)
    imgbytes = io.BytesIO(url.read())
    full_img = Image.open(imgbytes)
    img = full_img.crop((0, 140, 512, 396))
    return img


"""
Função que serve para pegar o ID dos campeões/gods e com isso, retornar a URL pela API da Hi-rez:
Obs. 1: serve para Paladins e Smite
Obs. 2: O jogo é diferenciado pela variável game, que é o nome do jogo em uma string

1 - pega_stat_img
"""


def pega_stat_img(game, stat_id, champions, itens):
    if game == "paladins":
        for champ in champions:
            if champ["id"] == stat_id:
                url = champ["ChampionIcon_URL"]
                ischampions = True
                try:
                    img = forma_img_2x1(url)
                    return img
                except:
                    pass
                break
            else:
                ischampions = False
    elif game == "smite":
        for champ in champions:
            if champ["id"] == stat_id:
                url = champ["godIcon_URL"]
                try:
                    img = forma_img_1x1(url)
                    return img
                except:
                    pass
                break
            else:
                ischampions = False
    if not ischampions:
        for item in itens:
            if item["ItemId"] == stat_id:
                url = item["itemIcon_URL"]
                break
        try:
            img = forma_img_1x1(url)
            return img
        except:
            pass


"""
Funções para colagem de stats ou ícones na imagem:
Obs. 1: serve para Paladins e Smite
Obs. 2: O jogo é diferenciado pela variável game, que é o nome do jogo em uma string

1 - itens_paste (Só no Paladins por enquanto)
2 - icons_paste
3 - stats_paste
4 - teams_paste (Só no Paladins por enquanto)
5 - nicks_paste (Só no Smite por enquanto)
"""


def itens_paste(game, stat_id_list, bkg, champions, itens):
    # Igonorar por enquanto, função sem uso, necessita criar uma nova imagem e mudar todas as dimensões
    if game == "paladins":
        collum_count = 0
        box = [144, 172]
        length = 40
        line_count = 0
        count = 10
        size = (48, 48)
        for stat_id in stat_id_list:
            if collum_count == count:
                collum_count = 0
                line_count += 1
            new_box = [box[0] + length * collum_count, box[1] + 48 * line_count]
            try:
                stat_img = pega_stat_img(game, stat_id, champions, itens)
                stat_img = stat_img.resize(size)
                bkg.paste(stat_img, new_box)
            except:
                pass
            collum_count += 1
    elif game == "smite":
        pass  # Em breve


def icons_paste(game, icon_id_list, bkg, champions, itens):
    if game == "paladins":
        box = [100, 134]  # Aonde os ícones vão começar a ser colados
        line_count = 0  # Contagem de linhas, para fazer o espaçamento
        size = (96, 48)  # Tamano que os ícones serão dimensionados
        height = 60  # Altura entre um ícone e outro
        for icon_id in icon_id_list:  # Passa entre todos os ids dos ícones
            if line_count == 5:  # Quando a linha for 5, ou seja, quando passar para o outro time
                box[1] += 12  # Espaço a mais entre um time e outro
            new_box = [box[0], box[1] + height * line_count]  # Cria a box de colagem levando em conta as linhas
            icon_img = pega_stat_img(game, icon_id, champions, itens)  # Transforma o Id em imagem pela função
            icon_img = icon_img.resize(size)  # Redimensiona a imagem
            bkg.paste(icon_img, new_box)  # Cola na imagem base
            line_count += 1
    elif game == "smite":
        box = [350, 60]  # Aonde os ícones vão começar a ser colados
        collum_count = 0  # Contagem de colunas, para fazer o espaçamento
        size = (96, 96)  # Tamano que os ícones serão dimensionados
        lenght = 100  # Distância horizontal entre um ícone e outro
        for icon_id in icon_id_list:  # Passa entre todos os ids dos ícones
            if collum_count == 5:  # Quando a coluna for 5, ou seja, quando passar para o outro time
                box[0] += 62  # Espaço a mais entre um time e outro
            new_box = [box[0] + lenght * collum_count, box[1]]  # Cria a box de colagem levando em conta as colunas
            icon_img = pega_stat_img(game, icon_id, champions, itens)  # Transforma o Id em imagem pela função
            icon_img = icon_img.resize(size)  # Redimensiona a imagem
            bkg.paste(icon_img, new_box)  # Cola na imagem base
            collum_count += 1


def teams_paste(game, teams_list, bkg):
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)  # Define a fonte do stat
    draw = ImageDraw.Draw(bkg)  # Método para "desenhar" o stat na imagem
    if game == "paladins":
        start_box = [220, 150]  # Aonde os times vão começar a ser colados
        line_count = 0  # Contagem de linhas, para fazer o espaçamento
        index = 0  # index para poder saber quando trocar de um time pro outro e quando parar de colar os times

        while index < 10:  # Vai até o index chegar em 9, aonde ele terá feito as 10 colagens
            if index < 5:  # Se o index for menor que 5, ainda estará no time vencedor
                team = teams_list[0]
            else:  # Caso seja maior ou igual a 5, cola o time perdedor
                team = teams_list[1]
            if index == 5:  # Quando chegar no sexto player (Primeiro do time perdedor)
                start_box[1] += 12  # Dá o espaçamento entre os times
            index += 1
            box = [start_box[0], start_box[1] + 60 * line_count]  # Cria a box de colagem
            draw.text(box, str(team), (255, 255, 255), font)  # Desenha o time na imagem
            line_count += 1
    elif game == "smite":
        pass  # Em breve


def stats_paste(game, stats_list, bkg):
    line_count = 0  # Contagem de linhas para espaçamento
    collum_count = 0  # Contagem de colunas para espaçamento
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)  # Define a fonte do stat
    draw = ImageDraw.Draw(bkg)  # Método para "desenhar" o stat na imagem
    if game == "paladins":
        length = [0, 296, 422, 548, 623, 712, 832, 952]  # As distâncias horizontais entres os stats
        count = 8  # Contagem total de stats para saber quando passar para o próximo player
        start_box = [300, 153]  # Aonde os stats vão começar a ser colados
        for stat in stats_list:  # percorre todos os stats (str)
            plus = 0  # Número para centralizar os stats de kda
            if line_count == 4 and collum_count == 8:  # Quando passar de um time pro outro
                start_box[1] += 12  # Coloca o espaçamento entre os times
            if collum_count == count:  # Quando chega no último stat do player
                collum_count = 0  # Reseta a contagem de colunas
                line_count += 1  # Passa pro próximo player
            if collum_count == 2:
                # If's para verificar comprimento do kda para centralizar
                if len(stat) == 7:
                    plus = 5
                elif len(stat) == 6:
                    plus = 10
                elif len(stat) == 5:
                    plus = 13
            box = [start_box[0] + length[collum_count] + plus, start_box[1] + 60 * line_count]  # Cria a box de colagem
            draw.text(box, str(stat), (0, 0, 0), font)  # Desenha o stat
            collum_count += 1
    elif game == "smite":
        length = 100  # A distância horizontal entres os stats
        height = 44  # A distância vertical entre os players
        count = 11  # Número de stats por player
        start_box = [398, 254]  # Aonde os stats vão começar a ser colados
        for stat in stats_list:  # percorre todos os stats (str)
            if line_count == count:  # Quando chega no último stat do player
                collum_count += 1  # Passa pra póxima coluna
                line_count = 0  # Reseta a contagem de linhas
                if collum_count == 5:  # Quando chegar no primeiro player do próximo time
                    start_box[0] += 62  # Colcoa a distância entre os times
            box = [start_box[0] + length * collum_count, start_box[1] + height * line_count]
            # reference: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
            # Cria o box de colagem
            draw.text(box, str(stat), (0, 0, 0), font, anchor="mb")  # Desenha o stat na imagem
            line_count += 1


def nicks_paste(game, nicks_list, bkg):
    if game == "paladins":
        pass  # Não necessário até o momento

    elif game == "smite":
        collum_count = 0  # Contagem de colunas para fazer o espaçamento
        length = 100  # Distância horizontal entre os nomes
        start_box = [397, 198]  # Aonde os nomes vão começar a ser colados
        draw = ImageDraw.Draw(bkg)  # Método para "desenhar" o stat na imagem
        font_comparacao = ImageFont.truetype("./fonts/Arial.ttf", 12)
        for nick in nicks_list:  # Pra cada nick na lista
            if draw.textsize(nick, font=font_comparacao)[0] > 96:  # Define a fonte dos nicks
                font = ImageFont.truetype("./fonts/Arial.ttf", 10)
            else:
                font = ImageFont.truetype("./fonts/Arial.ttf", 12)
            if collum_count == 5:  # Quando chegar no sexto player, ou seja, primeiro jogador do time perdedor
                start_box[0] += 62  # Distância entre os times
            box = (start_box[0] + length * collum_count, start_box[1])  # Cria a box para colagem
            draw.text(box, str(nick), (255, 255, 255), font, anchor="mb")  # Desenha na imagem
            collum_count += 1

"""
Função que é importada pelo arquivo principal para criar as imagens
Obs. 1: serve para Paladins e Smite
Obs. 2: O jogo é diferenciado pela variável game, que é o nome do jogo em uma string

1 - create_stats_img
"""


def create_stats_img(game, icons_id_list, nicks_list, stats_list, teams_list, champions, itens):
    if game == "paladins":
        bkg = Image.open("./images/bkg-paladins.png")  # Abre a imagem
        icons_paste(game, icons_id_list, bkg, champions, itens)  # Cola os ícones
        teams_paste(game, teams_list, bkg)  # Cola os times
        stats_paste(game, stats_list, bkg)  # Cola os stats e os nomes
        bkg.save("./createdimages/Teste-paladins.png")  # Salva em um arquivo novo, substituindo o antigo

    elif game == "smite":
        bkg = Image.open("./images/bkg-smite.png")  # Abre a imagem
        icons_paste(game, icons_id_list, bkg, champions, itens)  # Cola os ícones
        nicks_paste(game, nicks_list, bkg)  # Cola os nicks
        stats_paste(game, stats_list, bkg)  # Cola os stats
        bkg.save("./createdimages/Teste-smite.png")  # Salva em um arquivo novo, substituindo o antigo


# lista_stats = [] stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned",
# "Damage_Player", "Healing"] stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned",
# "Damage_Player", "Healing"] itens_reference = ["ItemId1", "ItemId2", "ItemId3", "ItemId4", "ItemId5", "ItemId6",
# "ActiveId1", "ActiveId2", "ActiveId3", "ActiveId4"] match_inf = paladins_req.getMatch(match) for player in
# match_inf: for item in itens_reference: lista_stats.append(player[item])

# #stats: [playerName]
# champion: [ChampionId] - [Deaths] - [Assists] - [Gold_Earned]
# baralho: [ItemId1 -> 6] (6 = lendária) - [ItemLevel1 -> 5]
# itens: [ActiveId1 -> 4] - [ActiveLevel1 ->4]
