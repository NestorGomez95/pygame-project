import pygame
from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4


WIDTH = 800
HEIGHT = 600
FPS = 60


pygame.init()
pygame.mixer.init()  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


levels = [
    (Level1, 'music/creepy_maze.wav'),
    (Level2, 'music/creepy_maze.wav'),
    (Level3, 'music/final_levels.mp3'),
    (Level4, 'music/final_levels.mp3')
]

current_level_index = 0
current_level, current_music = levels[current_level_index]


current_level = current_level()
pygame.mixer.music.load(current_music)
pygame.mixer.music.set_volume(0.3)  
pygame.mixer.music.play(loops=-1)  


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        current_level.handle_event(event)

    
    current_level.update()
    current_level.draw(screen)

    
    if current_level.game_over and current_level.knight_won:
        current_level_index += 1
        if current_level_index < len(levels):
            current_level, current_music = levels[current_level_index]
            current_level = current_level()

            
            pygame.mixer.music.stop()
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play(loops=-1)
        else:
            print("Game pass. ¡Congratulations!")
            running = False  

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
