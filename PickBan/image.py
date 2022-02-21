import discord
import io
from PIL import Image, ImageDraw, ImageFont

paste_reference = {
  1: [92, 187],
  2: [92, 337],
  3: [92, 487],
  4: [92, 637],
  5: [92, 787],
  6: [92, 937],
  7: [996, 187],
  8: [996, 337],
  9: [996, 487],
  10: [996, 637],
  11: [996, 787],
  12: [996, 937],
}

def draw_banned_map(draw, font, banned_map):
  box = paste_reference[banned_map]
  paste_box = [box[0] + 78, box[1] + 55]
  draw.text(paste_box, 'X', (0, 0, 0), font, anchor='mm')
  

def draw_picked_map(draw, font, picked_map):
  box = paste_reference[picked_map]
  paste_box = [box[0] + 78, box[1] + 55]
  draw.text(paste_box, 'O', (0, 255, 0), font, anchor='mm')

async def sendPickBanImage(ctx, banned_maps, picked_maps):
  bkg = Image.open("./Images/mapPickBan/Mapas-PLL.png")
  font = ImageFont.truetype("./Docs/Fonts/Arial.ttf", 200)
  draw = ImageDraw.Draw(bkg)
  for banned_map in banned_maps:
    draw_banned_map(draw, font, banned_map)
  for picked_map in picked_maps:
    draw_picked_map(draw, font, picked_map)
  with io.BytesIO() as image_binary:
    bkg.save(image_binary, 'PNG')
    image_binary.seek(0)
    await ctx.send(file=discord.File(fp=image_binary, filename='ban.png'))
     
    
