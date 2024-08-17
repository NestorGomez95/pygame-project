import pygame
import csv

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Level1:
    def __init__(self):
        self.GRID_SIZE = 50
        self.WIDTH, self.HEIGHT = 800, 600  # Ajustar según el tamaño de tu mapa
        self.GUARD_MOVE_INTERVAL = 500  # Tiempo en milisegundos entre movimientos de los guardias

        # Cargar el mapa desde un archivo CSV
        self.map_data = self.load_csv_map('levels/level1.csv')
        
        # Cargar imágenes del mapa
        self.tile_images = self.load_tileset()

        # Cargar imágenes del knight, los guardias y las llaves
        self.knight_image = pygame.image.load('images/player.png')
        self.guard_image = pygame.image.load('images/guard.png')
        self.key_image = pygame.image.load('images/key.png')

        # Configurar personajes y objetos
        self.setup_game()

        # Tiempo para mover guardias
        self.last_guard_move_time = pygame.time.get_ticks()

    def load_tileset(self):
        # Cargar las imágenes de los tiles del mapa
        tileset = {
            0: pygame.image.load('images/floor1.png'),
            1: pygame.image.load('images/floor2.png'),
            2: pygame.image.load('images/door.png'),
            3: pygame.image.load('images/wall.png'),
            # Añadir más tiles según sea necesario
        }
        return tileset

    def load_csv_map(self, filename):
        # Cargar el archivo CSV y convertirlo a una lista de listas de enteros
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            map_data = [list(map(int, row)) for row in reader]
        return map_data

    def setup_game(self):
        # Crear y posicionar los personajes y objetos del nivel
        self.knight = Actor(self.knight_image, 6 * self.GRID_SIZE, 6 * self.GRID_SIZE)
        self.keys_to_collect = [Actor(self.key_image, 5 * self.GRID_SIZE, 3 * self.GRID_SIZE)]
        
        # Definir las rutas de los guardias (movimiento circular)
        self.guards = [
            {'actor': Actor(self.guard_image, 3 * self.GRID_SIZE, 5 * self.GRID_SIZE),
             'route': [(3, 5), (4, 5), (4, 6), (3, 6)], 'route_index': 0},
            {'actor': Actor(self.guard_image, 7 * self.GRID_SIZE, 9 * self.GRID_SIZE),
             'route': [(7, 9), (8, 9), (8, 10), (7, 10)], 'route_index': 0}
        ]
        
        self.game_over = False
        self.knight_won = False

    def draw_map(self, screen):
        # Dibujar el mapa en la pantalla
        for y, row in enumerate(self.map_data):
            for x, tile_id in enumerate(row):
                tile_image = self.tile_images.get(tile_id)
                if tile_image:
                    screen.blit(tile_image, (x * self.GRID_SIZE, y * self.GRID_SIZE))

    def draw_actors(self, screen):
        # Dibujar el knight, las llaves y los guardias
        self.knight.draw(screen)
        for key in self.keys_to_collect:
            key.draw(screen)
        for guard in self.guards:
            guard['actor'].draw(screen)

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 74)
        message = "You won!" if self.knight_won else "You lost!"
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        screen.blit(text, text_rect)

    def draw(self, screen):
        # Dibujar el mapa y los actores
        self.draw_map(screen)
        self.draw_actors(screen)
        
        # Dibujar el mensaje de game over si el juego ha terminado
        if self.game_over:
            self.draw_game_over(screen)

    def handle_event(self, event):
        if not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_knight(-1, 0)
            elif event.key == pygame.K_UP:
                self.move_knight(0, -1)
            elif event.key == pygame.K_RIGHT:
                self.move_knight(1, 0)
            elif event.key == pygame.K_DOWN:
                self.move_knight(0, 1)

    def can_move_to(self, x, y):
        # Obtener la casilla del mapa en la posición del knight
        tile_id = self.map_data[y][x]
        
        # El knight no puede moverse a una pared (tile_id 3)
        if tile_id == 3:
            return False
        # El knight solo puede moverse a la puerta (tile_id 2) si ha recogido todas las llaves
        if tile_id == 2 and len(self.keys_to_collect) > 0:
            return False
        return True

    def move_knight(self, dx, dy):
        if self.game_over:
            return
        
        # Calcular las nuevas coordenadas del knight en la cuadrícula
        new_x = self.knight.rect.x // self.GRID_SIZE + dx
        new_y = self.knight.rect.y // self.GRID_SIZE + dy
        
        # Verificar si el knight puede moverse a la nueva posición
        if self.can_move_to(new_x, new_y):
            self.knight.rect.move_ip(dx * self.GRID_SIZE, dy * self.GRID_SIZE)
        
        # Verificar colisiones con llaves
        for key in self.keys_to_collect[:]:
            if self.knight.rect.colliderect(key.rect):
                self.keys_to_collect.remove(key)

        # Verificar colisiones con guardias
        self.check_guard_collision()

        # Verificar si el nivel ha sido completado
        if self.is_completed():
            self.game_over = True
            self.knight_won = True

    def move_guard(self, guard):
        # Mover el guardia a la siguiente posición en su ruta
        next_index = (guard['route_index'] + 1) % len(guard['route'])
        next_x, next_y = guard['route'][next_index]
        guard['actor'].rect.topleft = (next_x * self.GRID_SIZE, next_y * self.GRID_SIZE)
        guard['route_index'] = next_index
        
        # Verificar colisiones con el knight
        self.check_guard_collision()

    def move_guards(self):
        # Mover guardias en intervalos de tiempo
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_guard_move_time) > self.GUARD_MOVE_INTERVAL:
            for guard in self.guards:
                self.move_guard(guard)
            self.last_guard_move_time = current_time

    def check_guard_collision(self):
        for guard in self.guards:
            if self.knight.rect.colliderect(guard['actor'].rect):
                self.game_over = True
                self.knight_won = False

    def update(self):
        if not self.game_over:
            self.move_guards()  # Mover los guardias en cada actualización

    def is_completed(self):
        # Determinar si el nivel ha sido completado (por ejemplo, si se recogieron todas las llaves y el knight llegó a la puerta)
        knight_x = self.knight.rect.x // self.GRID_SIZE
        knight_y = self.knight.rect.y // self.GRID_SIZE
        # Si el knight está en la puerta (tile_id 2) y ha recogido todas las llaves, el nivel está completado
        return self.map_data[knight_y][knight_x] == 2 and len(self.keys_to_collect) == 0 and not self.game_over
