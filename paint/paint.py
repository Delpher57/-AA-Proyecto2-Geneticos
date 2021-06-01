import pygame, sys
from pygame.locals import *
from PIL import Image,ImageChops
import random
import math


windowSurface = pygame.display.set_mode((1280, 720))

COLOR_5 = pygame.Color("#22577a")
COLOR_1 = pygame.Color("#c7f9cc")
COLOR_3 = pygame.Color("#57cc99")
COLOR_4 = pygame.Color("#38a3a5")

#paleta de colores del 1 al 5, de mas claro a mas oscuro:
COLOR_1 = pygame.Color("#c7f9cc")
COLOR_2 = pygame.Color("#80ed99")
COLOR_3 = pygame.Color("#57cc99")
COLOR_4 = pygame.Color("#38a3a5")
COLOR_5 = pygame.Color("#22577a")



pygame.init()


## font setup
menu_font = pygame.font.SysFont("consolas", 17)
clear_text = menu_font.render("Limpiar", True, COLOR_1)
brush_text = menu_font.render("Herramientas", True, COLOR_1)
save_text = menu_font.render("Iniciar", True, COLOR_1)


draw = False
brush_size = 5
brush_color = COLOR_5


menu_rect = pygame.Rect(0, 0, 150, 360)




tree_rect = pygame.Rect(640, 0, 640, 720)
left_scr_rect = pygame.Rect(0, 0, 640, 720)
pygame.draw.rect(windowSurface, COLOR_2, tree_rect)
pygame.draw.rect(windowSurface, COLOR_3, left_scr_rect)


drawing_canvas_rect = pygame.Rect(160, 20, 320, 360)
drawing_canvas_shadow_rect = pygame.Rect(170, 30, 320, 360)
pygame.draw.rect(windowSurface, COLOR_4, drawing_canvas_shadow_rect)


eraser_rect = pygame.Rect(27, 95, 40, 40)
draw_rect = pygame.Rect(72, 95, 40, 40)

thin_brush = pygame.Rect(72, 140, 40, 40)
medium_brush = pygame.Rect(72, 185, 40, 40)
thick_brush = pygame.Rect(27, 140, 40, 40)
supa_brush = pygame.Rect(27, 185, 40, 40)

clear_rect = pygame.Rect(27, 290, 90, 25)
save_rect = pygame.Rect(27, 260, 90, 25)
save_flag = False
file_number = 1



def get_diferencia(imagen):
    """[vara de prueba para ver las diferencias entre imagenes]

    Args:
        imagen ([pygame image]): [imagen que vamos a comparar]
    """    
    pil_string_image = pygame.image.tostring(imagen, "RGB",False)
    pil_image = Image.frombytes("RGB",(320,360),pil_string_image)
    #convertimos la imagen de pygame en una imagen de pillow


    img1 = Image.open("1.png")
    diff = ImageChops.difference(img1,pil_image)
    if diff.getbbox():
        diff.show()
        return



pygame.draw.rect(windowSurface, COLOR_4, drawing_canvas_rect, 5)
pygame.draw.rect(windowSurface, COLOR_1, drawing_canvas_rect)


while False:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            draw = True
        if event.type == MOUSEBUTTONUP:
            draw = False

        
    # dibujamos un circulo si se esta haciendo click
    mouse_pos = pygame.mouse.get_pos()
    if draw == True and drawing_canvas_rect.collidepoint(mouse_pos):
        pygame.draw.circle(windowSurface, brush_color, mouse_pos, brush_size)
        save_flag = False





    ## Detectamos si se hizo click en el boton del borrador
    if draw == True:
        if eraser_rect.collidepoint(mouse_pos):
            brush_color = COLOR_1
    
    ## Detectamos si se hizo click en el boton del lapiz
    if draw == True:
        if draw_rect.collidepoint(mouse_pos):
            brush_color = COLOR_5
    
    ## Detectamos si se hizo click en limpiar
    if draw == True:
        if clear_rect.collidepoint(mouse_pos):
            pygame.draw.rect(windowSurface, COLOR_4, drawing_canvas_rect, 5)
            pygame.draw.rect(windowSurface, COLOR_1, drawing_canvas_rect)

            
    
    pygame.draw.rect(windowSurface, COLOR_3, menu_rect)
    
    pygame.draw.rect(windowSurface, COLOR_4, clear_rect)
    windowSurface.blit(clear_text, (30, 295))


    windowSurface.blit(brush_text, (27, 70))
    

    pygame.draw.rect(windowSurface, COLOR_4, save_rect)
    windowSurface.blit(save_text, (30, 262))





    #detectamos si se hizo click en guardar
    if draw == True and save_flag == False:
        if save_rect.collidepoint(mouse_pos):
            print("File has been saved :P")
            save_surface = pygame.Surface((320, 360))
            save_surface.blit(windowSurface, (0, 0), (160, 20, 320, 360))
            get_diferencia(save_surface)
            save_flag = True
            
        




 ## collision detectin for BRUSH SIZE
    if draw == True:
        if thin_brush.collidepoint(mouse_pos):
            brush_size = 1
        if medium_brush.collidepoint(mouse_pos):
            brush_size = 3
        if thick_brush.collidepoint(mouse_pos):
            brush_size = 5
        if supa_brush.collidepoint(mouse_pos):
            brush_size = 10
    




    
    
    

    pygame.draw.rect(windowSurface, COLOR_1, eraser_rect)
    if brush_color == COLOR_1:
        border = 3
    else:
        border = 1
    pygame.draw.rect(windowSurface, COLOR_4, eraser_rect, border)

    pygame.draw.rect(windowSurface, COLOR_5, draw_rect)
    if brush_color == COLOR_5:
        border = 3
    else:
        border = 1
    
    pygame.draw.rect(windowSurface, COLOR_2, draw_rect, border)
 
 



    # Rect for brush size

    
    if brush_size == 1:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, COLOR_1, thin_brush, brush_border)
    pygame.draw.circle(windowSurface, COLOR_1, thin_brush.center, 1)
    pygame.draw.rect(windowSurface, COLOR_1, thin_brush, brush_border)
    
    
    if brush_size == 3:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, COLOR_1, medium_brush, brush_border)
    pygame.draw.circle(windowSurface, COLOR_1, medium_brush.center, 3)
    pygame.draw.rect(windowSurface, COLOR_1, medium_brush, brush_border)
    
    
    if brush_size == 5:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, COLOR_1, thick_brush, 1)
    pygame.draw.circle(windowSurface, COLOR_1, thick_brush.center, 5)
    pygame.draw.rect(windowSurface, COLOR_1, thick_brush, brush_border)
    
    
    if brush_size == 10:
        brush_border = 3
    else:
        brush_border = 1
    pygame.draw.rect(windowSurface, COLOR_1, supa_brush, brush_border)
    pygame.draw.circle(windowSurface, COLOR_1, supa_brush.center, 10)
    pygame.draw.rect(windowSurface, COLOR_1, supa_brush, brush_border)


    




    pygame.display.update()



