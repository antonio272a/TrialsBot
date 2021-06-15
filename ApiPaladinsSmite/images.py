from PIL import Image, ImageDraw, ImageFont
import urllib
import urlopen
import io

"""
PT-BR: Classes que criam as imagens de stats das partidas usando a biblioteca Pillow.
Obs.: São muitos detalhes nas colagens sobre espaçamento, então os comentários vão ser colocados em cada linha e
somente em português, para suporte em inglês, entre em contato com o discord antonio272#3304

EN-US: Classes that create game stat images using Pillow library.
Note: There are a lot of details on the images pasting about spacing, so the comments will be placed on each line and
on portuguese only, for support in english, contact discord antonio272#3304
"""


class ImgPaladins:

    def __init__(self, match_inf, champions, itens, winner_team, loser_team):
        self.match_inf = match_inf
        self.champions = champions
        self.itens = itens
        self.font = ImageFont.truetype("./Docs/Fonts/Arial.ttf", 16)
        self.kda_list = ["Kills_Player", "Deaths", "Assists"]
        self.icons_id_list = self._create_id_list()
        self.stats_list = self._create_stats_list()
        self.bkg = Image.open("./Images/Bases/bkg-paladins.png")
        self.teams_list = ["[" + winner_team + "]", "[" + loser_team + "]"]
        self.create_image()

    @staticmethod
    def _make_image_1x1(url):
        # Usa as bibliotecas urllib, urlopen, io e Pillow para retorna a imagem em proporção original
        header = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, None, header)
        url = urllib.request.urlopen(req, timeout=100)
        imgbytes = io.BytesIO(url.read())
        img = Image.open(imgbytes)
        return img

    @staticmethod
    def _make_image_2x1(url):
        # Corta a imagem para que ela fique na proporção 2x1, para ficar na proporção certa para resize e colagem
        header = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, None, header)
        url = urllib.request.urlopen(req, timeout=100)
        imgbytes = io.BytesIO(url.read())
        full_img = Image.open(imgbytes)
        if full_img.size == (256, 256):
            img = full_img.crop((0, 70, 256, 198))
        else:
            img = full_img.crop((0, 140, 512, 396))
        return img

    def _get_stat_image(self, stat_id):
        for champ in self.champions:  # Compara com o Id's dos campeões
            if champ["id"] == stat_id:  # Se achar
                url = champ["ChampionIcon_URL"]  # retorna a url do ícone
                ischampions = True  # Se for Tru
                try:
                    img = self._make_image_2x1(url)  # Retorna a imagem em 2x1 para ficar com o tamanho certo
                    return img
                except:
                    pass
                break
            else:
                ischampions = False
        if not ischampions:  # Caso não seja campeão, confere nos itens
            for item in self.itens:
                if item["ItemId"] == stat_id:  # Se achar
                    url = item["itemIcon_URL"]  # retorna a url da imagem do item
                    break
            try:
                img = self._make_image_1x1(url)  # retorna a imagem em tamanho original
                return img
            except:
                pass

    def _create_kda_list(self, player):
        index = 0  # index para saber qual informação do kda está sendo usada
        kda_stat = ""
        for stat in self.kda_list:
            if index != 1:  # Se não for o do meio, só printa o stat
                kda_stat += str(player[stat])
            else:  # Se for o do meio, printa as barras junto
                kda_stat += "/" + str(player[stat]) + "/"
            index += 1
        return kda_stat

    def _create_stats_list(self):
        stats_list = []
        stats_reference_1 = ["playerName", "Gold_Earned"]
        stats_reference_2 = ["Killing_Spree", "Objective_Assists", "Damage_Player", "Damage_Mitigated", "Healing"]
        for player in self.match_inf:  # Pra cada jogador
            for stat_1 in stats_reference_1:  # Pra cada stat na referência, adiciona o stat na lista
                stats_list.append(player[stat_1])
            stats_list.append(self._create_kda_list(player))  # Forma o texto do KDA e coloca na lista
            for stat_2 in stats_reference_2:
                stats_list.append(player[stat_2])  # Coloca o resto dos stats depois do KDA
        return stats_list

    def _create_id_list(self):
        icons_id_list = []
        for player in self.match_inf:  # Pra cada jogador
            icons_id_list.append(player["ChampionId"])  # adiciona Id do champ na lista
        return icons_id_list

    def _icons_paste(self):
        box = [100, 134]  # Aonde os ícones vão começar a ser colados
        line_count = 0  # Contagem de linhas, para fazer o espaçamento
        size = (96, 48)  # Tamano que os ícones serão dimensionados
        height = 60  # Altura entre um ícone e outro
        for icon_id in self.icons_id_list:  # Passa entre todos os ids dos ícones
            if line_count == 5:  # Quando a linha for 5, ou seja, quando passar para o outro time
                box[1] += 12  # Espaço a mais entre um time e outro
            new_box = [box[0], box[1] + height * line_count]  # Cria a box de colagem levando em conta as linhas
            icon_img = self._get_stat_image(stat_id=icon_id)  # Transforma o Id em imagem pela função
            icon_img = icon_img.resize(size)  # Redimensiona a imagem
            self.bkg.paste(icon_img, new_box)  # Cola na imagem base
            line_count += 1

    def _stats_paste(self):
        line_count = 0  # Contagem de linhas para espaçamento
        collum_count = 0  # Contagem de colunas para espaçamento
        draw = ImageDraw.Draw(self.bkg)  # Método para "desenhar" o stat na imagem
        length = [0, 296, 447, 548, 623, 712, 832, 952]  # As distâncias horizontais entres os stats
        count = 8  # Contagem total de stats para saber quando passar para o próximo player
        start_box = [300, 153]  # Aonde os stats vão começar a ser colados
        for stat in self.stats_list:  # percorre todos os stats (str)
            if line_count == 4 and collum_count == 8:  # Quando passar de um time pro outro
                start_box[1] += 12  # Coloca o espaçamento entre os times
            if collum_count == count:  # Quando chega no último stat do player
                collum_count = 0  # Reseta a contagem de colunas
                line_count += 1  # Passa pro próximo player
            box = [start_box[0] + length[collum_count], start_box[1] + 60 * line_count]  # Cria a box de colagem
            if collum_count == 2:  # Se for o KDA
                box[1] += 13
                draw.text(box, str(stat), (0, 0, 0), self.font, anchor="mb")  # Desenha o Kda centralizado
            else:
                draw.text(box, str(stat), (0, 0, 0), self.font)  # Desenha o stat
            collum_count += 1

    def _teams_paste(self):
        draw = ImageDraw.Draw(self.bkg)  # Método para "desenhar" o stat na imagem
        start_box = [220, 150]  # Aonde os times vão começar a ser colados
        line_count = 0  # Contagem de linhas, para fazer o espaçamento
        index = 0  # index para poder saber quando trocar de um time pro outro e quando parar de colar os times
        while index < 10:  # Vai até o index chegar em 9, aonde ele terá feito as 10 colagens
            if index < 5:  # Se o index for menor que 5, ainda estará no time vencedor
                team = self.teams_list[0]
            else:  # Caso seja maior ou igual a 5, cola o time perdedor
                team = self.teams_list[1]
            if index == 5:  # Quando chegar no sexto player (Primeiro do time perdedor)
                start_box[1] += 12  # Dá o espaçamento entre os times
            index += 1
            box = [start_box[0], start_box[1] + 60 * line_count]  # Cria a box de colagem
            draw.text(box, str(team), (255, 255, 255), self.font)  # Desenha o time na imagem
            line_count += 1

    def create_image(self):
        self._icons_paste()  # Cola os ícones
        self._teams_paste()  # Cola os times
        self._stats_paste()  # Cola os stats e os nomes
        self.bkg.save("./Images/Createdimages/paladins.png")  # Salva em um arquivo novo, substituindo o antigo


