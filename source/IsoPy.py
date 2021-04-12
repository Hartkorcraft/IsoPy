import pygame
import sys
import Utils
from Utils import Colors
from Map import *

#* Global settings 
FPS = 60
REZ_X = 500
REZ_Y = 500
RENDER_REZ_X = 1000
RENDER_REZ_Y = 1000

BACKGROUND_COLOR = (50,50,50)

DEBUG_MINIMAP = True
DEBUG_MINIMAP_SIZE = 8

def main():

    #* Pygame init stuff
    pygame.init()
    pygame.display.set_caption("XD")
    screen = pygame.display.set_mode((RENDER_REZ_X, RENDER_REZ_Y), 0, 32)
    surface = pygame.Surface((REZ_X, REZ_Y))
    clock = pygame.time.Clock()

    #* Other init stuff
    surface.fill(BACKGROUND_COLOR)

    #* Map Stuff
    init_tiles()
    init_map(surface)
    set_map_offset(REZ_X/2,REZ_Y/4)

    #* Gizmos
    add_square_gizmo(0,1,10,10,1)

    add_circle_gizmo(0,0,5,1)

    #* Main loop
    while 1:

        #* Displaying
        display_map(surface)
        if DEBUG_MINIMAP: display_debug_map(surface, DEBUG_MINIMAP_SIZE)
        
        for gizmo in Gizmos:  
            if isinstance(gizmo.shape, pygame.Rect):
                pygame.draw.rect(surface, gizmo.color, gizmo.shape,gizmo.border)
            elif isinstance(gizmo.shape,Utils.Circle):
                pygame.draw.circle(surface,gizmo.color,(gizmo.shape.pos_x,gizmo.shape.pos_y),gizmo.shape.radius,gizmo.border)

        #* Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #* Rendering
        screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))
        screen = pygame.display.get_surface()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
