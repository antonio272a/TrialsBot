import discord
from discord.ext import commands
from PickBan.image import sendPickBanImage


class MapPickBan(commands.Cog):
  
  def __init__(self, client):
    self.client = client
    self.fst_cap_aliases = ['capitao 1', 'capitão 1', 'capitão1', 'capitao1', 'capitan 1', 'capitan1']
    self.scd_cap_aliases = ['capitao 2', 'capitão 2', 'capitão2', 'capitao2', 'capitan 2', 'capitan 2']
    self.maps_reference = [ 
      'Frog Isle', 'Jaguar Falls', 'Serpent Beach', 'Frozen Guard', 'Fish Market', 'Timber Mill', 'Stone Keep',
      'Bright Marsh', 'Splitstone Quarry', 'Ascension Peak', 'Warder\'s Gate', 'Shattered Desert', 'Bazaar', 'Ice Mines'
    ]
    self.in_progress_channels = []
    self.stop_command = 'stop'
    
  
  @commands.group(name='pickban', invoke_without_command=True)
  async def scrim_cmd(self, ctx):
    await ctx.send('Para iniciar, use ".pickban start"')

  def check_captain(self, capitain_aliases):
    def inner_check(message):
      response = message.content.lower()
      if self.stop_command in response: return True
      
      for alias in capitain_aliases:
        if response.startswith(alias):
         return True
      return False
    return inner_check
  
  def check_ban(self, valid_bans, capitan):
    def inner_check(message):
      response = message.content.lower()
      if self.stop_command in response: return True
      for valid_ban in valid_bans:
        if (response[:6] == f'ban {valid_ban}') and message.author.id == capitan:
          return True
      return False
    return inner_check

  def check_pick(self, valid_picks, capitain):
    def inner_check(message):
      response = message.content.lower()
      for valid_pick in valid_picks:
        if (response[:7] == f'pick {valid_pick}') and message.author.id == capitain:
          return True
      return False
    return inner_check

  async def get_ban(self, ctx, ban_number, capitain_id, check):
    ban_text = {
      1: { 'br': 'Primeiro', 'esp':'Primer'}, 
      2: { 'br': 'Segundo', 'esp': 'Segundo'},
    }
    
    ban_message = f'''
🔸**IDIOMA ESPAÑOL:**
{ban_text[ban_number]['esp']} **Ban** del capitan <@{capitain_id}>
Para banear, escribe "Ban <número>" usando la imagen como base para los números.
📌Ejemplo: Ban 1
      
🔹**IDIOMA PORTUGUÊS (BRASIL):**
{ban_text[ban_number]['br']} **Ban** do capitão <@{capitain_id}>
Para banir, escreva "Ban <número>" usando a imagem como base para os números.
📌Exemplo: Ban 1
'''
    
    await ctx.send(ban_message)
    ban_msg = await self.client.wait_for('message', check=check)
    if self.stop_command in ban_msg.content:
      return self.stop_command
    ban = int(ban_msg.content.split(sep=" ")[1])
    banned_map_msg = f'''
🔸**IDIOMA ESPAÑOL:**
El {ban_text[ban_number]['esp']} ban del capitan <@{capitain_id}> fue: **{self.maps_reference[ban - 1]}**

🔹**IDIOMA PORTUGUÊS (BRASIL):**
O {ban_text[ban_number]['br']} ban do capitão <@{capitain_id}> foi: **{self.maps_reference[ban - 1]}**
    '''
    await ctx.send(banned_map_msg)
    return ban

  def update_valid_maps(self, ban, valid_bans, banned_maps):
    valid_bans.remove(ban)
    banned_maps.append(ban)

  async def get_pick(self, ctx, capitain_id, check):
    pick_message = f'''
🔸**IDIOMA ESPAÑOL:**
Pick de mapa del capitán <@{capitain_id}>
Para pickear, escribe "pick <número>" usando la imagen como base para los números.
📌Ejemplo: Pick 1

🔹**IDIOMA PORTUGUÊS (BRASIL):**
Pick de mapa do capitão <@{capitain_id}>
Para pickar, escreva "pick <número> usando a imagem como base para os números"
📌Exemplo: Pick 1
    '''
    
    await ctx.send(pick_message)    
    pick_msg = await self.client.wait_for('message', check=check)
    pick = int(pick_msg.content.split(sep=' ')[1])
    
    picked_map_msg = f'''
🔸**IDIOMA ESPAÑOL:**
El mapa seleccionado por el capitan <@{capitain_id}> fue: **{self.maps_reference[pick - 1]}**
    
🔹**IDIOMA PORTUGUÊS (BRASIL):**
O mapa selecionado pelo capitão <@{capitain_id}> foi: **{self.maps_reference[pick - 1]}**
    '''
    await ctx.send(picked_map_msg)
    return pick

  async def get_capitain(self, ctx, team_number):
    team_name = {
      1: {'br': 'primeiro', 'esp': 'primer'},
      2: {'br': 'segundo', 'esp': 'segundo'},
    }
    aliases = self.fst_cap_aliases if team_number == 1 else self.scd_cap_aliases
    
    capitain_message = f'''
🔸**IDIOMA ESPAÑOL:**
Para seleccionar el {team_name[team_number]['esp']} capitan, escribe **"capitan {team_number}"**

🔹**IDIOMA PORTUGUÊS (BRASIL):**
Para selecionar o {team_name[team_number]['br']} capitão, escreva **"capitão {team_number}"**
    '''
    
    await ctx.send(capitain_message)
    cap_msg = await self.client.wait_for('message', check=self.check_captain(aliases))
    
    if self.stop_command in cap_msg.content:
      return self.stop_command
    
    cap = cap_msg.author.id
    selected_cap_msg = f'''
🔸**IDIOMA ESPAÑOL:**
{team_name[team_number]['esp'].title()} Capitan: <@{cap}>

🔹**IDIOMA PORTUGUÊS (BRASIL):**
{team_name[team_number]['br'].title()} Capitão: <@{cap}>
    '''
    await ctx.send(selected_cap_msg)
    return cap

  async def break_command(self, ctx):
    break_command_msg = f'''
🔸**IDIOMA ESPAÑOL:**
Comando Pick/Ban cancelado, escriba ".pickban start" para comenzar de nuevo

🔹**IDIOMA PORTUGUÊS (BRASIL):**
Comando de Pick/Ban cancelado, digite ".pickban start" para iniciar novamente
    '''
    await ctx.send(break_command_msg)

  @scrim_cmd.command(name='start')
  async def start_ban(self, ctx):

      channel_id = ctx.channel.id
      if (channel_id in self.in_progress_channels):
        return

      self.in_progress_channels.append(channel_id)

      ################################################## Get Captains

      fst_cap = await self.get_capitain(ctx, 1)
      if fst_cap == self.stop_command: return await self.break_command(ctx)
      
      scd_cap = await self.get_capitain(ctx, 2)
      if scd_cap == self.stop_command: return await self.break_command(ctx)

      ################################################### Set bans

      valid_bans = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
      banned_maps = []
      picked_maps = []

      #################################################### Get Bans  

      await sendPickBanImage(ctx, banned_maps, picked_maps)

      for index in range(1,5):
        capitain = fst_cap if index % 2 else scd_cap
        ban_number = 1 if index <= 2 else 2
        ban = await self.get_ban(ctx, ban_number, capitain, self.check_ban(valid_bans, capitain))
        if ban == self.stop_command: return await self.break_command(ctx)
        self.update_valid_maps(ban, valid_bans, banned_maps)
        await sendPickBanImage(ctx, banned_maps, picked_maps)
      
      ############################################################ Get Pick

      pick = await self.get_pick(ctx, fst_cap, self.check_pick(valid_bans, fst_cap))

      picked_maps.append(pick)

      with open(f'./Images/mapPickBan/mapPicks/map-pick-{pick}.png', 'rb') as img:
        await ctx.send(file=discord.File(img, 'pick.png'))
      
      ################################################################### Remove from in_progress list
      
      self.in_progress_channels.remove(channel_id)
      
def setup(client):
    client.add_cog(MapPickBan(client))
