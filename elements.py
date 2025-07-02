
import pygame
import constants
import os
import math


class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wood = 5

        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        self.image = pygame.image.load(tree_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.TREE, constants.TREE))
        self.size = self.image.get_width()



    def draw(self, screen, camera_x, camera_y):
        #calcular posicion en pantalla relativa a la camara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        #aolo dibujar si esta en pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGTH):
            screen.blit(self.image, (screen_x, screen_y))

    def chop(self, with_axe=False):
        if self.wood > 0:
            if with_axe:
                self.wood -= 2
                if self.wood < 0:
                    self.wood = 0
            else:         
                self.wood -= 1        
            return True
        return False

    def is_depleted(self):
        return self.wood <= 0
        

class SmallStone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stone = 1
        
        stone_path = os.path.join('assets', 'images', 'objects', 'small_stone.png')
        self.image = pygame.image.load(stone_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.SMALL_STONE, constants.SMALL_STONE))
        self.size = self.image.get_width()

    def draw(self, screen, camera_x, camera_y):
        #calcular posicion en pantalla relativa a la camara
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        #aolo dibujar si esta en pantalla
        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGTH):
            screen.blit(self.image, (screen_x, screen_y))

    def collect(self):
        if self.stone > 0:
            self.stone -= 1
            return True
        return False     
       
    def is_depleted(self):
        return self.stone <= 0


class FarmLand:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_watered = False
        self.growth_stage = 0
        self.las_update_time =pygame.time.get_ticks()

    # cargar todas las imagenes de tierra de cultivo
        self.images = {}
        for i in range(1, 7):
            path = os.path.join('assets', 'images', 'objects', 'Farm', f'Farmland{i}.png')
            self.images[i] = pygame.image.load(path).convert_alpha()
            self.images[i] = pygame.transform.scale(self.images[i], (constants.GRASS, constants.GRASS)) 

        self.size = constants.GRASS    

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGTH):
            image_key = min(6, max(1, self.growth_stage + 1))
            screen.blit(self.images[image_key], (screen_x, screen_y))   

    def water(self):
        """regar la tierra de cultivo"""
        if not self.is_watered:
            self.is_watered = True
            self.las_update_time = pygame.time.get_ticks()     
            return True
        return False   
    
    def update(self, current_time):
        """actualizar crecimiento basado en el tiempo transcurrido"""
        #solo crecer si esta regada"
        if self.is_watered and self.growth_stage < 5:
            #verificar si ha ásado tiempo para crecer(5 minutos de juego = 10 segundos de tiempo real)
            if self.growth_stage == 0:
                self.growth_stage = 1
            if current_time - self.las_update_time > 10000:
                self.growth_stage = min(5, self.growth_stage + 1)   
                self.las_update_time = current_time

    def harvest(self):
        """cocechar cultivos si estan completamente crecidos"""
        if self.growth_stage == 5:
            harvested = True
            self.growth_stage = 0
            self.is_watered = False
            return harvested
        return False            


class Water:
    def __init__(self, x, y, is_flowing=False):
        self.x = x
        self.y = y
        self.is_flowing = is_flowing # para diferenciar rios de lagos
        self.is_drinkable = True
        self.size = constants.GRASS
        # para animacion simple
        self.animation_frame = 0
        self.animation_timer = 0         

    def update (self, dt):
        #animacion simple del agua
        self.animation_timer += dt
        if self.animation_timer > 500: #cambiar frame cada 500ms
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4           

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        if (screen_x + self.size >= 0 and screen_x <= constants.WIDTH and
                screen_y + self.size >= 0 and screen_y <= constants.HEIGTH):
            # crear un rectangulo para el agua
            water_text = pygame.Rect(screen_x, screen_y, self.size, self.size)

            #aplicar un pequeño offset basado en animation_frame para crear efecto de odulacion
            offset_y = math.sin(self.animation_frame * math.pi / 2) * 2

            #dibujar el agua como un rectangulo con el color definido en constants
            pygame.draw.rect(screen, constants.WATER_COLOR,
                             pygame.Rect(screen_x, screen_y + offset_y, self.size, self.size))        