class ImgSmite:

    def __init__(self, match_inf, gods, itens):
        self.match_inf = match_inf
        self.gods = gods
        self.itens = itens
        self.font = ImageFont.truetype("./Docs/Fonts/Arial.ttf", 16)
        self.font_nicks = ImageFont.truetype("./Docs/Fonts/Arial.ttf", 12)
        self.font_menor_nicks = ImageFont.truetype("./Docs/Fonts/Arial.ttf", 10)
        self.kda_list = ["Kills_Player", "Deaths", "Assists"]
        self.icons_id_list = self._create_id_list()
        self.stats_list = self._create_stats_list()
        self.nicks_list = self._create_nicks_list()
        self.bkg = Image.open("./Images/Bases/bkg-smite.png")
        self.create_image()

    @staticmethod
    def _make_image_1x1(url):
        # Usa as bibliotecas urllib, urlopen, io e Pillow para retorna a imagem em proporção original
        header = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, None, header)
        url = urllib.request.urlopen(req, timeout=100)
        imgbytes = io.BytesIO(url.read())
        img = Image.open(imgbytes)
        return img

    def _get_stat_image(self, stat_id):
        for god in self.gods:  # Compara com os Id's dos gods
            if god["id"] == stat_id:  # se achar
                url = god["godIcon_URL"]  # retorna a url do ícone
                isgod = True
                try:
                    img = self._make_image_1x1(url)  # retona a imagem do ícone
                    return img
                except:
                    pass
                break
            else:
                isgod = False
        if not isgod:  # Se não for um god
            for item in self.itens:  # Compara o Id com os dos itens
                if item["ItemId"] == stat_id:  # se achar
                    url = item["itemIcon_URL"]  # Retorna a url da imagem do Item
                    break
            try:
                img = self._make_image_1x1(url)  # Retorna a imagem do ícone
                return img
            except:
                pass

    def _create_kda_list(self, player):
        index = 0  # index para saber qual informação do kda está sendo usada
        kda_stat = ""
        for stat in self.kda_list:
            if index != 1:  # Se não for o do meio, só printa o stat
                kda_stat += str(player[stat])
            else:  # Se for o do meio, printa as barras junto
                kda_stat += "/" + str(player[stat]) + "/"
            index += 1
        return kda_stat

    def _create_stats_list(self):
        stats_list = []
        stats_reference_1 = "Final_Match_Level"
        stats_reference_2 = ["Gold_Earned", "Gold_Per_Minute", "Damage_Player", "Damage_Bot", "Damage_Taken",
                             "Damage_Mitigated", "Structure_Damage", "Healing", "Wards_Placed"]
        for player in self.match_inf:  # Pra cada jogador
            stats_list.append(player[stats_reference_1])  # adiciona o stat na lista
            stats_list.append(self._create_kda_list(player))  # Forma o texto do KDA e coloca na lista
            for stat_2 in stats_reference_2:
                stats_list.append(player[stat_2])  # Coloca o resto dos stats depois do KDA
        return stats_list

    def _create_id_list(self):
        icons_id_list = []
        for player in self.match_inf:  # Pra cada jogador
            icons_id_list.append(player["GodId"])  # adiciona Id do god na lista
        return icons_id_list

    def _create_nicks_list(self):
        nicks_list = []
        for player in self.match_inf:  # Pra cada jogador
            if not player["playerName"]:  # Confere se o jogador possui número público
                if not player["hz_player_name"]:  # Tenta ver se tem conta da Hi-rez vinculada
                    player_name = ""  # Não conseguindo nenhum dos dois acima, deixa a string vazia
                else:
                    player_name = player["hz_player_name"]
            else:
                try:
                    player_name = player["playerName"][player["playerName"].find("]") + 1:]
                except:
                    player_name = player["playerName"]
            nicks_list.append(player_name)
        return nicks_list

    def _icons_paste(self):
        box = [350, 60]  # Aonde os ícones vão começar a ser colados
        collum_count = 0  # Contagem de colunas, para fazer o espaçamento
        size = (96, 96)  # Tamano que os ícones serão dimensionados
        lenght = 100  # Distância horizontal entre um ícone e outro
        for icon_id in self.icons_id_list:  # Passa entre todos os ids dos ícones
            if collum_count == 5:  # Quando a coluna for 5, ou seja, quando passar para o outro time
                box[0] += 62  # Espaço a mais entre um time e outro
            new_box = [box[0] + lenght * collum_count, box[1]]  # Cria a box de colagem levando em conta as colunas
            icon_img = self._get_stat_image(icon_id)  # Transforma o Id em imagem pela função
            icon_img = icon_img.resize(size)  # Redimensiona a imagem
            self.bkg.paste(icon_img, new_box)  # Cola na imagem base
            collum_count += 1

    def _nicks_paste(self):
        collum_count = 0  # Contagem de colunas para fazer o espaçamento
        length = 100  # Distância horizontal entre os nomes
        start_box = [397, 198]  # Aonde os nomes vão começar a ser colados
        draw = ImageDraw.Draw(self.bkg)  # Método para "desenhar" o stat na imagem
        for nick in self.nicks_list:  # Pra cada nick na lista
            if collum_count == 5:  # Quando chegar no sexto player, ou seja, primeiro jogador do time perdedor
                start_box[0] += 62  # Distância entre os times
            box = (start_box[0] + length * collum_count, start_box[1])  # Cria a box para colagem
            if draw.textsize(nick, font=self.font_nicks)[0] > 96:  # Define a fonte dos nicks
                draw.text(box, str(nick), (255, 255, 255), self.font_menor_nicks, anchor="mb")
            else:
                draw.text(box, str(nick), (255, 255, 255), self.font_nicks, anchor="mb")
            # Desenha na imagem
            collum_count += 1

    def _stats_paste(self):
        length = 100  # A distância horizontal entres os stats
        height = 44  # A distância vertical entre os players
        line_count = 0  # contagem de linhas para espaçamento
        collum_count = 0  # contagem de colunas para mudança de player
        count = 11  # Número de stats por player
        draw = ImageDraw.Draw(self.bkg)  # Método para "desenhar" o stat na imagem
        start_box = [398, 254]  # Aonde os stats vão começar a ser colados
        for stat in self.stats_list:  # percorre todos os stats (str)
            if line_count == count:  # Quando chega no último stat do player
                collum_count += 1  # Passa pra póxima coluna
                line_count = 0  # Reseta a contagem de linhas
                if collum_count == 5:  # Quando chegar no primeiro player do próximo time
                    start_box[0] += 62  # Colcoa a distância entre os times
            box = [start_box[0] + length * collum_count, start_box[1] + height * line_count]
            # reference: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
            # Cria o box de colagem
            draw.text(box, str(stat), (0, 0, 0), self.font, anchor="mb")  # Desenha o stat na imagem
            line_count += 1

    def create_image(self):
        self._icons_paste()  # Cola os ícones
        self._nicks_paste()  # Cola os nicks
        self._stats_paste()  # Cola os stats e os nomes
        self.bkg.save("./Images/Createdimages/smite.png")  # Salva em um arquivo novo, substituindo o antigo


"""
PT-BR: Igonorar por enquanto, função sem uso, necessita criar uma nova imagem e mudar todas as dimensões
EN-US: Ignore for now, unused function, needs a new image and dimensions changes
def itens_paste(game, stat_id_list, bkg, champions, itens):
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
"""
