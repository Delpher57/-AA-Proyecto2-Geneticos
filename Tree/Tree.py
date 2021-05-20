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
parameter_array = [] # En este arreglo van todas las generaciones de parametros de arboles creadas
global generation
generation = 0 # La generacion actual de arboles generados
global current_parameter_set
current_parameter_set = [] # Arreglo auxiliar donde se inserta el set actual de parametros
global parametros_seleccionados
parametros_seleccionados = [] # Arreglo auxiliar donde se insertan los parametros de arboles seleccionados con la funcion de seleccion

def imagen_a_vector(img_arr):
    # Esta funcion convierte una imagen (siendo un arreglo numpy obtenido al usar la funcion imread) a un vector
    # Entrada: Un arreglo numpy de imagen
    # Salida: La imagen convertida a un vector

    vector = numpy.reshape(a=img_arr, newshape=(functools.reduce(operator.mul, img_arr.shape)))
    return vector

def vector_a_imagen(vector, forma_imagen):
    # Esta funcion convierte un vector de una imagen a su forma original
    # Entrada: Un vector
    # Salida: Un arreglo numpy de imagen

    array_imagen = numpy.reshape(a=vector, newshape=forma_imagen)
    return array_imagen

def poblacion_inicial(forma_silueta, num_poblacion_inicial): # Funcion de poblacion inicial
    global current_parameter_set
    global parameter_array
    global generation

    # Esta funcion genera la poblacion inicial para el algoritmo genetico
    # Entrada: La forma de la imagen silueta, el numero de la poblacion inicial
    # Salida: Un arreglo con la poblacion inicial de arboles

    pob_inicial = numpy.empty(shape=(num_poblacion_inicial,
                                         functools.reduce(operator.mul, forma_silueta)),
                                  dtype=numpy.uint8) # Se genera un arreglo numpy vacio donde se generaran los arboles de la poblacion inicial
    i = 0
    current_parameter_set = [] # Se hace un arreglo auxiliar donde se insertara cada set de parametros usados para generar un arbol
    for indv_num in range(num_poblacion_inicial):
        # Genera aleatoriamente los parametros de los arboles de la poblacion inicial
        x1 = random.randrange(100,301)
        y1 = random.randrange(300,501)
        angle = random.randrange(-100,-60)
        depth = random.randrange(5,11)

        drawTree(x1,y1,angle,depth, False) # Se dibuja el arbol
        current_parameter_set.append([x1,y1,angle,depth]) # Se guardan los parametros usados en un arreglo de parametros
        filename = "current_tree%s" %i
        pygame.image.save(window, filename + ".jpeg")  # Se guarda el arbol dibujado como una imagen
        color = (0, 0, 0)
        screen.fill(color) # Se resetea la pantalla para poder dibujar otro arbol luego
        current_tree = cv2.imread(
            filename + ".jpeg")  # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original

        current_vector= imagen_a_vector(current_tree) # Se convierte la imagen del arbol a un vector para facilitar la seleccion luego

        pob_inicial[indv_num, :] = current_vector # Se guarda el arbol actual en la poblacion inicial
        i = i + 1

    parameter_array.insert(generation, current_parameter_set) # Se inserta un arreglo con los arreglos de parametros como la primera generacion de arboles generados
    current_parameter_set = []
    generation += 1 # Se incrementa la generacion actual
    pygame.display.flip()
    print(parameter_array[0])
    return pob_inicial

def funcion_adaptabilidad(vector_silueta, vector_arbol_generado):
    # Esta funcion calcula la fitness de un arbol generado
    # Entrada: El vector de la silueta y el vector del arbol generado
    # Salida: El valor de fitness del arbol generado

    diferencia = numpy.mean(numpy.abs(vector_silueta - vector_arbol_generado)) # Se calcula la media de las diferencias entre los elementos del vector de la silueta y el vector del arbol generado
    similitud = numpy.sum(vector_silueta) - diferencia # Para que mientras mayor sea el valor mejor sea la fitness, entonces se le resta el valor previo a la suma de todos los elementos del vector silueta
    # Mientras mas alto sea el valor de esta resta, entonces mejor es la fitness del arbol generado, porque significa que la diferencia entre la silueta y el arbol generado es mas baja
    return similitud # Se retorna el valor del fitness del arbol generado

def calcular_todas_similitudes(vector_silueta, poblacion):
    # Esta funcion calcula la fitness de todos los arboles de una poblacion
    # Entrada: El vector de la silueta, una poblacion de arboles generados
    # Salida: Un arreglo con los valores de fitness de los arboles de la poblacion

    array_similitudes = numpy.zeros(poblacion.shape[0]) # Se crea un arreglo de similitudes del tamano de la poblacion

    for individuo in range(poblacion.shape[0]): # Para cada arbol de la poblacion, se calcula su fitness, y esta se agrega al arreglo de los valores de fitness
        array_similitudes[individuo] = funcion_adaptabilidad(vector_silueta, poblacion[individuo, :])

    return array_similitudes

