import pygame
import sys
import random
import time

pygame.init()

def main_game_loop():
    pygame.init()
    final = False
    start_game = False
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    puntos = 0
    vidas = 5
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Ventana de Juego")
    
    rect_x = 350
    rect_y = 500
    rect_width = 100
    rect_height = 50
    rect_speed = 1.3
    
    fruits = []
    bad_fruits = []
    
    speed_multiplier = 1.0
    max_speed_multiplier = 5.0  # Establece el valor máximo del multiplicador de velocidad
    
    speed_increase_interval = 5
    last_speed_increase_time = 0
    
    class Fruit:
        def __init__(self):
            self.x = random.randint(0, window_size[0] - 30)
            self.y = 0
            self.speed = 0.4
    
        def move(self):
            self.y += self.speed * speed_multiplier
    
        def draw(self):
            pygame.draw.circle(screen, (255, 0, 0), (self.x, int(self.y)), 15)
    
    class BadFruit:
        def __init__(self):
            self.x = random.randint(0, window_size[0] - 30)
            self.y = 0
            self.speed = 0.4
    
        def move(self):
            self.y += self.speed * speed_multiplier
    
        def draw(self):
            pygame.draw.circle(screen, (0, 0, 255), (self.x, int(self.y)), 15)
    
    last_fruit_time = time.time()
    generate_bad_fruit = False
    
    def draw_text(text, x, y, color=BLACK, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 670 <= mouse_x <= 770 and 30 <= mouse_y <= 80:
                    start_game = True
                    running = False
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect_x -= rect_speed
        if keys[pygame.K_RIGHT]:
            rect_x += rect_speed
        if rect_x > 860:
            rect_x = -50
        if rect_x < -60:
            rect_x = 850
    
        current_time = time.time()
        if current_time - last_speed_increase_time >= speed_increase_interval:
            if speed_multiplier < max_speed_multiplier:
                speed_multiplier *= 1.2  # Incrementa el multiplicador de velocidad en un 50%
            last_speed_increase_time = current_time
    
        for fruit in fruits:
            fruit.move()
            if fruit.y > window_size[1]:
                fruits.remove(fruit)
                vidas -= 1
                print(vidas)
            elif (rect_x < fruit.x < rect_x + rect_width and rect_y < fruit.y < rect_y + rect_height):
                fruits.remove(fruit)
                puntos += 1
                print(puntos)
    
        for bad_fruit in bad_fruits:
            bad_fruit.move()
            if bad_fruit.y > window_size[1]:
                bad_fruits.remove(bad_fruit)
            elif (rect_x < bad_fruit.x < rect_x + rect_width and rect_y < bad_fruit.y < rect_y + rect_height):
                bad_fruits.remove(bad_fruit)
                vidas -= 1
                print(vidas)
    
        screen.fill(BLACK)
        draw_text(f"Puntaje: {puntos}", 20, 20, color=WHITE, font_size=24)
        draw_text(f"Vidas: {vidas}", 20, 60, color=WHITE, font_size=24)
        pygame.draw.rect(screen, (240, 240, 240), (670, 30, 100, 50))
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))
    
        for fruit in fruits:
            fruit.draw()
    
        for bad_fruit in bad_fruits:
            bad_fruit.draw()
    
        pygame.display.flip()
    
        if vidas <= 0:
            start_game = True
            final = True
            break
    
        current_time = time.time()
        if current_time - last_fruit_time >= 2.0:
            if generate_bad_fruit:
                bad_fruits.append(BadFruit())
            else:
                fruits.append(Fruit())
            last_fruit_time = current_time
            generate_bad_fruit = not generate_bad_fruit
    
    if final:
        screen.fill(WHITE)
        draw_text("¡Juego terminado!", 250, 200, color=BLACK, font_size=36)
        draw_text(f"Tu puntaje: {puntos}", 240, 280, color=BLACK, font_size=36)
        pygame.display.flip()
        pygame.time.wait(2000)
    
    pygame.quit()
    
    if start_game:
        from menu import main_game_loo
        main_game_loo()
        
main_game_loop()
