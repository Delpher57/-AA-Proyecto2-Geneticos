import itertools
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

global parameter_array
parameter_array = []
global generation
generation = 0
global current_parameter_set
current_parameter_set = []
global parametros_seleccionados
parametros_seleccionados = []

def imagen_a_cromosoma(img_arr):
    cromosoma = numpy.reshape(a=img_arr, newshape=(functools.reduce(operator.mul, img_arr.shape)))
    return cromosoma

def cromosoma_a_imagen(cromosoma, forma_imagen):
    array_imagen = numpy.reshape(a=cromosoma, newshape=forma_imagen)
    return array_imagen

def poblacion_inicial(forma_silueta, num_poblacion_inicial=8): # Aqui se deberia dibujar arboles random como poblacion inicial
    global current_parameter_set
    global parameter_array
    global generation

    pob_inicial = numpy.empty(shape=(num_poblacion_inicial,
                                         functools.reduce(operator.mul, forma_silueta)),
                                  dtype=numpy.uint8)
    i = 0
    current_parameter_set = []
    for indv_num in range(num_poblacion_inicial):
        # Genera aleatoriamente los valores geneticos de los cromosomas de la poblacion inicial
        x1 = random.randrange(100,301)
        y1 = random.randrange(300,551)
        angle = random.randrange(-100,101)
        depth = random.randrange(1,11)

        drawTree(x1,y1,angle,depth, i)
        current_parameter_set.append([x1,y1,angle,depth])
        filename = "current_tree%s" %i
        pygame.image.save(window, filename + ".jpeg")  # Se guarda el arbol dibujado como una imagen
        color = (0, 0, 0)
        screen.fill(color)
        current_tree = cv2.imread(
            filename + ".jpeg")  # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original

        current_cromosoma= imagen_a_cromosoma(current_tree)

        pob_inicial[indv_num, :] = current_cromosoma
        i = i + 1

    parameter_array.insert(generation, current_parameter_set)
    current_parameter_set = []
    generation += 1
    pygame.display.flip()
    print(parameter_array[0])
    return pob_inicial

def funcion_adaptabilidad(cromosoma_silueta, cromosoma_arbol_generado):
    diferencia = cromosoma_silueta - cromosoma_arbol_generado
    similitud = numpy.mean(numpy.abs(diferencia))
    similitud = numpy.sum(cromosoma_silueta) - similitud
    return similitud

def calcular_todas_similitudes(cromosoma_silueta, poblacion):
    array_similitudes = numpy.zeros(poblacion.shape[0])

    for individuo in range(poblacion.shape[0]):
        array_similitudes[individuo] = funcion_adaptabilidad(cromosoma_silueta, poblacion[individuo, :])

    return array_similitudes

def seleccion(poblacion, similitudes, numero_padres):
    global parameter_array
    global generation
    global parametros_seleccionados

    padres = numpy.empty((numero_padres,poblacion.shape[1]),dtype=numpy.uint8)
    parametros_seleccionados = []

    i = 0
    for padre in range(numero_padres):
        similitud_maxima = numpy.where(similitudes == numpy.max(similitudes))
        print(similitud_maxima[0][0])
        similitud_maxima = similitud_maxima[0][0] # Se obtienen los indices de la poblacion seleccionada
        parametros_seleccionados.append(parameter_array[generation-1][similitud_maxima])
        similitudes[similitud_maxima] = -1 # Se pone la similitud del padre seleccionado en -1 para no seleccionarlo en una proxima iteracion
        i += 1

    padres = parametros_seleccionados
    return padres

def cruce(padres, num_individuos):
    global generation
    global parameter_array

    permutaciones_usadas = []
    nueva_poblacion = []

    while len(nueva_poblacion) < num_individuos//2:
        permutacion_padres = random.sample(padres,2)

        if permutacion_padres in permutaciones_usadas:
            while permutacion_padres in permutaciones_usadas:
                permutacion_padres = random.sample(padres, 2)

        permutaciones_usadas.append(permutacion_padres)
        print(permutacion_padres)
        hijo = [permutacion_padres[0][0],permutacion_padres[0][1],permutacion_padres[1][2],permutacion_padres[1][3]]
        hijo = mutacion(hijo,5)
        print(hijo)
        nueva_poblacion.append(hijo)

    for padre in padres:
        nueva_poblacion.append(padre)
        print(len(nueva_poblacion))

    print(nueva_poblacion)
    generation += 1
    parameter_array.insert(generation, nueva_poblacion)
    print(parameter_array)
    return nueva_poblacion

def mutacion(parametros, porcentaje_mutacion):
    decision_random = random.choice([True, False])
    parametro_mutar = parametros[random.randrange(0,len(parametros)-1)]
    print(parametro_mutar)
    porcentaje_parametro = (porcentaje_mutacion*parametro_mutar) / 100.0
    print(porcentaje_parametro)

    if decision_random:
        parametro_mutar += porcentaje_parametro
    else:
        parametro_mutar -= porcentaje_parametro

    print(parametro_mutar)
    return parametro_mutar

def drawTree(x1, y1, angle, depth, tree_number):
    # time.sleep(.001)

    pygame.display.flip()
    fork_angle = 20 - (random.random())
    base_len = 10.0 - (random.random())
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        y2 = y1 + int(math.sin(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
        drawTree(x2, y2, angle - fork_angle, depth - 1, tree_number)
        drawTree(x2, y2, angle + fork_angle, depth - 1, tree_number)



#------------------------------------Se lee y convierte la imagen de la silueta a un numpy array-------------------------------------------------------------------
imageFileName = input("Escriba el nombre de la imagen: ")
my_img = cv2.imread(imageFileName) # Se lee la imagen
inverted_img = (255.0 - my_img) # Se invierte para que el arbol quede en blanco
final = inverted_img / 255.0

plt.imshow(final)
plt.show() # Prueba para ver la imagen invertida

silueta_cromosoma = imagen_a_cromosoma(final) # Se convierte la imagen de la silueta a una cromosoma del algoritmo genetico
#------------------------------------Se lee y convierte la imagen de la silueta a un numpy array------------------------------------------------------------------

#------------------------------------Se dibuja el arbol y se guarda la imagen del arbol dibujado como un numpy array----------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

poblacion = poblacion_inicial(final.shape)
similitudes = calcular_todas_similitudes(silueta_cromosoma, poblacion)

# se deberia meter este codigo en un loop cuya condicion para deneterse es que tenga una minima cantidad de similitud con la silueta
padres = seleccion(poblacion, similitudes, len(poblacion)//2)
print(parametros_seleccionados)
print(len(parametros_seleccionados))
print(len(poblacion))
cruce(padres,len(poblacion))


def input(event):
    if event.type == pygame.QUIT:
        exit(0)

    if event.type == KEYDOWN:

        # si apretamos abajo se hace otro arbol
        if event.key == K_DOWN:
            screen.fill((0, 0, 0))
            # drawTree(300, 550, -90, 8)
            drawTree(300, 550, -90, 8, 0)

while True:
    input(pygame.event.wait())
    pygame.display.flip()
#------------------------------------Se dibuja el arbol y se guarda la imagen del arbol dibujado como un numpy array----------------------------------------------