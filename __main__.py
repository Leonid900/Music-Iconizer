from PIL import Image, ImageFilter, ImageDraw, ImageColor, ImageFont
from pathlib import Path
import sys
PATH_BASE_DIR = Path(__file__).resolve().parent
PATH_RESOURCES = PATH_BASE_DIR.joinpath('resources\\')
PATH_TILESET = PATH_RESOURCES.joinpath('Tileset.png')
PATH_FONT = PATH_RESOURCES.joinpath('ArialRounded.ttf')

# MAIN TILESET
img = Image.open(PATH_TILESET)

# HARDCODED VALUES
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
    'purple': '#e674cd'} # purple
icons = {
    'bass-key': (4,0),
    'guitar': (5,0),
    'acoustic-guitar': (6,0),
    'drums': (7, 0),
    'drumsticks': (8, 0),
    'piano': (9, 0),
    'small-star': (10, 0),
    'star': (11, 0),
    'note': (12, 0),
    'rise': (13, 0),
    'drop': (14, 0),
    'ellipsis': (15, 0)}
block_presets = {
    'verse' : {'block_text':'V', 'block_color':'green', 'block_icon':''},
    'verse1' : {'block_text':'V1', 'block_color':'green', 'block_icon':''},
    'verse2' : {'block_text':'V2', 'block_color':'green', 'block_icon':''},
    'verse3' : {'block_text':'V3', 'block_color':'green', 'block_icon':''},
    'verse4': {'block_text': 'V4', 'block_color': 'green', 'block_icon': ''}, 
    'q-verse' : {'block_text':'V', 'block_color':'blue', 'block_icon':''},
    'q-verse1' : {'block_text':'V1', 'block_color':'blue', 'block_icon':''},
    'q-verse2' : {'block_text':'V2', 'block_color':'blue', 'block_icon':''},
    'q-verse3' : {'block_text':'V3', 'block_color':'blue', 'block_icon':''},
    'q-verse4': {'block_text': 'V4', 'block_color': 'blue', 'block_icon': ''},
    'bridge' : {'block_text':'B', 'block_color':'orange', 'block_icon':''},
    'bridge1' : {'block_text':'B1', 'block_color':'orange', 'block_icon':''},
    'bridge2' : {'block_text':'B2', 'block_color':'orange', 'block_icon':''},
    'bridge3' : {'block_text':'B3', 'block_color':'orange', 'block_icon':''},
    'bridge4': {'block_text': 'B4', 'block_color': 'orange', 'block_icon': ''},
    'q-bridge' : {'block_text':'B', 'block_color':'blue', 'block_icon':''},
    'q-bridge1' : {'block_text':'B1', 'block_color':'blue', 'block_icon':''},
    'q-bridge2' : {'block_text':'B2', 'block_color':'blue', 'block_icon':''},
    'q-bridge3' : {'block_text':'B3', 'block_color':'blue', 'block_icon':''},
    'q-bridge4': {'block_text': 'B4', 'block_color': 'blue', 'block_icon': ''},
    'chorus': {'block_text': 'C', 'block_color': 'red', 'block_icon': ''},
    'solo': {'block_text': 'S', 'block_color': 'purple', 'block_icon': ''},
    'drop': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop'},
    'hit': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop'},
    'theme': {'block_text': '', 'block_color': 'purple', 'block_icon': 'note'}}

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

def generate_colored_sprite(color: str, x:int, y:int) -> Image:
    '''
    Generate colored sprite with specific color
    
    Arguments:
    color        -- Input string with color in human readable format.
                    Colors are stored in the "colors" dictionary.
    x            -- Horizontal position of a tile in the tileset
    y            -- Vertical position of a tile in the tileset

    returns     PIL.Image
    '''
    mask = get_tile(img, x, y)
    rgb = ImageColor.getrgb(colors[color])
    fill = Image.new('RGBA', (mask.width, mask.height), rgb)
    return Image.composite(fill, mask, mask)  

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

def generate_block(text: str = '', color: str = 'gray', icon: str = '') -> Image:
    '''
    Generate full block sprite with 128x128
    
    Arguments:
    text        -- Text label       (default: "")
    color       -- Rectangle color  (default: "gray")
    icon        -- Optional icon    (default: None)
    returns     PIL.Image
    '''
    
    # Mix Font onto Background
    square = generate_colored_sprite(color, 2, 0)
    font = generate_text(text)
    mix1 = Image.alpha_composite(square, font)

    # Mix optional Icon onto Background
    if icon:
        icon = generate_colored_sprite('white', icons[icon][0], icons[icon][1])
        mix2 = Image.alpha_composite(mix1, icon)
        return mix2
    else:
        return mix1

def generate_block_from_preset(preset_name):
    '''
    Generate block from preset
    
    Arguments:
    preset_name     -- Preset name
    returns     PIL.Image
    '''
    text = block_presets[preset_name]['block_text']
    color = block_presets[preset_name]['block_color']
    icon = block_presets[preset_name]['block_icon']
    return generate_block(text, color, icon)