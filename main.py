import pygame
import sys
import constants
from character import Character
from world import World

#inicializar pygame
pygame.init()

WIDTH, HEIGTH = 800, 600
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGTH))
pygame.display.set_caption("Simulador de Vida Salvaje")

def main():

    clock = pygame.time.Clock()
    world = World(constants.WIDTH, constants.HEIGTH)
    character = Character(constants.WIDTH // 2, constants.HEIGTH // 2)
    show_inventory = False

    status_update_time = 0

    camera_x = 0
    camera_y = 0


    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    character.interact(world)
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory      
                if event.key == pygame.K_f:
                    character.update_food(20) 
                if event.key == pygame.K_c:
                    character.update_thirst(20) 
        # manejar eventos del mouse para el inventario            
        if event.type == pygame.MOUSEBUTTONDOWN:
            character.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)

        dx = dy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5 
        
        #actualizar el estado de corriendo
        character.is_running = keys[pygame.K_LSHIFT] and character.stamina > 0
        character.move(dx, dy, world)

        # la camara sigue al personaje
        camera_x = character.x - constants.WIDTH // 2
        camera_y = character.y - constants.HEIGTH // 2

        # actualizar chunks basado enlaposicion del personajee
        world.update_chunks(character.x, character.y)



        status_update_time += dt
        if status_update_time >= constants.STATUS_UPDATE_INTERVAL:
            character.update_status()
            status_update_time = 0

        if character.energy <= 0 or character.food <= 0 or character.thirst <= 0 :
            pygame.quit()
            sys.exit()

        #limpiar la pantalla
        screen.fill((0, 0, 0))
           
                                     
        

        world.update_time(dt)
        world.draw(screen, camera_x, camera_y)        
        character.draw(screen, camera_x, camera_y)
        if show_inventory:
            character.draw_inventory(screen) 

        #dibujar inventario ( hotbar siempre visible + inventario principal si esta abierto)
        character.draw_inventory(screen, show_inventory)    

        # dibujar HUD
        font = pygame.font.Font(None, 24)
        energy_text = font.render(f"Energy: {int(character.energy)}", True, constants.WHITE)
        food_text = font.render(f"Food: {int(character.food)}", True, constants.WHITE)
        thirst_text = font.render(f"Thirst: {int(character.thirst)}", True, constants.WHITE)
        stamina_text = font.render(f"Stamina: {int(character.stamina)}", True, constants.WHITE)
        #añadir indicador de tiempo
        time_of_day = (world.current_time / constants.DAY_LENGTH) * 24 #convertir a formato 24 hrs.
        time_text = font.render(f"Time: {int(time_of_day):02d}:00", True, constants.WHITE)



        screen.blit(energy_text, (10, constants.HEIGTH -115))
        screen.blit(food_text, (10, constants.HEIGTH -90))
        screen.blit(thirst_text,(10, constants.HEIGTH -65))
        screen.blit(stamina_text, (10, constants.HEIGTH -40))
        screen.blit(time_text, (10, constants.HEIGTH - 15))

        

        pygame.display.flip()
           

if __name__ == "__main__":
    main()





