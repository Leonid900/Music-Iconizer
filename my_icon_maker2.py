from PIL import Image, ImageFilter, ImageDraw, ImageColor
from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent
TILESET_PATH = Path(r'U:\UQtemp22\SongIcons\SongIcons.png')
img = Image.open(TILESET_PATH)

colors = {
    'bg':'#272822', #gray-black bg
    'yellow':'#e6db74', #yellow string
    'orange':'#fd971f', #orange (scope)
    'red':'#f92672', #red (operator)
    'blue':'#66d9ef', #blue (class)
    'green':'#a6e22e', #green (function or method)
    'white':'#f8f8f2', #white (default_text)
    'gray':'#ababaa', #gray (comment)
    'fullwhite': '#ffffff', #full white
    'fullblack': '#000000',  # full black
}



def get_tile(img, x, y, tile_size=128):
    '''
    Get Image object tile from the tileset
    '''
    return img.crop((tile_size*x, tile_size*y, (tile_size*x)+tile_size, (tile_size*y)+tile_size))


def get_bar_sprite(color):
    '''
    Generate square
    '''
    spr = get_tile(img, 11, 0)
    rgb = ImageColor.getrgb(colors[color])
    fill = Image.new('RGBA', (spr.width, spr.height), rgb)
    colored = Image.composite(fill, spr, spr)  
    colored.show()
    
get_bar_sprite('blue')
