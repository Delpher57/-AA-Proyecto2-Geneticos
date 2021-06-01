import pygame,math,random,time
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

colors = [pygame.Color("#eb345b"),pygame.Color("#ebdb2a"),pygame.Color("#26ebe1"),pygame.Color("#6b1fcf")]
def get_color():
    global colors
    color = colors[0]
    colors.pop(0)
    colors += [color]
    return color

def drawTree(x1, y1, angle, depth, angulo_ramas, tamanno,cantidad_ramas=4,grueso=2):
    
    
    #fork_angle = angulo_ramas + random.random() * 5
    base_len = tamanno
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle))*depth*base_len)
        y2 = y1 + int(math.sin(math.radians(angle))*depth*base_len)


        pygame.draw.line(screen, get_color(), (x1, y1), (x2, y2), grueso)

        angle_diference = (-180)/cantidad_ramas

        initial_angle = (angulo_ramas + cantidad_ramas*10) - (180)/cantidad_ramas

        for i in range(0,cantidad_ramas):
            drawTree(x2, y2, initial_angle, depth - 1, initial_angle, tamanno,cantidad_ramas)
            initial_angle -= angle_diference
        
        #drawTree(x2, y2, angle - fork_angle, depth - 1, angulo_ramas, tamanno)
        #drawTree(x2, y2, angle + fork_angle, depth - 1, angulo_ramas, tamanno)

test = 3
def input(event):
    global test

    if event.type == pygame.QUIT:
        exit(0)

    if event.type == KEYDOWN:

        # si apretamos abajo se hace otro arbol
        if event.key == K_DOWN:
            test+=1
    
 








while True:
    input(pygame.event.wait())
    screen.fill((0,0,0))
    
    drawTree(300, 550, -90, 3 ,180 ,30,test,8)
    pygame.display.flip()


