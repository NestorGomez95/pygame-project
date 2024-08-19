import pygame
import random


try:
    font = pygame.font.Font(None, 74)
    screen_middle = (self.WIDTH // 2, self.HEIGHT // 2)
    game_over_text = font.render("GAME OVER", True, (0, 255, 255))
    message = "You won!" if self.knight_won else "You lost!"
    text = font.render(message, True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=screen_middle)
    screen.blit(text, text_rect)
    if self.knight_won:
        won_text = font.render("You won!", True, (0, 255, 0))
    else:
        won_text = font.render("You lost!", True, (255, 0, 0))
    text_rect = won_text.get_rect(midtop=screen_middle)
    screen.blit(won_text, text_rect)
    space_text = font.render("Press SPACE to play again", True, (0, 255, 255))
    space_rect = space_text.get_rect(midtop=(self.WIDTH / 2, self.HEIGHT / 2 + self.GRID_SIZE))
    screen.blit(space_text, space_rect)
except pygame.error as e:
    print(f"Error loading tileset: {e}")
    return {}
class Actor(pygame.sprite.Sprite):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

GRID_WIDTH = 16
GRID_HEIGHT = 12
GRID_SIZE = 50
BACKGROUND_SEED = 123456
WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE
MAP = ["WWWWWWWWWWWWWWWW",
       "W              W",
       "W              W",
       "W  W           W",
       "W  WWWWWWWWWW  W",
       "W              W",
       "W              W",
       "W  WWWWWWWWWW  W",
       "W           W  W",
       "W              W",
       "W              D",
       "WWWWWWWWWWWWWWWW"]

# Inicializar Pygame y configurar la pantalla
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mapa sin personajes")

def screen_coords(x, y):
    return (x * GRID_SIZE, y * GRID_SIZE)

def draw_background():
    random.seed(BACKGROUND_SEED)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x % 2 == y % 2:
                screen.blit(pygame.image.load('images/floor1.png'), screen_coords(x, y))
            else:
                screen.blit(pygame.image.load('images/floor2.png'), screen_coords(x, y))
            n = random.randint(0, 99)
            if n < 5:
                screen.blit(pygame.image.load('images/crack1.png'), screen_coords(x, y))
            elif n < 10:
                screen.blit(pygame.image.load('images/crack2.png'), screen_coords(x, y))

def draw_scenery():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = MAP[y][x]
            if square == "W":
                screen.blit(pygame.image.load('images/wall.png'), screen_coords(x, y))
            elif square == "D":
                screen.blit(pygame.image.load('images/door.png'), screen_coords(x, y))

def draw_map():
    draw_background()  # Dibuja el fondo del mapa
    draw_scenery()     # Dibuja las paredes, puertas, y otros elementos estáticos

# Inicializar el juego (sin personajes)
draw_map()
pygame.display.flip()

# Guarda el mapa como una imagen
pygame.image.save(screen, "mapa_sin_personajes.png")

# Mantén la ventana abierta por unos segundos para ver el resultado
pygame.time.wait(3000)

pygame.quit()
