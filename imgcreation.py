from PIL import Image, ImageDraw, ImageFont
import urllib
import urlopen
import io


def forma_img(url):
    header = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, None, header)
    url = urllib.request.urlopen(req, timeout=100)
    imgbytes = io.BytesIO(url.read())
    full_img = Image.open(imgbytes)
    img = full_img.crop((0, 140, 512, 396))
    return img

# Paladins functions
def paladins_pega_stat_img(stat_id, champions, itens):
    for champ in champions:
        if champ["id"] == stat_id:
            url = champ["ChampionIcon_URL"]
            break
        else:
            ischampions = False
    if not ischampions:
        for item in itens:
            if item["ItemId"] == stat_id:
                url = item["itemIcon_URL"]
                break
    try:
        img = forma_img(url)
        return img
    except:
        pass


def paladins_itens_paste(stat_id_list, bkg, champions, itens):
    collum_count = 0
    box = [144, 172]
    length = 40
    line_count = 0
    count = 10
    size = (48, 24)
    for stat_id in stat_id_list:
        if collum_count == count:
            collum_count = 0
            line_count += 1
        new_box = [box[0] + length * collum_count, box[1] + 48 * line_count]
        try:
            stat_img = pega_stat_img(stat_id, champions, itens)
            stat_img = stat_img.resize(size)
            bkg.paste(stat_img, new_box)
        except:
            pass
        collum_count += 1


def paladins_icons_paste(icon_id_list, bkg, champions, itens):
    box = [40, 100]
    line_count = 0
    size = (96, 48)
    height = 60
    for icon_id in icon_id_list:
        if line_count == 5:
            box[1] += 12
        new_box = [box[0], box[1] + height * line_count]
        icon_img = paladins_pega_stat_img(icon_id, champions, itens)
        icon_img = icon_img.resize(size)
        bkg.paste(icon_img, new_box)
        line_count += 1


def paladins_teams_paste(teams_list, bkg):
    start_box = [176, 116]
    line_count = 0
    index = 0
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)
    draw = ImageDraw.Draw(bkg)
    while index < 10:
        if index < 5:
            team = teams_list[0]
        else:
            team = teams_list[1]
        if index == 5:
            start_box[1] += 12
        index += 1
        box = [start_box[0], start_box[1] + 60 * line_count]
        draw.text(box, str(team), (255, 255, 255), font)
        line_count += 1


def paladins_stats_paste(stats_list, bkg):
    line_count = 0
    collum_count = 0
    length = [0, 276, 392, 528, 588, 692, 812, 932]
    count = 8
    start_box = [260, 116]
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)
    draw = ImageDraw.Draw(bkg)
    for stat in stats_list:
        if line_count == 4 and collum_count == 8:
            start_box[1] += 12
        if collum_count == count:
            collum_count = 0
            line_count += 1
        box = [start_box[0] + length[collum_count], start_box[1] + 60 * line_count]
        draw.text(box, str(stat), (255, 255, 255), font)
        collum_count += 1


def create_paladins_stats_img(icons_id_list, stats_list, teams_list, champions, itens):
    bkg = Image.open("./images/bkg.png")
    paladins_icons_paste(icons_id_list, bkg, champions, itens)
    paladins_teams_paste(teams_list, bkg)
    paladins_stats_paste(stats_list, bkg)
    bkg.save("./createdimages/Teste-paladins.png")

# Smite Functions

def smite_forma_img(url):
    header = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, None, header)
    url = urllib.request.urlopen(req, timeout=100)
    imgbytes = io.BytesIO(url.read())
    img = Image.open(imgbytes)
    return img


def smite_pega_stat_img(stat_id, champions, itens):
    for god in champions:
        if god["id"] == stat_id:
            url = god["godIcon_URL"]
            break
        else:
            ischampions = False
    try:
        if not ischampions:
            for item in itens:
                if item["ItemId"] == stat_id:
                    url = item["itemIcon_URL"]
                    break
    except:
        pass
    try:
        img = smite_forma_img(url)
        return img
    except:
        pass


def smite_icons_paste(icon_id_list, bkg, champions, itens):
    box = [162, 80]
    collum_count = 0
    size = (96, 96)
    lenght = 100
    for icon_id in icon_id_list:
        if collum_count == 5:
            box[0] += 84
        new_box = [box[0] + lenght * collum_count, box[1]]
        icon_img = smite_pega_stat_img(icon_id, champions, itens)
        icon_img = icon_img.resize(size)
        bkg.paste(icon_img, new_box)
        collum_count += 1


def smite_stats_paste(stats_list, bkg):
    line_count = 0
    collum_count = 0
    length = 100
    height = 44
    count = 11
    start_box = [190, 204]
    font = ImageFont.truetype("./fonts/Arial.ttf", 16)
    draw = ImageDraw.Draw(bkg)
    for stat in stats_list:
        if line_count == count:
            collum_count += 1
            line_count = 0
        if line_count == 0:
            lvl = 10
            if collum_count == 5:
                start_box[0] += 84
        box = [start_box[0] + length * collum_count + lvl, start_box[1] + height * line_count]
        draw.text(box, str(stat), (0, 0, 0), font)
        line_count += 1
        lvl = 0


def smite_nicks_paste(nicks_list, bkg):
    collum_count = 0
    length = 100
    start_box = [162, 180]
    font = ImageFont.truetype("./fonts/Arial.ttf", 12)
    draw = ImageDraw.Draw(bkg)
    for nick in nicks_list:
        if len(nick) <= 6:
            len_nick = 24
        elif len(nick) <=9:
            len_nick = 18
        elif len(nick) <= 12:
            len_nick = 12
        else:
            len_nick = 6
        if collum_count == 5:
            start_box[0] += 84
        box = [start_box[0] + length * collum_count + len_nick, start_box[1]]
        draw.text(box, str(nick), (0, 0, 0), font)
        collum_count += 1


def create_smite_stats_img(icons_id_list, nicks_list, stats_list, gods, itens):
    bkg = Image.open("./images/bkg-smite.png")
    smite_icons_paste(icons_id_list, bkg, gods, itens)
    smite_nicks_paste(nicks_list, bkg)
    smite_stats_paste(stats_list, bkg)
    bkg.save("./createdimages/Teste-smite.png")


# lista_stats = [] stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned",
# "Damage_Player", "Healing"] stats_reference = ["playerName", "Kills_Player", "Deaths", "Assists", "Gold_Earned",
# "Damage_Player", "Healing"] itens_reference = ["ItemId1", "ItemId2", "ItemId3", "ItemId4", "ItemId5", "ItemId6",
# "ActiveId1", "ActiveId2", "ActiveId3", "ActiveId4"] match_inf = paladins_req.getMatch(match) for player in
# match_inf: for item in itens_reference: lista_stats.append(player[item])
#
# for player in match_inf:
#     lista_champId.append(player["ChampionId"])

# bkg.save("./createdimages/Teste.png")

# #stats: [playerName]
# champion: [ChampionId] - [Deaths] - [Assists] - [Gold_Earned]
# baralho: [ItemId1 -> 6] (6 = lendária) - [ItemLevel1 -> 5]
# itens: [ActiveId1 -> 4] - [ActiveLevel1 ->4]


# """Cria imagens pra backup"""

# lista_champUrl = []
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
