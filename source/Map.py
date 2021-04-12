import pygame
import sys
import os.path
import Utils
from Utils import Colors
from dataclasses import dataclass
from enum import IntEnum

MAP_SIZE_X = 100
MAP_SIZE_Y = 100

MAP_OFFSET_X = 0
MAP_OFFSET_Y = 0

TILE_OFFSET_X = 16
TILE_OFFSET_Y = 8

DEBUG_MINIMAP = False

#Palety https://lospec.com/palette-list/vocodes-62
#       https://lospec.com/palette-list/battery24


#* Global Vars 
gameMap = []
Tiles = {}

Gizmos = []

grass_tile_img = 0
rock_tile_img = 0
sand_tile_img = 0

#* Helpers

# * Tiles
@dataclass
class Tile:
    def __init__(self, id, image, debug_color = Colors['white']):
        self.id = id
        self.image = image
        self.debug_color = debug_color

@dataclass
class Gizmo:
    def __init__(self, shape, color = Colors['white'], border = 0):
        self.shape = shape
        self.color = color
        self.border = border

class Ttype(IntEnum):
    EMPTY = -1
    GRASS = 0
    ROCK = 1
    SAND = 2

def init_tiles():
    global grass_tile_img

    path =  os.path.join(os.path.dirname(__file__), '../Imported/Sprites/Tiles/')

    grass_tile_img = pygame.image.load(path + "grass_tile32x32.png").convert()
    grass_tile_img.set_colorkey((0, 0, 0))

    global rock_tile_img
    rock_tile_img = pygame.image.load(path + "rock_tile32x32.png").convert()
    rock_tile_img.set_colorkey((0, 0, 0))

    global sand_tile_img
    sand_tile_img = pygame.image.load(path + "sand_tile32x32.png").convert()
    sand_tile_img.set_colorkey((0, 0, 0))

    global Tiles
    Tiles = {
        Ttype.EMPTY: Tile(Ttype.EMPTY, 0, Colors["white"]),
        Ttype.GRASS: Tile(Ttype.GRASS, grass_tile_img, Colors["green"]),
        Ttype.ROCK: Tile(Ttype.ROCK, rock_tile_img, Colors["gray"]),
        Ttype.SAND: Tile(Ttype.SAND, sand_tile_img, Colors["yellow"]),
    }

def set_map_offset(x,y):
    global MAP_OFFSET_X
    global MAP_OFFSET_Y
    MAP_OFFSET_X = x
    MAP_OFFSET_Y = y
    
def init_map(surface):

    # * Map data
    with open("Isomap.txt", "r") as f:
        data = f.read()

    data = data.split("\n")
    map_data = []
    for row in data:
        map_data.append(list(row))

    for y in range(MAP_SIZE_Y):
        row = []
        for x in range(MAP_SIZE_X):
            row.append(Tiles[Ttype.EMPTY])
        gameMap.append(row)

    out_of_range_y = False
    for y in range(len(map_data)):
        out_of_range_x = False
        for x in range(len(map_data[y])):
            if x > MAP_SIZE_X - 1 or y > MAP_SIZE_Y - 1:
                if y > MAP_SIZE_Y - 1:
                    out_of_range_x = True
                break

            if map_data[y][x].isdigit() and int(map_data[y][x]) < len(Tiles):
                gameMap[y][x] = Tiles[int(map_data[y][x])]
        if out_of_range_y:
            break

    return surface

def display_map(surface):
    for y, row in enumerate(gameMap):
        for x, tile in enumerate(row):
            pos = Utils.car_to_iso(x,y)
            if tile.id != Ttype.EMPTY:
                if tile.image:
                    surface.blit(tile.image, (MAP_OFFSET_X + pos[0]* TILE_OFFSET_X, MAP_OFFSET_Y + pos[1]* TILE_OFFSET_Y))

def display_debug_map(surface,size):

    for y, row in enumerate(gameMap):
        for x, tile in enumerate(row):
            if tile.id != Ttype.EMPTY:
                    pygame.draw.rect(surface, tile.debug_color , pygame.Rect( 10 + x * size, 10 + y * size, size, size), 1)

def add_square_gizmo(pos_x,pos_y,size_x=10,size_y=10,border=0,color = Colors['white']):
    rect_pos = Utils.car_to_iso(pos_x,pos_y)
    rect_size = (size_x,size_y)
    rect = pygame.Rect(TILE_OFFSET_X - rect_size[0]/2 + MAP_OFFSET_X + rect_pos[0]* TILE_OFFSET_X , MAP_OFFSET_Y + rect_pos[1]* TILE_OFFSET_Y , rect_size[0],rect_size[1])
    gizmo = Gizmo(rect,color,border)
    Gizmos.append(gizmo)

def add_circle_gizmo(pos_x,pos_y,radius = 5,border=0,color = Colors['white']):
    circle_pos = Utils.car_to_iso(pos_x,pos_y)
    circle = Utils.Circle(TILE_OFFSET_X + MAP_OFFSET_X + circle_pos[0] * TILE_OFFSET_X,radius + MAP_OFFSET_Y + circle_pos[1] * TILE_OFFSET_Y , radius)
    gizmo = Gizmo(circle,color,border)
    Gizmos.append(gizmo)
    

