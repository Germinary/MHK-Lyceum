import pygame
import sys
import os
from config import config
from time import sleep
from random import randint, choice
from collections_ import *
from characters import *
from utils import *
from audio import *
from particles import *
from other import *

# Коллекции
texts = []


def terminate():
	pygame.quit()
	sys.exit()


class UniqueSprite(pygame.sprite.Sprite):
	def __init__(self, image):
		super().__init__(all_sprites)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

class Text(pygame.sprite.Sprite):
	btn_image = load_image('images/button.bmp', colorkey=-1)

	def __init__(self, text, text_size, pos):
		super().__init__(all_sprites)

		font = pygame.font.Font(FONT_NAME, text_size)
		font_color = "white"

		self.image = font.render(text, True, font_color)
		self.rect = self.image.get_rect()
		self.rect.x = pos[0] + self.btn_image.get_width() // 2 - self.image.get_width() // 2
		self.rect.y = pos[1] + self.btn_image.get_height() // 2 - self.image.get_height() // 2

	def update(self, event):
		pass


class Button(pygame.sprite.Sprite):
	default_ = load_image('images/button.bmp', colorkey=-1)

	def __init__(self, text, go_to, text_size, pos):
		super().__init__(all_sprites)
		self.image = self.default_
		self.go_to = go_to
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]

		Text(text, text_size, pos)

	def update(self, event):
		if self.rect.collidepoint(*event.pos):
			if event.type == pygame.MOUSEBUTTONDOWN:
				sounds['ui'].play()
				sleep(0.5)
				level(self.go_to)


levels = [
	['level0'],
	['level1', SoulWarrior],
	['level2', Xero],
	['level3', PureVessel],
]


def level(level):
	pygame.mixer.music.fadeout(500)
	pygame.mixer.music.load(music[levels[level][0]])
	pygame.mixer.music.play(-1)

	all_sprites.empty()
	background_image = load_image(f'images/bg_level{level}.bmp')
	background_image = pygame.transform.scale(background_image, (width, height))
	background = UniqueSprite(background_image)

	if level != 0:
		enemy = levels[level][1]()
		player = MainCharacter()
		enemy.set_target(player)
		enemy.direction = -1
	else:
		player = MainCharacter()

	running = True
	masks = create_masks()

	while running:
		all_sprites.draw(screen)
		all_sprites.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == config['jump'] and player.on_ground():
					sounds['jump'].play()
					player.grounded = False
					player.jump_fase = 0
				if event.key == config['hit'] and player.attacks >= 150:
					player.attacks = 0
					sounds['sword'][randint(0, 4)].play()
				if event.key == config['dash'] and player.dash >= 800:
					sounds['dash'].play()
					player.dash = 0
				if event.key == config['magic'] and player.magic_cooldown >= 1000:
					sounds['magic'].play()
					player.magic_cooldown = 0
					if level != 0:
						Magic(player.direction, [player.rect.x, player.rect.y], enemy)
					else:
						Magic(player.direction, [player.rect.x, player.rect.y], None)
			else:
				pass
				#print(event)
		if player.hp <= 0:
			print('You lose!', player.hp, '/', enemy.hp)
			sys.exit(0)
		if level != 0 and enemy.hp <= 0:
			print('You win!', player.hp, '/', enemy.hp)
			sys.exit(0)
		keys = pygame.key.get_pressed()

		if keys[config['left']]:
			player.direction = -1
			player.go()
		elif keys[config['right']]:
			player.direction = 1
			player.go()

		else:
			player.is_moving = False

		clock.tick(FPS)
		pygame.display.flip()

	terminate()

def menu():
	pygame.mixer.music.fadeout(3000)
	background_image = load_image('images/bg_menu.bmp')
	background = UniqueSprite(background_image)

	x = width // 2 - Text.btn_image.get_width() // 2
	y = height // 2 - Text.btn_image.get_height() // 2 - 130
	Text("HOLLOW KNIGHT MINI", 30, [x, y])

	buttons = [
		['Тренировочная комната', 0],
		['Уровень 1', 1],
		['Уровень 2', 2],
		['Уровень 3', 3]
	]

	for i, button in enumerate(buttons):
		x = width // 2 - Button.default_.get_width() // 2
		y = height // 2 - Button.default_.get_height() // 2 + i * 80 - 40
		text_size = 15
		Button(*button, text_size, [x, y])


	running = True

	pygame.mixer.music.load(music['menu'])
	pygame.mixer.music.play(-1)

	while running:
		all_sprites.draw(screen)

		for text in texts:
			screen.blit(text[0], (text[1], text[2]))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				all_sprites.update(event)

		clock.tick(FPS)
		pygame.display.flip()

	terminate()



if __name__ == '__main__':
	menu()