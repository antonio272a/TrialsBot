from PIL import Image, ImageDraw, ImageFont
import urllib
import urlopen
import io

def FormaImg(url):
    header = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, None, header)
    url = urllib.request.urlopen(req, timeout=100)
    imgbytes = io.BytesIO(url.read())
    img = Image.open(imgbytes)
    return img

def PegaStatImg(statId, champions, itens):
    for champ in champions:
        if champ["id"] == statId:
            url = champ["ChampionIcon_URL"]
            break
        else: ischampions = False
    if not ischampions:
        for item in itens:
            if item["ItemId"] == statId:
                url = item["itemIcon_URL"]
                break
    try:
        img = FormaImg(url)
        return img
    except: pass

def ItensPaste(statId_list, bkg, champions, itens):
    collum_count = 0
    box = [144, 172]
    length = 40
    line_count = 0
    count = 10
    size = (32, 32)
    for statId in statId_list:
        if collum_count == count:
            collum_count = 0
            line_count +=1
        new_box = [box[0] + length*collum_count, box[1] + 48*line_count]
        stat_img = PegaStatImg(statId, champions, itens)
        try:
            stat_img = PegaStatImg(statId, champions, itens)
            stat_img = stat_img.resize(size)
            bkg.paste(stat_img, new_box)
        except: pass
        collum_count += 1

def IconsPaste(iconId_list, bkg, champions, itens):
    box = [144, 172]
    line_count = 0
    size = (32, 32)
    for iconId in iconId_list:
        new_box = [box[0], box[1] + 48*line_count]
        icon_img = PegaStatImg(iconId, champions, itens)
        icon_img = icon_img.resize(size)
        bkg.paste(icon_img, new_box)
        line_count += 1

def StatsPaste(stats_list, bkg):
    line_count = 0
    collum_count = 0
    length = [0, 192, 258, 327, 420, 511, 647]
    count = 7
    start_box = [223,180]
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)
    draw = ImageDraw.Draw(bkg)
    for stat in stats_list:
        if collum_count == count:
            collum_count = 0
            line_count += 1
        box = [start_box[0] + length[collum_count],start_box[1] + 48*line_count]
        draw.text(box, str(stat), (255, 255, 255), font)
        collum_count += 1

def CreatePaladinsStatsImg(iconsId_list, stats_list, champions, itens):
    bkg = Image.open("./images/bkg.png")
    IconsPaste(iconsId_list, bkg, champions, itens)
    StatsPaste(stats_list, bkg)
    bkg.save("./createdimages/Teste.png")




# lista_stats = []
# stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned", "Damage_Player", "Healing"]
# stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned", "Damage_Player", "Healing"]
# itens_reference = ["ItemId1", "ItemId2", "ItemId3", "ItemId4", "ItemId5", "ItemId6", "ActiveId1", "ActiveId2", "ActiveId3", "ActiveId4"]
# match_inf = paladins_req.getMatch(match)
# for player in match_inf:
#     for item in itens_reference:
#         lista_stats.append(player[item])
#
# for player in match_inf:
#     lista_champId.append(player["ChampionId"])

# bkg.save("./createdimages/Teste.png")

# #stats: [playerName]
# champion: [ChampionId] - [Deaths] - [Assists] - [Gold_Earned]
# baralho: [ItemId1 -> 6] (6 = lendária) - [ItemLevel1 -> 5]
# itens: [ActiveId1 -> 4] - [ActiveLevel1 ->4]



#"""Cria imagens pra backup"""

#lista_champUrl = []
# champions = paladins_req.getChampions()
# for champion in champions:
#      lista_champUrl.append(champion["ChampionIcon_URL"])
#      lista_champId.append(champion["id"])
# index = 0
# print("iniciando colagem")
# for url in lista_champUrl:
#     img = FormaImg(url)
#     print("Imagem ", index, " Criada")
#     index += 1
#     img.save("./champIcons/" + str(lista_champId[index]) + ".png")
#     print("Imagem ", index, " Salva")
