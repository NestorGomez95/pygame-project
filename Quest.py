import pygame
import random

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
GUARD_MOVE_INTERVAL = 0.5  # Intervalo de movimiento en segundos
PLAYER_MOVE_INTERVAL = 0.1
BACKGROUND_SEED = 123456
WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE
MAP = ["WWWWWWWWWWWWWWWW",
       "W              W",
       "W              W",
       "W  W  KG       W",
       "W  WWWWWWWWWW  W",
       "W              W",
       "W      P       W",
       "W  WWWWWWWWWW  W",
       "W      GK   W  W",
       "W              W",
       "W              D",
       "WWWWWWWWWWWWWWWW"]

# Inicializar Pygame y configurar la pantalla
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego con Pygame")

# Cargar imágenes
player_image = pygame.image.load('images/player.png')
guard_image = pygame.image.load('images/guard.png')
key_image = pygame.image.load('images/key.png')

def screen_coords(x, y):
    return (x * GRID_SIZE, y * GRID_SIZE)

def grid_coords(actor):
    return (round(actor.rect.x / GRID_SIZE), round(actor.rect.y / GRID_SIZE))

# Definir rutas para los guardias
guard_routes = [
    [(5, 3), (5, 4), (5, 5), (4, 5), (3, 5)],  # Ruta del primer guardia
    [(8, 7), (8, 8), (8, 9), (7, 9)],  # Ruta del segundo guardia
]

def setup_game():
    global game_over, player_won, player, keys_to_collect, guards, last_guard_move_time
    game_over = False
    player_won = False
    player = Actor(player_image)
    keys_to_collect = []
    guards = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = MAP[y][x]
            if square == "P":
                player.rect.topleft = screen_coords(x, y)
            elif square == "K":
                key = Actor(key_image)
                key.rect.topleft = screen_coords(x, y)
                keys_to_collect.append(key)
            elif square == "G":
                guard = Actor(guard_image)
                guard.rect.topleft = screen_coords(x, y)
                guards.append(guard)

    # Asignar rutas a los guardias
    for i, guard in enumerate(guards):
        guard.route = guard_routes[i]
        guard.route_index = 0
    last_guard_move_time = pygame.time.get_ticks()

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

def draw_actors():
    player.draw(screen)
    for key in keys_to_collect:
        key.draw(screen)
    for guard in guards:
        guard.draw(screen)

def draw_game_over():
    font = pygame.font.Font(None, GRID_SIZE)
    screen_middle = (WIDTH / 2, HEIGHT / 2)
    game_over_text = font.render("GAME OVER", True, (0, 255, 255))
    text_rect = game_over_text.get_rect(midbottom=screen_middle)
    screen.blit(game_over_text, text_rect)

    if player_won:
        won_text = font.render("You won!", True, (0, 255, 0))
    else:
        won_text = font.render("You lost!", True, (255, 0, 0))
    text_rect = won_text.get_rect(midtop=screen_middle)
    screen.blit(won_text, text_rect)
    space_text = font.render("Press SPACE to play again", True, (0, 255, 255))
    space_rect = space_text.get_rect(midtop=(WIDTH / 2, HEIGHT / 2 + GRID_SIZE))
    screen.blit(space_text, space_rect)

def draw():
    draw_background()
    draw_scenery()
    draw_actors()
    if game_over:
        draw_game_over()

def on_key_up(key):
    if key == pygame.K_SPACE and game_over:
        setup_game()

def on_key_down(key):
    if key == pygame.K_LEFT:
        move_player(-1, 0)
    elif key == pygame.K_UP:
        move_player(0, -1)
    elif key == pygame.K_RIGHT:
        move_player(1, 0)
    elif key == pygame.K_DOWN:
        move_player(0, 1)

def move_player(dx, dy):
    global game_over, player_won
    if game_over:
        return
    (x, y) = grid_coords(player)
    x += dx
    y += dy
    square = MAP[y][x]
    if square == "W":
        return
    elif square == "D":
        if len(keys_to_collect) > 0:
            return
        else:
            game_over = True
            player_won = True
    for key in keys_to_collect:
        (key_x, key_y) = grid_coords(key)
        if x == key_x and y == key_y:
            keys_to_collect.remove(key)
            break
    player.rect.topleft = screen_coords(x, y)
    # Verificar colisión con guardias
    for guard in guards:
        if player.rect.colliderect(guard.rect):
            game_over = True
            player_won = False

def move_guard(guard):
    global game_over
    if game_over:
        return
    
    # Obtener la siguiente posición en la ruta del guardia
    next_index = (guard.route_index + 1) % len(guard.route)
    next_x, next_y = guard.route[next_index]
    
    # Verificar colisiones con muros
    if MAP[next_y][next_x] == "W":
        guard.route_index = next_index
        return
    
    # Mover el guardia a la siguiente posición
    guard.rect.topleft = screen_coords(next_x, next_y)
    guard.route_index = next_index
    
    # Verificar colisión con el jugador
    if guard.rect.colliderect(player.rect):
        game_over = True
        player_won = False

def move_guards():
    global last_guard_move_time
    current_time = pygame.time.get_ticks()
    if (current_time - last_guard_move_time) / 1000 > GUARD_MOVE_INTERVAL:
        for guard in guards:
            move_guard(guard)
        last_guard_move_time = current_time

setup_game()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            on_key_down(event.key)
        elif event.type == pygame.KEYUP:
            on_key_up(event.key)

    draw()
    move_guards()  # Mover guardias en cada frame
    pygame.display.flip()
    clock.tick(60)  # Limita a 60 FPS

pygame.quit()