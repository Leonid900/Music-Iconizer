from PIL import Image, ImageFilter, ImageDraw, ImageColor, ImageFont
from pathlib import Path
import sys
import yaml
import re
PATH_BASE_DIR = Path(__file__).resolve().parent
PATH_RESOURCES = PATH_BASE_DIR.joinpath('resources\\')
PATH_DOCS = PATH_BASE_DIR.joinpath('doc\\')
PATH_TILESET = PATH_RESOURCES.joinpath('Tileset.png')
PATH_FONT = PATH_RESOURCES.joinpath('ArialRounded.ttf')

# INIT AND CONSTANTS
img = Image.open(PATH_TILESET)
MARGIN_X = 128

# HARDCODED VALUES
colors = {
    'none':'#ababaa',
    'bg':'#272822', #gray-black bg
    'yellow':'#e6db74', #yellow string
    'orange':'#fd971f', #orange (scope)
    'red':'#f92672', #red (operator)
    'blue':'#66d9ef', #blue (class)
    'green':'#a6e22e', #green (function or method)
    'white':'#f8f8f2', #white (default_text)
    'gray':'#ababaa', #gray (comment)
    'lgray': '#E4E4E4',  # gray (comment)
    'fullwhite': '#ffffff', #full white
    'fullblack': '#000000',  # full black
    'purple': '#e674cd'} # purple
icons = {
    'none': (0, 0),
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
    'ellipsis': (15, 0),
    'header_open': (0, 1),
    'header_fill': (1, 1),
    'header_close': (2, 1),
    'header_single': (3, 1)
    }
