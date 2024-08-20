import pygame
from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4

# Configuración básica
WIDTH = 800
HEIGHT = 600
FPS = 60

# Inicializar Pygame y el módulo de sonido
pygame.init()
pygame.mixer.init()  # Inicializa el módulo de sonido

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Lista de niveles y sus respectivas músicas
levels = [
    (Level1, 'music/creepy_maze.wav'),
    (Level2, 'music/creepy_maze.wav'),
    (Level3, 'music/final_levels.mp3'),
    (Level4, 'music/final_levels.mp3')
]

current_level_index = 0
current_level, current_music = levels[current_level_index]

# Cargar el primer nivel y su música
current_level = current_level()
pygame.mixer.music.load(current_music)
pygame.mixer.music.set_volume(0.3)  # Ajusta el volumen al 50%
pygame.mixer.music.play(loops=-1)  # Reproduce la música en bucle

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
        current_level_index += 1
        if current_level_index < len(levels):
            current_level, current_music = levels[current_level_index]
            current_level = current_level()

            # Detener la música actual y cargar la nueva música para el siguiente nivel
            pygame.mixer.music.stop()
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen al 50% para el siguiente nivel
            pygame.mixer.music.play(loops=-1)
        else:
            print("Juego completado. ¡Felicidades!")
            running = False  # Finalizar el juego si se han completado todos los niveles

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
