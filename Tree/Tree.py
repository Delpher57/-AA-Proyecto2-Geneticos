import pygame, math, time, random


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

 
def drawTree(x1, y1, angle, depth):
    #time.sleep(.001)
    pygame.display.flip()
    fork_angle = 20 - (random.random())
    base_len = 10.0 - (random.random())
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle + random.random())) * depth * base_len * (random.random()+0.5))
        y2 = y1 + int(math.sin(math.radians(angle + random.random())) * depth * base_len * (random.random()+0.5))
        pygame.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), 2)
        drawTree(x2, y2, angle - fork_angle, depth - 1)
        drawTree(x2, y2, angle + fork_angle, depth - 1)


def input(event):

    if event.type == pygame.QUIT:
        exit(0)
    
    if event.type == KEYDOWN:
        
        #si apretamos abajo se hace otro arbol
        if event.key == K_DOWN:
            screen.fill((0,0,0))
            #drawTree(300, 550, -90, 8)
            drawTree(300, 550, -90, 8)




drawTree(300, 550, -90, 8)

while True:
    input(pygame.event.wait())
    pygame.display.flip()