block_presets = {
    'separator': {},
    'verse' : {'block_text':'V', 'block_color':'green', 'block_icon':'', 'label':'Verse'},
    'verse1': {'block_text': 'V1', 'block_color': 'green', 'block_icon': '', 'label': 'Verse'},
    'verse2': {'block_text': 'V2', 'block_color': 'green', 'block_icon': '', 'label': 'Verse'},
    'verse3': {'block_text': 'V3', 'block_color': 'green', 'block_icon': '', 'label': 'Verse'},
    'verse4': {'block_text': 'V4', 'block_color': 'green', 'block_icon': '', 'label': 'Verse'},
    'q-verse' : {'block_text':'V', 'block_color':'blue', 'block_icon':'', 'label':'Verse'},
    'q-verse1' : {'block_text':'V1', 'block_color':'blue', 'block_icon':'', 'label':'Verse'},
    'q-verse2' : {'block_text':'V2', 'block_color':'blue', 'block_icon':'', 'label':'Verse'},
    'q-verse3': {'block_text': 'V3', 'block_color': 'blue', 'block_icon': '', 'label': 'Verse'},
    'q-verse4': {'block_text': 'V4', 'block_color': 'blue', 'block_icon': '', 'label': 'Verse'},
    'bridge': {'block_text': 'B', 'block_color': 'orange', 'block_icon': '', 'label': 'Bridge'},
    'bridge1' : {'block_text':'B1', 'block_color':'orange', 'block_icon':'', 'label':'Bridge'},
    'bridge2' : {'block_text':'B2', 'block_color':'orange', 'block_icon':'', 'label':'Bridge'},
    'bridge3' : {'block_text':'B3', 'block_color':'orange', 'block_icon':'', 'label':'Bridge'},
    'bridge4': {'block_text': 'B4', 'block_color': 'orange', 'block_icon': '', 'label': 'Bridge'},
    'rap': {'block_text': 'R', 'block_color': 'orange', 'block_icon': '', 'label': 'Rap'},
    'q-bridge': {'block_text': 'B', 'block_color': 'blue', 'block_icon': '', 'label': 'Bridge'},
    'q-bridge1': {'block_text': 'B1', 'block_color': 'blue', 'block_icon': '', 'label': 'Bridge'},
    'q-bridge2': {'block_text': 'B2', 'block_color': 'blue', 'block_icon': '', 'label': 'Bridge'},
    'q-bridge3' : {'block_text':'B3', 'block_color':'blue', 'block_icon':'', 'label':'Bridge'},
    'q-bridge4': {'block_text': 'B4', 'block_color': 'blue', 'block_icon': '', 'label': 'Bridge'},
    'q-rap': {'block_text': 'R', 'block_color': 'blue', 'block_icon': '', 'label': 'Rap'},
    'chorus': {'block_text': 'C', 'block_color': 'red', 'block_icon': '', 'label': 'Chorus'},
    'solo': {'block_text': 'S', 'block_color': 'purple', 'block_icon': '', 'label': 'Solo'},
    'drum-solo': {'block_text': '', 'block_color': 'purple', 'block_icon': 'drums', 'label': 'Drum Solo'},
    'guitar-solo': {'block_text': '', 'block_color': 'purple', 'block_icon': 'guitar', 'label': 'Guitar Solo'},
    'intro': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop', 'label': 'Intro'},
    'drop': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop', 'label': 'Drop'},
    'hit': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop', 'label': 'Hit'},
    'theme': {'block_text': '', 'block_color': 'purple', 'block_icon': 'note', 'label': 'Theme'},
    'outro': {'block_text': '', 'block_color': 'gray', 'block_icon': 'drop', 'label': 'Outro'},
    'outro-chorus': {'block_text': '', 'block_color': 'red', 'block_icon': 'drop', 'label': 'Outro'},
    'header_open': {'block_text': '', 'block_color': '', 'block_icon': 'header_open', 'icon_color': 'lgray'},
    'header_fill': {'block_text': '', 'block_color': '', 'block_icon': 'header_fill', 'icon_color': 'lgray'},
    'header_close': {'block_text': '', 'block_color': '', 'block_icon': 'header_close', 'icon_color': 'lgray'},
    'header_single': {'block_text': '', 'block_color': '', 'block_icon': 'header_single', 'icon_color': 'lgray'},
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

def generate_colored_sprite(color: str = 'gray', x:int =0, y: int=0) -> Image:
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

def generate_label(text: str, font_size: int = 20) -> Image:
    '''
    Generate label sprite with 128x128
    
    Arguments:
    text        -- Text label
    font_size   -- Font size (default: 32)

    returns     PIL.Image
    '''
    font = ImageFont.truetype(str(PATH_FONT), font_size)
    W, H = 128, 128
    canvas = Image.new('RGBA', (128, 128))
    draw = ImageDraw.Draw(canvas)
    w, h = draw.textsize(text, font=font)
    h_fix = 53
    draw.text(((W-w)/2, ((H-h)/2)-h_fix), text, ImageColor.getrgb(colors['gray']), font=font)
    return canvas

def generate_block(text: str = '', color: str = 'gray', icon: str = 'none', icon_color: str = 'white') -> Image:
    '''
    Generate full block sprite with 128x128
    
    Arguments:
    text        -- Text label       (default: "")
    color       -- Rectangle color  (default: "gray")
    icon        -- Optional icon    (default: None)
    returns     PIL.Image
    '''

    # Mix Font onto Background
    if color:
        square = generate_colored_sprite(color, 2, 0)
    else:
        square = Image.new('RGBA', (128, 128))
    font = generate_text(text)
    mix1 = Image.alpha_composite(square, font)

    # Mix optional Icon onto Background
    if icon:
        icon = generate_colored_sprite(icon_color, icons[icon][0], icons[icon][1])
        mix2 = Image.alpha_composite(mix1, icon)
        return mix2
    else:
        return mix1

def generate_block_from_preset(preset):
    '''
    Generate block from preset
    
    Arguments:
    preset_name     -- Preset name
    returns     PIL.Image
    '''
    
    if preset == 'separator':
        return generate_separator()
    
    text = block_presets[preset]['block_text']
    color = block_presets[preset]['block_color']
    icon = block_presets[preset]['block_icon']
    icon_color = 'white'
    if 'icon_color' in block_presets[preset].keys():
        icon_color = block_presets[preset]['icon_color']
    return generate_block(text, color, icon, icon_color)

def generate_separator():
    '''
    Get empty Image object with 32x128 size
    '''
    return Image.new('RGBA', (32, 128))

class Block():
    def __init__(self, preset=None, settings = None, header=None, label=None):
        
        if preset:
            self.img = generate_block_from_preset(preset)
        else:
            self.img = generate_block(settings[0], settings[1], settings[2],settings[3])
        self.header = header
        self.label = label
        
        if preset:
            if 'label' in block_presets[preset].keys():
                self.label = block_presets[preset]['label']

def generate_full_document(song=[]):
    global MARGIN_X
    
    #Block(settings = (text, block_color, icon, icon_color))
    #Block(preset= '', header = '')
        
    # song = []
    # song.append(Block(settings=('','red','drums','white'), header='header_open'))
    # song.append(Block(preset='theme', header='header_close'))
    # song.append(Block(preset='separator'))
    # song.append(Block(preset='verse', header='header_open'))
    # song.append(Block(preset='verse1', header='header_fill'))
    # song.append(Block(preset='chorus', header='header_fill'))
    # song.append(Block(preset='theme', header='header_close'))
    # song.append(Block(preset='separator'))
    # song.append(Block(preset='verse1', header='header_open'))
    # song.append(Block(preset='verse1', header='header_fill'))
    # song.append(Block(preset='chorus', header='header_fill'))
    # song.append(Block(preset='theme', header='header_close'))
    # song.append(Block(preset='separator'))
    # song.append(Block(preset='bridge1', header='header_single'))
    # song.append(Block(preset='q-verse1', header='header_open'))
    # song.append(Block(preset='q-bridge2', header='header_close'))
    # song.append(Block(preset='separator'))
    # song.append(Block(preset='drop', header='header_single'))
    # song.append(Block(preset='separator'))
    # song.append(Block(preset='chorus', header='header_open'))
    # song.append(Block(preset='chorus', header='header_fill'))
    # song.append(Block(preset='outro', header='header_close'))


    # GET PICTURE WIDTH
    picture_w = 0
    for block in song:
        picture_w += block.img.width
        
    # CREATE EMPTY IMAGE
    song_image = Image.new('RGBA', (picture_w+MARGIN_X*2, MARGIN_X*3), ImageColor.getrgb("#FFFFFF"))

    # FILL EMPTY IMAGE WITH blockS AND block LINES
    next_x = 0
    for block in song:
        buffer_image = Image.new('RGBA', (picture_w+MARGIN_X*2, MARGIN_X*3))
        
        buffer_image.paste(block.img, (MARGIN_X+next_x, MARGIN_X), block.img)
        if block.header:
            header = generate_block_from_preset(block.header)
            buffer_image.paste(header, (MARGIN_X+next_x, 0), header)
        song_image = Image.alpha_composite(song_image, buffer_image)
        next_x += block.img.width


    next_x = 0
    for block in song:
        buffer_image = Image.new('RGBA', (picture_w+MARGIN_X*2, MARGIN_X*3))
        if block.label:
            label = generate_label(block.label)
            buffer_image.paste(label, (MARGIN_X+next_x, 256), label)
        song_image = Image.alpha_composite(song_image, buffer_image)
        next_x += block.img.width

    # RETURN IMAGE OBJECT
    return song_image

def parse_to_images(path):
    # BROKEN YET
    # YARN PARSER
    
    song = []
    with open(path) as f:
        dom = yaml.safe_load(f)


    header = 0
    for i, block in enumerate(dom['song']):

        # if type(block) == str:
        #     song.append(Block(preset=block))
        
        if type(block) == dict:
            header_count = 0
            
                
                
            if 'preset' in block.keys():
                header = ''
                if 'header' in block.keys() and block['header']:
                    if header_count == 0:
                        header = 'header_open'
                    else:
                        header = 'header_fill'
                song.append(Block(preset=block['preset'], header=header))
                
            else:
                # (text, block_color, icon, icon_color)
                song.append(Block(settings=(block['name'], block['color'],block['icon'],block['icon_color'])))
        header_count += 1
    
    return song


def quick_parser(string):
    song = []
    current_header = 'none'
    previous_header = current_header
    string_e = string.split(' ')
    for i, tag in enumerate(string_e):   
        # if tag == '[':
        #     current_header = 'header_open'
        # elif tag == ']':
        #     current_header = 'header_close'
        # if i-1>0:
        #     if previous_header == 'header_open':
        #         current_header = 'header_fill'
        # print(i, tag, previous_header, current_header, sep='\t\t\t')
        if tag != '[' and tag != ']':
            song.append(Block(preset=tag, header='header_fill'))
        if tag == ']':
            song.append(Block(preset='separator', header=''))
        previous_header = current_header
    return song

def generate_song_info(song_name: str, bpm: str, measure: str, key: str, font_size: int = 15) -> Image:
    '''
    Generate song info sprite
    
    Arguments:
    - lazy to do -

    returns     PIL.Image
    '''
    font = ImageFont.truetype(str(PATH_FONT), font_size)
    W, H = 128*6, 128*3
    canvas = Image.new('RGBA', (W, H))
    draw = ImageDraw.Draw(canvas)
    # w, h = draw.textsize(text, font=font)
    h_fix = 6
    draw.text((8,8+25*0), f'Song: {song_name}', (0, 0, 0), font=font)
    draw.text((8,8+25*1), f'BPM: {bpm} {measure}', (0, 0, 0), font=font)
    draw.text((8,8+25*2), f'Key: {key}', (0, 0, 0), font=font)
    return canvas



def do_stuff(song, song_info):
    info = generate_song_info(song_info[0], song_info[1], song_info[2], song_info[3])
    
    song_structure = generate_full_document(quick_parser(song))
    buffer_image = Image.new('RGBA', (song_structure.width, song_structure.height))
    buffer_image.paste(info, (0, 0), info)
    
    finalimage = Image.alpha_composite(song_structure, buffer_image)
    finalimage.show()


# song = '[ hit theme ] [ verse1 verse1 chorus theme ] [ verse2 verse2 chorus theme ] [ bridge1 ] [ q-verse3 q-bridge2 ] [ hit ] [ chorus chorus outro ]'
# song_info = ('Hyperventilation Dance', '140.000', '4/4', 'Em')
# do_stuff(song, song_info)


song = '[ intro ] [ theme ] [ verse1 bridge chorus theme ] [ verse2 bridge chorus theme ] [ drum-solo ] [ guitar-solo ] [ q-rap bridge2 ] [ chorus theme outro ]'
song_info = ('Fuwa Fuwa (Full Size) Yui Hirasawa VERSION', '', '4/4', '')
do_stuff(song, song_info)
