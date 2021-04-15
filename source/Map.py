import pygame
import sys
import os.path
import Utils
#import random
from Utils import Colors
from dataclasses import dataclass
from enum import IntEnum

MAP_SIZE_X = 100
MAP_SIZE_Y = 100

TILE_OFFSET_X = 16
TILE_OFFSET_Y = 8

TILE_SIZE_X = 32
TILE_SIZE_Y = 32

Z_OFFSET = 13

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

map_offset_x = 0
map_offset_y = 0

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

def Set_map_offset(x,y):
    global map_offset_x, map_offset_y
    map_offset_x = x
    map_offset_y = y

def Map_offset_x(): return map_offset_x
def Map_offset_y(): return map_offset_y

#TODO Do z_levels
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
                    surface.blit(tile.image, (map_offset_x + pos[0]* TILE_OFFSET_X, map_offset_y + (pos[1]* TILE_OFFSET_Y)))
                    

def display_debug_map(surface,size):
    for y, row in enumerate(gameMap):
        for x, tile in enumerate(row):
            if tile.id != Ttype.EMPTY:
                    pygame.draw.rect(surface, tile.debug_color , pygame.Rect( 10 + x * size, 10 + y * size, size, size), 1)

def display_gizmos(surface):
    for gizmo in Gizmos:  
        if isinstance(gizmo.shape, pygame.Rect):
            pygame.draw.rect(surface, gizmo.color, gizmo.shape,gizmo.border)
        elif isinstance(gizmo.shape,Utils.Circle):
            pygame.draw.circle(surface,gizmo.color,(gizmo.shape.pos_x,gizmo.shape.pos_y),gizmo.shape.radius,gizmo.border)

def add_square_gizmo(pos_x,pos_y,size_x=10,size_y=10,border=0,color = Colors['white'], centered = True, offseting = True):
    rect_pos = Utils.car_to_iso(pos_x,pos_y)
    rect_size = (size_x,size_y)
    tile_offset = [0,0]
    #global map_offset_x, map_offset_y

    center_offset = [
        -rect_size[0]/2, # offset x
        -rect_size[1]]   # offset y

    if centered:
        center_offset[0] = -rect_size[0]/2 # offset x
        center_offset[1] = -rect_size[1]/2 # offset y
    if offseting:
        tile_offset[0]  = TILE_OFFSET_X + center_offset[0] # offset x
        tile_offset[1] =  TILE_OFFSET_Y + center_offset[1] # offset y

    rect = pygame.Rect(
         map_offset_x + rect_pos[0]* TILE_OFFSET_X + tile_offset[0],
         map_offset_y + rect_pos[1]* TILE_OFFSET_Y + tile_offset[1], 
        rect_size[0],
        rect_size[1])
    gizmo = Gizmo(rect,color,border)
    Gizmos.append(gizmo) 

def add_circle_gizmo(pos_x,pos_y,radius = 5,border=0,color = Colors['white'], centered = False):
    circle_pos = Utils.car_to_iso(pos_x,pos_y)
    center_offset = 0
    #global map_offset_x, map_offset_y

    if centered:
        center_offset = -radius
    circle = Utils.Circle(
        map_offset_x + TILE_OFFSET_X + (circle_pos[0] * TILE_OFFSET_X),
        map_offset_y + TILE_OFFSET_Y + (circle_pos[1] * TILE_OFFSET_Y) + center_offset,
        radius)
    gizmo = Gizmo(circle,color,border)
    Gizmos.append(gizmo)
    

