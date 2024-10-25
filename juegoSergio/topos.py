import pygame
import random
import sys
import time

def main_game_loop_t():
    # Inicialización de Pygame
    pygame.init()
    # Configuración de la pantalla
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Atrapatopos")
    # Definir la variable de cierre
    final = False
    start_game = False
    # Colores
    background_color = (255, 255, 255)
    topo_color = (0, 0, 0)

    # Tamaño del topo
    topo_radius = 20

    # Puntuación inicial
    score = 0

    # Tiempo total en segundos
    total_time = 30

    # Fuentes para texto
    font = pygame.font.Font(None, 36)

    def draw_text(text, x, y):
        text_surface = font.render(text, True, topo_color)
        screen.blit(text_surface, (x, y))

    # Cuadrícula
    grid_rows = 6
    grid_cols = 6
    cell_width = width // grid_cols
    cell_height = (height - 100) // grid_rows  # Ajusta la altura de la celda para que quepa completamente
    grid_offset_y = 80  # Espacio en la parte superior

    # Bucle principal del juego
    running = True
    clock = pygame.time.Clock()

    def new_topo_position():
        x = random.randint(0, grid_cols - 1)
        y = random.randint(0, grid_rows - 1)  # Asegura que el topo no se salga de la pantalla
        return x * cell_width + cell_width // 2, y * cell_height + cell_height // 2 + grid_offset_y

    topo_x, topo_y = new_topo_position()

    # Inicializar el temporizador
    start_time = time.time()
    last_topo_change_time = start_time
    topo_change_interval = 3  # Cambiar la posición del topo cada 3 segundos
    topo_change_time = start_time  # Nuevo: seguimiento del tiempo de cambio del topo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Cerrar Pygame
                sys.exit()  # Salir del programa por completo
                running = False

        # Lógica del juego
        elapsed_time = time.time() - start_time
        time_left = max(total_time - elapsed_time, 0)  # Asegura que el tiempo no sea negativo

        if time_left == 0:
            final = True
            start_game = True
            break

        # Verificar si ha pasado el intervalo de cambio de posición
        if time.time() - topo_change_time >= topo_change_interval:
            topo_x, topo_y = new_topo_position()
            topo_change_time = time.time()  # Actualizar el tiempo de cambio del topo

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = ((topo_x - mouse_x) ** 2 + (topo_y - mouse_y) ** 2) ** 0.5
            if distance < topo_radius:
                score += 1
                topo_x, topo_y = new_topo_position()
                topo_change_time = time.time()  # Reiniciar el temporizador de cambio del topo

        screen.fill(background_color)

        pygame.draw.circle(screen, topo_color, (topo_x, topo_y), topo_radius)
        # Estas líneas las borras cuando el fondo esté acomodado
        # -------------------------------------------------------
        for x in range(0, width, cell_width):
            pygame.draw.line(screen, topo_color, (x, grid_offset_y), (x, height), 2)
        for y in range(grid_offset_y, height, cell_height):
            pygame.draw.line(screen, topo_color, (0, y), (width, y), 2)
        # -------------------------------------------------------

        pygame.draw.rect(screen, (240, 240, 240), (670, 20, 100, 50))
        draw_text(f"Puntuación: {score}", 10, 10)
        draw_text(f"Tiempo restante: {int(time_left)}", 10, 50)

        pygame.display.flip()
        clock.tick(60)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 770 >= mouse_x >= 670 and 70 >= mouse_y >= 20:
                start_game = True  # Esto indica que el juego debe iniciar

        if start_game:
            # Salir del bucle del juego y permitir iniciar el menú
            break

    # Pantalla de fin de juego
    if final:
        screen.fill((255, 255, 255))
        draw_text("¡Juego terminado!", 250, 200)
        draw_text(f"Tu puntaje: {score}", 240, 280)
        pygame.display.flip()
        pygame.time.wait(2000)

    # Salir del juego
    pygame.quit()

    if start_game:
        from menu import main_game_loo
        main_game_loo()

main_game_loop_t()
