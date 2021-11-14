from PIL import Image, ImageFilter, ImageDraw, ImageColor
from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent

TILESET_PATH = Path(r'U:\UQtemp22\SongIcons\SongIcons.png')

img = Image.open(TILESET_PATH)

# VARIABLE STUFF
margin_x = 128

# HARDCODED PRESETS THAT YALANY DOESN NOT LIKE :3
presets = {
    'verse':        {'base_x': 7,    'base_y': 5,   'icon_x': 8,     'icon_y': 6},
    'verse1':       {'base_x': 7,    'base_y': 5,   'icon_x': 8,     'icon_y': 7},
    'verse2':       {'base_x': 7,    'base_y': 5,   'icon_x': 9,     'icon_y': 7},
    'verse3':       {'base_x': 7,    'base_y': 5,   'icon_x': 10,    'icon_y': 7},
    'verse4':       {'base_x': 7,    'base_y': 5,   'icon_x': 11,    'icon_y': 7},
    'bridge':       {'base_x': 7,    'base_y': 4,   'icon_x': 9,     'icon_y': 6},
    'bridge1':      {'base_x': 7,    'base_y': 4,   'icon_x': 15,    'icon_y': 5},
    'bridge2':      {'base_x': 7,    'base_y': 4,   'icon_x': 15,    'icon_y': 6},
    'bridge3':      {'base_x': 7,    'base_y': 4,   'icon_x': 15,    'icon_y': 7},
    'q-verse':      {'base_x': 7,    'base_y': 1,   'icon_x': 8,     'icon_y': 6},
    'q-verse1':     {'base_x': 7,    'base_y': 1,   'icon_x': 8,     'icon_y': 7},
    'q-verse2':     {'base_x': 7,    'base_y': 1,   'icon_x': 9,     'icon_y': 7},
    'q-verse3':     {'base_x': 7,    'base_y': 1,   'icon_x': 10,    'icon_y': 7},
    'q-verse4':     {'base_x': 7,    'base_y': 1,   'icon_x': 11,    'icon_y': 7},
    'q-bridge':     {'base_x': 7,    'base_y': 1,   'icon_x': 9,     'icon_y': 6},
    'q-bridge1':    {'base_x': 7,    'base_y': 1,   'icon_x': 15,    'icon_y': 5},
    'q-bridge2':    {'base_x': 7,    'base_y': 1,   'icon_x': 15,    'icon_y': 6},
    'q-bridge3':    {'base_x': 7,    'base_y': 1,   'icon_x': 15,    'icon_y': 7},
    'chorus':       {'base_x': 7,    'base_y': 3,   'icon_x': 10,   'icon_y': 6 },
    'solo':         {'base_x': 7,    'base_y': 2,   'icon_x': 11,   'icon_y': 6 },
    'theme':        {'base_x': 7,    'base_y': 2,   'icon_x': 13,   'icon_y': 6 },
    'hit':          {'base_x': 7,    'base_y': 0,   'icon_x': 14,   'icon_y': 7 },
    'bar_open':     {'base_x': 0,    'base_y': 0,   'icon_x': 0,    'icon_y': 1 },
    'bar_fill':     {'base_x': 0,    'base_y': 0,   'icon_x': 1,    'icon_y': 1 },
    'bar_close':    {'base_x': 0,    'base_y': 0,   'icon_x': 2,    'icon_y': 1 },
    'bar_single':   {'base_x': 0,    'base_y': 0,   'icon_x': 3,    'icon_y': 1 },
    
    'label_intro':   {'base_x': 0,    'base_y': 0,   'icon_x': 12,    'icon_y': 8},
}


def get_tile(img, x,y, tile_size=128):
    '''
    Get Image object with 128x128 tile from the tileset
    '''
    return img.crop((tile_size*x, tile_size*y, (tile_size*x)+128, (tile_size*y)+128))



def get_bar(preset):
    '''
    Get combined BASE with ICON as Image object
    '''    

    base_x = presets[preset]['base_x']
    base_y = presets[preset]['base_y']
    icon_x = presets[preset]['icon_x']
    icon_y = presets[preset]['icon_y']

    base = get_tile(img, base_x, base_y)
    icon = get_tile(img, icon_x, icon_y)
    return Image.alpha_composite(base, icon)


def get_separator():
    '''
    Get empty Image object with 32x128 size
    '''
    return Image.new('RGBA', (32,128))


def create_song_image():
    '''
    Create full song with all bars, return Image
    '''
    global margin_x
    # CREATE ARRAY OF BARS
    song = []
    song.append({'pic': get_bar(preset='hit'), 'header': 'bar_single'})
    song.append( {'pic' : get_bar(preset='q-bridge1'),  'header': 'bar_open'} )
    song.append( {'pic' : get_bar(preset='bridge2'), 'header': 'bar_fill'} )
    song.append( {'pic' : get_bar(preset='bridge3'), 'header': 'bar_close'} )
    song.append( {'pic' : get_separator()} )
    song.append( {'pic' : get_bar(preset='q-verse'), 'header': 'bar_single'} )   
    song.append( {'pic' : get_separator()} )
    song.append( {'pic': get_bar(preset='verse2'),  'header': 'bar_open'})
    song.append( {'pic': get_bar(preset='bridge'), 'header': 'bar_fill'})
    song.append( {'pic': get_bar(preset='solo'), 'header': 'bar_fill'})
    song.append( {'pic': get_bar(preset='chorus'), 'header': 'bar_close'})

    # GET PICTURE WIDTH
    picture_w = 0
    for bar in song:
        picture_w += bar['pic'].width
    
    # CREATE EMPTY IMAGE
    song_image = Image.new('RGBA', (picture_w+margin_x*2, margin_x*3), ImageColor.getrgb("#FFFFFF"))
    
    # FILL EMPTY IMAGE WITH BARS AND BAR LINES
    next_x = 0
    for bar in song:
        buffer_image = Image.new('RGBA', (picture_w+margin_x*2, margin_x*3))
        buffer_image.paste(bar['pic'], (margin_x+next_x, margin_x), bar['pic'])
        if 'header' in bar.keys():
            header = get_bar(preset=bar['header'])
            buffer_image.paste(header, (margin_x+next_x, 0), header)
        
        song_image = Image.alpha_composite(song_image, buffer_image)
        next_x += bar['pic'].width

    # RETURN IMAGE OBJECT
    return song_image
    
    

img = create_song_image()
img.show()

