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
    i = 0
    for indv_num in range(num_poblacion_inicial):
        # Genera aleatoriamente los valores geneticos de los cromosomas de la poblacion inicial

        drawTree(300, 550, -90, 8)
        filename = "current_tree%s" %i
        pygame.image.save(window, filename + ".jpeg")  # Se guarda el arbol dibujado como una imagen
        color = (0, 0, 0)
        screen.fill(color)
        current_tree = cv2.imread(
            filename + ".jpeg")  # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original

        current_cromosoma= imagen_a_cromosoma(current_tree)

        pob_inicial[indv_num, :] = current_cromosoma
        i = i + 1

    pygame.display.flip()
    return pob_inicial

def funcion_adaptabilidad(cromosoma_silueta, cromosoma_arbol_generado):
    diferencia = cromosoma_silueta - cromosoma_arbol_generado
    print(diferencia)
    similitud = numpy.mean(numpy.abs(diferencia))
    similitud = numpy.sum(cromosoma_silueta) - similitud
    print(similitud)
    return similitud

def calcular_todas_similitudes(cromosoma_silueta, poblacion):
    print(poblacion.shape)
    array_similitudes = numpy.zeros(poblacion.shape[0])

    for individuo in range(poblacion.shape[0]):
        array_similitudes[individuo] = funcion_adaptabilidad(cromosoma_silueta, poblacion[individuo, :])

    return array_similitudes

def seleccion(poblacion, similitudes, numero_padres):
    padres = numpy.empty((numero_padres,poblacion.shape[1]),dtype=numpy.uint8)

    for padre in range(numero_padres):
        similitud_maxima = numpy.where(similitudes == numpy.nax(similitudes))
        similitud_maxima = similitud_maxima[0][0]
        padres[numero_padres, :] = poblacion[similitud_maxima, :]
        similitudes[similitud_maxima] = -1 # Se pone la similitud del padre seleccionado en -1 para no seleccionarlo en una proxima iteracion

    return padres

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

plt.imshow(final)
plt.show() # Prueba para ver la imagen invertida

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

poblacion = poblacion_inicial(final.shape)
print(len(poblacion))
similitudes = calcular_todas_similitudes(silueta_cromosoma, poblacion)

# se deberia meter este codigo en un loop cuya condicion para deneterse es que tenga una minima cantidad de similitud con la silueta
padres = seleccion(poblacion, similitudes, len(poblacion)/2)

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