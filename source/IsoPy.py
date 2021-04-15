import pygame




import sys
import Utils
import math
#import time
from Utils import Colors
from Map import *

#* Global settings 
FPS = 60
REZ_X = 500
REZ_Y = 500
RENDER_REZ_X = 1000
RENDER_REZ_Y = 1000

BACKGROUND_COLOR = (50,50,50)

DEBUG = True
DEBUG_MINIMAP = False
DEBUG_MINIMAP_SIZE = 8

pygame.init()

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
    #Set_map_offset(REZ_X/2,REZ_Y/4)

    #* Gizmos

    #add_square_gizmo(5,0,10,10,1,Colors['white'])
    #add_circle_gizmo(0,0,5,1,Colors['red'])

    for y, row in enumerate(gameMap):
        for x, tile in enumerate(row):
            add_square_gizmo(x,y,8,8,1)

    #* Other 

    #* Main loop
    while 1:
        
        #* Update stuff
        mouse_pos = pygame.mouse.get_pos()

        #* Displaying
        display_map(surface)
        
        if DEBUG:
            if DEBUG_MINIMAP: display_debug_map(surface, DEBUG_MINIMAP_SIZE)
            display_gizmos(surface)

        #* Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #* Other 

        mouse_grid_pos = Utils.car_to_iso(mouse_pos[0], mouse_pos[1])  

        print(
            mouse_grid_pos[0] / TILE_OFFSET_X,
            mouse_grid_pos[1] / TILE_OFFSET_Y
            )

        #* Rendering
        screen.blit(pygame.transform.scale(surface, screen.get_size()), (0, 0))
        screen = pygame.display.get_surface()
        pygame.display.update()
        clock.tick(FPS)

        #time.sleep(1)


main()

# if __name__ == "__main__":
    # main()


#                 Y.                      _   
#                 YiL                   .```.  
#                 Yii;                .; .;;`.    
#                 YY;ii._           .;`.;;;; :    
#                 iiYYYYYYiiiii;;;;i` ;;::;;;;    
#             _.;YYYYYYiiiiiiYYYii  .;;.   ;;; 
#          .YYYYYYYYYYiiYYYYYYYYYYYYii;`  ;;;;    
#        .YYYYYYY$$YYiiYY$$$$iiiYYYYYY;.ii;`..   
#       :YYY$!.  TYiiYY$$$$$YYYYYYYiiYYYYiYYii.    
#       Y$MM$:   :YYYYYY$!"``"4YYYYYiiiYYYYiiYY.    
#    `. :MM$$b.,dYY$$Yii" :'   :YYYYllYiiYYYiYY    
# _.._ :`4MM$!YYYYYYYYYii,.__.diii$$YYYYYYYYYYY
# .,._ $b`P`     "4$$$$$iiiiiiii$$$$YY$$$$$$YiY;
#    `,.`$:       :$$$$$$$$$YYYYY$$$$$$$$$YYiiYYL
#     "`;$$.    .;PPb$`.,.``T$$YY$$$$YYYYYYiiiYYU:  
#     ;$P$;;: ;;;;i$y$"!Y$$$b;$$$Y$YY$$YYYiiiYYiYY 
#     $Fi$$ .. ``:iii.`-":YYYYY$$YY$$$$$YYYiiYiYYY    
#     :Y$$rb ````  `_..;;i;YYY$YY$$$$$$$YYYYYYYiYY:    
#      :$$$$$i;;iiiiidYYYYYYYYYY$$$$$$YYYYYYYiiYYYY. 
#       `$$$$$$$YYYYYYYYYYYYY$$$$$$YYYYYYYYiiiYYYYYY    
#       .i!$$$$$$YYYYYYYYY$$$$$$YYY$$YYiiiiiiYYYYYYY    
#      :YYiii$$$$$$$YYYYYYY$$$$YY$$$$YYiiiiiYYYYYYi'    
