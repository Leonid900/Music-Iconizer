from PIL import Image, ImageFilter, ImageDraw, ImageColor
from pathlib import Path
import sys
PATH_BASE_DIR = Path(__file__).resolve().parent
PATH_RESOURCES = PATH_BASE_DIR.joinpath('resources\\')
PATH_TILESET = PATH_RESOURCES.joinpath('Tileset.png')
PATH_FONT = PATH_RESOURCES.joinpath('ArialRounded.ttf')

img = Image.open(PATH_TILESET)

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
    returns PIL.Image
    '''
    return img.crop((tile_size*x, tile_size*y, (tile_size*x)+tile_size, (tile_size*y)+tile_size))


def get_bar_sprite(color):
    '''
    Generate square with specific color
    returns PIL.Image    
    '''
    spr = get_tile(img, 2, 0)
    rgb = ImageColor.getrgb(colors[color])
    fill = Image.new('RGBA', (spr.width, spr.height), rgb)
    return Image.composite(fill, spr, spr)  
        
get_bar_sprite('red').show()
