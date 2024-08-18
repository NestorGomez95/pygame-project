import pygame
from level1 import Level1
from level2 import Level2

# Configuración básica
WIDTH = 800
HEIGHT = 600
FPS = 60

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar el primer nivel
current_level = Level1()
level_number = 1  # Variable para rastrear el nivel actual

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

    # Verificar si se ha completado el nivel actual
    if current_level.game_over and current_level.knight_won:
        if level_number == 1:
            # Si se completó el nivel 1, cargar el nivel 2
            current_level = Level2()
            level_number = 2
        elif level_number == 2:
            # Si se completó el nivel 2, finalizar el juego o manejarlo como desees
            print("Juego completado. ¡Felicidades!")
            running = False  # Puedes cambiar esto para hacer algo más después de completar ambos niveles

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
