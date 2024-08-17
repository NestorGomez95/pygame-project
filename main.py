import pygame
from level1 import Level1

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

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Delegar eventos de teclado al nivel actual
        current_level.handle_event(event)

    # Limpiar la pantalla antes de dibujar
    screen.fill((0, 0, 0))  # Fondo negro

    # Actualizar y dibujar el nivel actual
    current_level.update()
    current_level.draw(screen)

    # Verificar si el nivel ha sido completado
    if current_level.is_completed():
        print("Nivel completado")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
