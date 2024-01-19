import pygame

pygame.init()
width, height = 1280, 720

size = width, height

screen_rect = (-100, -100, width + 200, height + 200)
vis_screen_rect = (0, 0, width, height)

# Объекты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()