from arcade import Sprite

CONTENT_PATH = 'Content'
CONTENT_SPRITES_PATH = CONTENT_PATH + '/Sprites/'

def LoadSprite(file_name, file_path = CONTENT_SPRITES_PATH):
    return Sprite(file_path + file_name)