def seleccion(poblacion, similitudes, numero_padres):
    # Esta funcion selecciona los arboles mas similares a la silueta para usarlos como padres
    # Entrada: Una poblacion de arboles generados, un arreglo de valores de fitness de estos arboles, el numero de padress que se desea seleccionar
    # Salida: Un arreglo con los padres seleccionados

    global parameter_array
    global generation
    global parametros_seleccionados

    parametros_seleccionados = [] # Se define un arreglo auxiliar para los parametros de arbol actuales

    i = 0
    for padre in range(numero_padres): # Se calcula el valor de fitness y si coincide con el valor maximo de fitness de la poblacion se agrega al array de padres
        # Esto se hace hasta que se alcance la cantidad de padres que se pidio
        similitud_maxima = numpy.where(similitudes == numpy.max(similitudes))
        print(similitud_maxima[0][0])
        similitud_maxima = similitud_maxima[0][0] # Se obtienen los indices de la poblacion seleccionada
        parametros_seleccionados.append(parameter_array[generation-1][similitud_maxima])
        similitudes[similitud_maxima] = -1 # Se pone la similitud del padre seleccionado en -1 para no seleccionarlo en una proxima iteracion
        i += 1

    padres = parametros_seleccionados # Los padres serian los parametros de arboles que se seleccionaron
    return padres

def cruce(padres, num_individuos, forma_silueta):
    # Esta funcion crea la nueva poblacion cruzando dos parametros para generar hijos
    # Entrada: Arreglo de padres seleccionados, numero de individuos que se desea generar, la forma de la imagen silueta
    # Salida: Nueva poblacion de arboles producto del cruzamiento

    global generation
    global parameter_array

    permutaciones_usadas = []
    nueva_poblacion = []

    while len(nueva_poblacion) < num_individuos//2: # La cantidad de hijos que se genera es la mitad de la cantidad de individuos que se quiere generar
        permutacion_padres = random.sample(padres,2) # Se genera una permutacion random de padres

        if permutacion_padres in permutaciones_usadas: # Si ya se habia usado, se saca otra
            while permutacion_padres in permutaciones_usadas:
                permutacion_padres = random.sample(padres, 2)

        permutaciones_usadas.append(permutacion_padres)
        print(permutacion_padres)

        crossover_point = random.randrange(1,5) # Se escoje un punto de crossover al azar
        hijo = [[],[],[],[]]
        i = crossover_point
        remainder = 4 - crossover_point
        indice = 0
        while i != 0: # Se cruzan los genes de un padre hasta ese crossover point escogido
            hijo[indice] = permutacion_padres[0][indice]
            i = i - 1
            indice = indice + 1

        while remainder != 0: # Luego de llegar al crossover point, se cruzan los genes del otro padre
            hijo[indice] = permutacion_padres[0][indice]
            remainder = remainder - 1
            indice = indice + 1

        print(hijo)
        hijo = mutacion(hijo,5) # Se muta el hijo
        print(hijo)
        nueva_poblacion.append(hijo)

    for padre in padres: # La otra mitad de la nueva poblacion seran los padres usados, por si acaso los hijos recien creados tienen peores genes que los padres
        # En ese caso entonces la seleccion escogera a los padres y asi se evitara la regresion en la nueva generacion
        nueva_poblacion.append(padre)
        print(len(nueva_poblacion))

    print(nueva_poblacion)
    parameter_array.insert(generation, nueva_poblacion) # Se insertan los parametros de la nueva generacion en el arreglo de parametros de cada generacion de arboles
    print(parameter_array[generation])

    pob_imagenes_nueva = numpy.empty(shape=(num_individuos, # Se crea un arreglo donde se insertaran las imagenes de los arboles que se van a generar usando los nuevos parametros creados via cruce
                                     functools.reduce(operator.mul, forma_silueta)),
                              dtype=numpy.uint8)

    i = 0
    for indv_num in range(num_individuos): # Se dibujan todos los arboles de la generacion nueva, para poder guardar sus imagenes y convertirlas a vectores para poder usar en la siguiente seleccion
        # Genera aleatoriamente los valores geneticos de los cromosomas de la poblacion inicial
        color = (0, 0, 0)
        screen.fill(color)
        #pygame.display.flip()
        drawTree(parameter_array[generation][i][0], parameter_array[generation][i][1], parameter_array[generation][i][2], parameter_array[generation][i][3], False)
        filename = "current_tree%s" % i
        pygame.image.save(window, filename + ".jpeg")  # Se guarda el arbol dibujado como una imagen
        color = (0, 0, 0)
        screen.fill(color)
        time.sleep(0.04)
        current_tree = cv2.imread(
            filename + ".jpeg")  # Se lee la imagen del arbol generado para luego compararla con la imagen de la silueta original

        current_vector = imagen_a_vector(current_tree) # Se convierte la imagen a un vector para usar en la siguiente seleccion

        pob_imagenes_nueva[indv_num, :] = current_vector # Se guarda el vector de la imagen del arbol en el arreglo de imagenes de la nueva poblacion
        i = i + 1

    generation += 1 # Se incrementa el numero de la generacion actual
    pygame.display.flip()
    print(pob_imagenes_nueva)

    return pob_imagenes_nueva

