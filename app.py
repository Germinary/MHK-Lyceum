import pygame
import sys
import os
from config import config
from random import randint, choice
from share import *
from characters import *
from utils import *
from audio import *
from particles import *
from other import *

LEVELS = [
	['Тренировочная комната', '', 'level0'],
	['Воин душ', 'Тревожный бог Святилища', 'level1', SoulWarrior],
	['Ксеро', 'Рожденный в грезах бог верности и предательства', 'level2', Xero],
	['Чистый сосуд', 'Могучий бог небытия', 'level3', PureVessel],
]


class Background(pygame.sprite.Sprite):
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
				game.go_to(self.go_to)


class Game():
	def __init__(self):
		pygame.display.set_caption('Hollow Knight Mini')
		icon = load_image('images/logo.bmp', colorkey=-1)
		pygame.display.set_icon(icon)

	def level(self, level):
		all_sprites.empty()
		background_image = load_image(f'images/bg_level{level}.bmp')
		background_image = pygame.transform.scale(background_image, (width, height))
		background = Background(background_image)

		if level != 0:
			enemy = LEVELS[level][3]()
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
						player.jump_power = 0
					if event.key == config['hit'] and player.attacks >= 150:
						player.attacks = 0
						sounds['sword'][randint(0, 4)].play()
					if event.key == config['dash'] and player.dash_power >= 800:
						sounds['dash'].play()
						player.dash_power = 0
					if event.key == config['magic'] and player.magic_cooldown >= 1:
						sounds['magic'].play()
						player.magic_cooldown = 0
						if level != 0:
							Magic(player.direction, [player.rect.x, player.rect.y], enemy)
						else:
							Magic(player.direction, [player.rect.x, player.rect.y], None)
					if event.key == config['exit']:
						pygame.mixer.stop()
						self.menu()
			if player.hp <= 0:
				self.end_battle(False)
			if level != 0 and enemy.hp <= 0:
				self.end_battle(True)
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

		self.terminate()

	def end_battle(self, result):
		all_sprites.empty()

		x = width // 2 - Text.btn_image.get_width() // 2
		y = height // 2 - Text.btn_image.get_height() // 2
		Text('Вы победили' if result else 'Вы проиграли', 30, [x, y])

		running = True

		pygame.mixer.stop()
		pygame.mixer.music.stop()
		pygame.mixer.music.set_volume(100)

		time = 2

		while running:
			screen.fill("black")
			all_sprites.draw(screen)
			time -= 1 / FPS

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			if time <= 0:
				self.menu()

			clock.tick(FPS)
			pygame.display.flip()

		self.terminate()

	def go_to(self, level):
		title, subtitle = LEVELS[level][:2]
		all_sprites.empty()

		x = width // 2 - Text.btn_image.get_width() // 2
		y = height // 2 - Text.btn_image.get_height() // 2 - 50
		Text(title, 30, [x, y])

		x = width // 2 - Text.btn_image.get_width() // 2
		y = height // 2 - Text.btn_image.get_height() // 2 + 50
		Text(subtitle, 20, [x, y])

		running = True

		pygame.mixer.music.fadeout(500)
		pygame.mixer.music.load(music[LEVELS[level][2]])
		pygame.mixer.music.play(-1)

		time = 2

		while running:
			screen.fill("black")
			all_sprites.draw(screen)
			time -= 1 / FPS

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			if time <= 0:
				self.level(level)

			clock.tick(FPS)
			pygame.display.flip()

		self.terminate()

	def menu(self):
		all_sprites.empty()
		pygame.mixer.music.stop()
		background_image = load_image('images/bg_menu.bmp')
		background = Background(background_image)

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

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					all_sprites.update(event)
				if event.type == pygame.KEYDOWN and event.key == config['exit']:
					self.terminate()

			clock.tick(FPS)
			pygame.display.flip()

		self.terminate()

	def terminate(self):
		pygame.quit()
		sys.exit()


game = Game()

if __name__ == '__main__':
	game.menu()