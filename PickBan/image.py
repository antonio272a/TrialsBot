import discord
import io
from PIL import Image, ImageOps

paste_reference = {
  1: (54, 160),
  2: (364, 161),
  3: (674, 161),
  4: (984, 160),
  5: (1293, 161),
  6: (1604, 161),
  7: (54, 478),
  8: (364, 478),
  9: (674, 478),
  10: (984, 478),
  11: (1293, 478),
  12: (1604, 478),
  13: (54, 793),
  14: (364, 793),
}

def draw_on_map(bkg, image, banned_map):
  box = paste_reference[banned_map]
  bkg.paste(image, box, mask=image)

def create_pick_image():
  base = Image.new('RGBA', (252, 252), (0, 0, 0, 0))
  img_with_border = ImageOps.expand(base, border=10, fill=(0, 255, 12))
  return img_with_border

# bkg = Image.open('../Images/mapPickBan/Mapas-PLL.png')
# image = create_pick_image()
# # ban_image = Image.open('../Images/mapPickBan/ban-mapa.png')
# ban_image = Image.new('RGB', (263,263), (0,0,0))
# for box in paste_reference.values():
#   bkg.paste(ban_image, box)

# bkg.save('./image.png')

async def sendPickBanImage(ctx, banned_maps, picked_maps):
  bkg = Image.open("./Images/mapPickBan/Mapas-PLL.png")
  ban_image = Image.open('./Images/mapPickBan/ban-mapa.png')
  
  pick_image = create_pick_image()
  
  for banned_map in banned_maps:
    draw_on_map(bkg, ban_image, banned_map)
  
  for picked_map in picked_maps:
    draw_on_map(bkg, pick_image, picked_map)
  
  with io.BytesIO() as image_binary:
    bkg.save(image_binary, 'PNG')
    image_binary.seek(0)
    await ctx.send(file=discord.File(fp=image_binary, filename='ban.png'))
     
    
