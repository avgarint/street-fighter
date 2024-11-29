import pygame
from player import *

FPS = 60
WINDOW_SIZE = (1920, 1080)

should_quit = False

pygame.init()
pygame.display.set_caption('Street Fighter')

clock = pygame.time.Clock()
window = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.SysFont('Comic Sans MS', 150)
background = pygame.image.load('./art/background.jpg')
player_group = pygame.sprite.Group()

player_0 = player(window, 100, 10, 10, 770, player.DIRECTION_LEFT, 10, 30, 0)
player_1 = player(window, 100, 10, 1700, 770, player.DIRECTION_LEFT, 10, 30, 1)

player_group.add(player_0)
player_group.add(player_1)

music = pygame.mixer.Sound('./art/music.mp3')
music.set_volume(0.1)
music.play(-1)

while not should_quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_quit = True

    window.blit(background, (0, 0))

    if player_0.health == 0 or player_1.health == 0:
        if player_0.health == 0:
            text_surface = font.render('Player 1 won!', False, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
            window.blit(text_surface, text_rect)
        else:
            text_surface = font.render('Player 2 won!', False, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
            window.blit(text_surface, text_rect)

    player_0.update_gui()
    player_1.update_gui()

    player_0.update_inputs(player_1)
    player_1.update_inputs(player_0)

    player_group.draw(window)
    player_group.update()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
