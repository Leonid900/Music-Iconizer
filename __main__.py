from PIL import Image, ImageFilter, ImageDraw, ImageColor, ImageFont
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

def get_tile(img: Image, x: int, y: int, tile_size: int = 128) -> Image:
    '''
    Get Image object tile from the tileset 
    
    Arguments:
    img         -- Input image of a tileset (PIL.Image)
    x           -- horizontal tile position in tileset
    y           -- vertical tile position in tileset
    tile-size   -- size of a single tile (default 128)
    
    returns     PIL.Image
    '''
    return img.crop((tile_size*x, tile_size*y, (tile_size*x)+tile_size, (tile_size*y)+tile_size))
def generate_bar_square(color: str) -> Image:
    '''
    Generate square with specific color
    
    Arguments:
    color        -- Input string with color in human readable format.
                    Colors are stored in the "colors" dictionary.

    returns     PIL.Image
    '''
    spr = get_tile(img, 2, 0)
    rgb = ImageColor.getrgb(colors[color])
    fill = Image.new('RGBA', (spr.width, spr.height), rgb)
    return Image.composite(fill, spr, spr)  
def generate_text(text: str, font_size: int = 53) -> Image:
    '''
    Generate text sprite with 128x128
    
    Arguments:
    text        -- Text label
    font_size   -- Font size (default: 53)

    returns     PIL.Image
    '''
    font = ImageFont.truetype(str(PATH_FONT), font_size)
    W, H = 128, 128
    canvas = Image.new('RGBA', (128, 128))
    draw = ImageDraw.Draw(canvas)
    w, h = draw.textsize(text, font=font)
    h_fix= 6
    draw.text(((W-w)/2, ((H-h)/2)-h_fix), text, (255, 255, 255), font=font)
    return canvas
def generate_bar(text: str = '', color: str = 'gray', icon: str = None) -> Image:
    '''
    Generate text sprite with 128x128
    
    Arguments:
    text        -- Text label       (default: "")
    color       -- Rectangle color  (default: "gray")
    icon        -- Optional icon    (default: None)
    returns     PIL.Image
    '''
    
    square = generate_bar_square(color)
    font = generate_text(text)
    mix1 = Image.alpha_composite(square, font)
    return mix1


generate_bar('V','red','').show()
