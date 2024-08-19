import pygame
from level1 import Level1
from level3 import Level3
from level4 import Level4

# Configuración básica
WIDTH = 800
HEIGHT = 600
FPS = 70

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar el primer nivel
current_level = Level3()
level_number = 3

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Delegar eventos de teclado al nivel actual
        current_level.handle_event(event)

    # Actualizar y dibujar el nivel actual
    current_level.update()
    current_level.draw(screen)

    if current_level.game_over and current_level.knight_won:
        if level_number == 3:
            current_level = Level4()
            level_number = 4
        elif level_number == 4:
            print("Juego completado. ¡Felicidades!")
            running = False

    pygame.display.flip()
    clock.tick(FPS)  # Asegúrate de que el FPS esté configurado correctamente

pygame.quit()
