import sys
import functools
import operator
import numpy
import pygame, math, time, random
import matplotlib.pyplot as plt # Nota: Si no funciona, use pip install matplotlib
import cv2 # Nota: Si no funciona, use pip install opencv-python
#np.set_printoptions(threshold=sys.maxsize) # Esto es una prueba para visualizar los valores del numpy array

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def imagen_a_cromosoma(img_arr):
    cromosoma = numpy.reshape(a=img_arr, newshape=(functools.reduce(operator.mul, img_arr.shape)))
    return cromosoma

def cromosoma_a_imagen(cromosoma, forma_imagen):
    array_imagen = numpy.reshape(a=cromosoma, newshape=forma_imagen)
    return array_imagen

def poblacion_inicial(forma_silueta, num_poblacion_inicial=8): # Aqui se deberia dibujar arboles random como poblacion inicial
    pob_inicial = numpy.empty(shape=(num_poblacion_inicial,
                                         functools.reduce(operator.mul, forma_silueta)),
                                  dtype=numpy.uint8)
    for indv_num in range(num_poblacion_inicial):
        # Genera aleatoriamente los valores geneticos de los cromosomas de la poblacion inicial

        drawTree(300, 550, -90, 8)
        pygame.image.save(window, "current_tree.jpeg")  # Se guarda el arbol dibujado como una imagen
        current_tree = cv2.imread(
            "current_tree.jpeg")  # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original
        print(generated_tree)
        print(len(generated_tree))

        current_cromosoma= imagen_a_cromosoma(current_tree)
        print(current_cromosoma)
        print(len(current_cromosoma))

        pob_inicial[indv_num, :] = current_cromosoma
    print(len(pob_inicial))
    print(pob_inicial)
    return pob_inicial

def drawTree(x1, y1, angle, depth):
    # time.sleep(.001)
    pygame.display.flip()
    fork_angle = 20 - (random.random())
    base_len = 10.0 - (random.random())
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        y2 = y1 + int(math.sin(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
        drawTree(x2, y2, angle - fork_angle, depth - 1)
        drawTree(x2, y2, angle + fork_angle, depth - 1)

#------------------------------------Se lee y convierte la imagen de la silueta a un numpy array-------------------------------------------------------------------
imageFileName = input("Escriba el nombre de la imagen: ")
my_img = cv2.imread(imageFileName) # Se lee la imagen
inverted_img = (255.0 - my_img) # Se invierte para que el arbol quede en blanco
final = inverted_img / 255.0
print(final) # Prueba para visualizar los valores (en un numpy array) de la imagen invertida
print(len(final))

plt.imshow(final)
plt.show() # Prueba para ver la imagen invertida
print(final.shape)

silueta_cromosoma = imagen_a_cromosoma(final) # Se convierte la imagen de la silueta a una cromosoma del algoritmo genetico
print(silueta_cromosoma)
print(len(silueta_cromosoma))
#------------------------------------Se lee y convierte la imagen de la silueta a un numpy array------------------------------------------------------------------

#------------------------------------Se dibuja el arbol y se guarda la imagen del arbol dibujado como un numpy array----------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

drawTree(300, 550, -90, 8)
pygame.image.save(window, "generated_tree.jpeg") # Se guarda el arbol dibujado como una imagen
generated_tree = cv2.imread("generated_tree.jpeg") # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original
print(generated_tree)
print(len(generated_tree))

generado_cromosoma = imagen_a_cromosoma(generated_tree)
print(generado_cromosoma)
print(len(generado_cromosoma))

def input(event):
    if event.type == pygame.QUIT:
        exit(0)

    if event.type == KEYDOWN:

        # si apretamos abajo se hace otro arbol
        if event.key == K_DOWN:
            screen.fill((0, 0, 0))
            # drawTree(300, 550, -90, 8)
            drawTree(300, 550, -90, 8)

while True:
    input(pygame.event.wait())
    pygame.display.flip()
#------------------------------------Se dibuja el arbol y se guarda la imagen del arbol dibujado como un numpy array----------------------------------------------