def mutacion(parametros, porcentaje_mutacion):
    # Esta funcion muta un parametro random de un arreglo de parametros
    # Entrada: Arreglo de parametros de un arbol, porcentaje por el que se va a mutar el parametro
    # Salida: El arreglo de parametros con un parametro al azar mutado

    decision_random = random.choice([True, False]) # Si se escogio True se le va a sumar al parametro mutado, si es False entonces se le resta
    indice = random.randrange(0,len(parametros)-1) # Se escoge el indice del parametro al que se va a mutar
    parametro_mutar = parametros[indice]
    porcentaje_parametro = (porcentaje_mutacion*parametro_mutar) / 100.0 # Se calcula el porcentaje por el que se va a mutar el parametro escogido

    if decision_random: # Dependiendo de si se escogio True o False se le suma o resta al parametro escogido para mutar
        parametro_mutar += porcentaje_parametro
    else:
        parametro_mutar -= porcentaje_parametro

    parametros[indice] = parametro_mutar
    return parametros # Se retorna el arreglo de parametros con el parametro mutado

def drawTree(x1, y1, angle, depth, final):
    # Esta funcion dibuja un arbol con los parametros dados
    # Entrada: Coordenada x1, coordenada y1, el angulo, la profundidad, y un boolean que indica si es el arbol escogido como respuesta final o no
    # Salida: Dibuja un arbol en la pantalla

    # time.sleep(.001)

    if final:
        pygame.display.flip()
    fork_angle = 20 - (random.random())
    base_len = 10.0 - (random.random())
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        y2 = y1 + int(math.sin(math.radians(angle + random.random())) * depth * base_len * (random.random() + 0.5))
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
        drawTree(x2, y2, angle - fork_angle, depth - 1, final)
        drawTree(x2, y2, angle + fork_angle, depth - 1, final)



#------------------------------------Se lee y convierte la imagen de la silueta a un numpy array-------------------------------------------------------------------
imageFileName = input("Escriba el nombre de la imagen: ")
my_img = cv2.imread(imageFileName) # Se lee la imagen de la silueta
inverted_img = (255.0 - my_img) # Se invierte para que el arbol quede en blanco y el fondo en negro, de esta manera se parece mas a como se ven los arboles dibujados por drawTree
final = inverted_img / 255.0

plt.imshow(final)
plt.show() # Prueba para ver la imagen invertida

silueta_vector = imagen_a_vector(final) # Se convierte la imagen de la silueta a un vector para ser usada en la seleccion
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------Se dibuja el arbol y se guarda la imagen del arbol dibujado como un numpy array----------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

poblacion = poblacion_inicial(final.shape) # Se genera la poblacion inicial
similitudes = calcular_todas_similitudes(silueta_vector, poblacion) # Se calculan los valores de fitness de la poblacion inicial
print(similitudes)

arbol_final = []
print(numpy.max(similitudes))
while numpy.max(similitudes) < 286449.5: # El loop del algoritmo genetico, se detiene cuando el arbol sea lo suficientemente similar al arbol de la silueta
    padres = seleccion(poblacion, similitudes, len(poblacion)//2) # Se seleccionan los padres de la poblacion
    poblacion = cruce(padres,len(poblacion),final.shape) # Se cruza la poblacion para generar una nueva poblacion
    similitudes = calcular_todas_similitudes(silueta_vector,poblacion) # Se calculan los valores de fitness de la poblacion
    print(similitudes)

    arbol_final = []
    if numpy.max(similitudes) >= 286449.5: # Si se ha generado un arbol que se parece lo suficiente al arbol de la silueta, entonces se guarda el valor de ese arbol para dibujarlo
        similitud_maxima = numpy.where(similitudes == numpy.max(similitudes))
        print(similitud_maxima[0][0])
        similitud_maxima = similitud_maxima[0][0]  # Se obtienen los indices de la poblacion seleccionada
        arbol_final = parameter_array[generation - 1][similitud_maxima]
        break

print(arbol_final)
print(parameter_array[generation - 1][similitud_maxima])
drawTree(arbol_final[0],arbol_final[1],arbol_final[2],arbol_final[3], True) # Se dibuja el arbol final
print("Final")
def input(event):
    if event.type == pygame.QUIT:
        exit(0)

    if event.type == KEYDOWN:

        # si apretamos abajo se hace otro arbol
        if event.key == K_DOWN:
            screen.fill((0, 0, 0))
            # drawTree(300, 550, -90, 8)
            drawTree(300, 550, -90, 8, True)

while True:
    input(pygame.event.wait())
    pygame.display.flip()
#----------------------------------------------------------------------------------------------------------------------------------------------------------