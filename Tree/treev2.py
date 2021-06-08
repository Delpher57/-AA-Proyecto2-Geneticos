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

def get_random(range=1):
    return random.uniform(-range, range) * random.choice([-1,1])

def reduce_num(num):
    if num == 1:
        return num
    else:
        return num - 0.75


def drawTree(x1, y1, angle, depth, angulo_inicio, tamanno,cantidad_ramas=4,grueso=2, random=0,random2=0):
    
    
    base_len = tamanno
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle))*depth*base_len)
        y2 = y1 + int(math.sin(math.radians(angle))*depth*base_len)


        pygame.draw.line(screen, get_color(), (x1, y1), (x2, y2), grueso)

        angle_diference = (-180)/cantidad_ramas + get_random(random) 

        initial_angle = (angulo_inicio) - (180)/(cantidad_ramas)  + get_random(random)
        if cantidad_ramas==2:
            initial_angle+=45

        for i in range(0,cantidad_ramas):
            drawTree(x2, y2, initial_angle, depth - 1, initial_angle, tamanno + get_random(random2),cantidad_ramas,random=random,random2= reduce_num(random2))
            initial_angle -= angle_diference - get_random(random)

def input(event):


    if event.type == pygame.QUIT:
        exit(0)



    

def tree(x1,y1,profundidad,tamanno,cantidad_ramas, ancho_tronco,random1, random2):
    """[generamos un arbo dados loa parametros, 
        lo que hacemos es llamar la funcion y aqui preparamos los parametros]

    Args:
        x1 ([int]): [posicion en x del tronco]
        y1 ([int]): [posicion en y del tronco]
        profundidad ([int]): [cantidad de subdiviciones]
        tamanno ([int]): [tamaño del arbol (largo de las ramas)]
        cantidad_ramas ([int]): [cantidad de amas]
        ancho_tronco ([int]): [hancho del tronco del arbol]
        random1 ([int]): [random en los angulos de las hojas]
        random2 ([int]): [random en el largo de las hojas]
    """    
    angulo_inicio =180+(180/(cantidad_ramas-1))
    if cantidad_ramas==2:
        angulo_inicio-=90

    angulo_tronco = -90
    drawTree(x1,y1, angulo_tronco, profundidad ,angulo_inicio ,tamanno,cantidad_ramas,ancho_tronco,random1,random2)


while True:
    input(pygame.event.wait())
    screen.fill((0,0,0))
    tree(x1=300,y1=550,profundidad=6,tamanno=10,cantidad_ramas=3,ancho_tronco=8,random1=5,random2=5)
   
    pygame.display.flip()


