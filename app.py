import pygame
import sys
import os
from config import config
from time import sleep
from random import randint

pygame.init()
size = width, height = 1000, 600

# Объекты
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Коллекции
texts = []
sounds = {
	'jump': pygame.mixer.Sound('data/sounds/hero_jump.wav'),
	'dash': pygame.mixer.Sound('data/sounds/hero_dash.wav'),
	'land': pygame.mixer.Sound('data/sounds/hero_land.wav'),
	'kick': pygame.mixer.Sound('data/sounds/hero_kick.wav'),
	'ui': pygame.mixer.Sound('data/sounds/other_ui.wav'),
	'magic': pygame.mixer.Sound('data/sounds/hero_magic.wav')
}
music = {
	'menu': 'data/music/menu.mp3',
	'level0': 'data/music/level0.mp3',
	'level1': 'data/music/level1.mp3',
	'level2': 'data/music/level2.mp3', 
	'level3': 'data/music/level3.mp3',
}

# Константы
FPS = 60
FONT_NAME = 'data/share/font.ttf'

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)

	if not os.path.isfile(fullname):
		print(f"Файл с изображением '{fullname}' не найден")
		sys.exit()
	image = pygame.image.load(fullname)

	if colorkey is not None:
		image = image.convert()
		if colorkey == -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey)
	else:
		image = image.convert_alpha()

	return image


def terminate():
	pygame.quit()
	sys.exit()


class UniqueSprite(pygame.sprite.Sprite):
	def __init__(self, *data):
		super().__init__(*data[:-1])
		self.image = data[-1]
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0


class Button(pygame.sprite.Sprite):
	def __init__(self, *data):
		super().__init__(*data[:-1])
		self.image = data[-1][0]
		self.go_to = data[-1][1]
		self.rect = self.image.get_rect()
		self.rect.x = data[-1][2][0]
		self.rect.y = data[-1][2][1]

	def update(self, event):
		if self.rect.collidepoint(*event.pos):
			if event.type == pygame.MOUSEBUTTONDOWN:
				sounds['ui'].play()
				sleep(0.5)
				level(self.go_to)


class Magic(pygame.sprite.Sprite):
	images = [load_image(f'magic/{i}.bmp', colorkey=-1) for i in range(3)]
	def __init__(self, *data):
		super().__init__(*data[:-1])
		if data[-1][0] == 1:
			image = pygame.transform.flip(Magic.images[0], True, False)
			self.image = image
		else:
			self.image = Magic.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = data[-1][1][0]
		self.rect.y = data[-1][1][1]
		self.frame = 0
		self.cur_frame = 0
		self.direction = data[-1][0]
		self.v = 1200
	def update(self):
		self.frame += 1
		if self.frame % 4 == 0:
			if self.direction == -1:
				self.image = self.images[self.cur_frame]
			else:
				mirrored = [pygame.transform.flip(i, True, False) for i in self.images]
				self.image = mirrored[self.cur_frame]
			lim = len(self.images)
			self.cur_frame += 1
			self.cur_frame -= self.cur_frame // lim * lim
		self.rect = self.rect.move(self.direction * self.v / FPS, 0)


class MainCharacter(pygame.sprite.Sprite):
	image = load_image('character/0.bmp', colorkey=-1)
	walk = [load_image(f'character/walk/{i}.bmp', colorkey=-1) for i in range(2)]
	attack_ = [load_image(f'character/attack/{i}.bmp', colorkey=-1) for i in range(3)]

	def __init__(self, *group):
		super().__init__(*group)
		self.image = pygame.transform.flip(MainCharacter.image, True, False)
		self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = height - self.image.get_height() - 100
		print(self.rect.y)

		self.v = 300
		self.gravity = 300

		self.jump_fase = 300

		self.attacks = 100

		self.cur_frame = 0
		self.frame = 0

		self.dash = 300

		self.is_moving = False
		self.direction = 1
		self.grounded = False
		self.magic_cooldown = 1000

	def update(self):
		if self.magic_cooldown < 1000:
			self.magic_cooldown += 300 / FPS
		if not self.grounded and self.on_ground() and self.jump_fase >= self.gravity:
			sounds['land'].play()
			self.grounded = True
		if not self.on_ground() and self.dash >= 300:
			self.rect = self.rect.move(0, self.gravity / FPS)
		if not self.is_moving:
			if self.direction == -1:
				self.image = MainCharacter.image
			else:
				mirrored = pygame.transform.flip(MainCharacter.image, True, False)
				self.image = mirrored
		if self.jump_fase < self.gravity:
			self.jump_fase += 200 / FPS * 4
			if self.dash >= 300:
				self.rect = self.rect.move(0, -250 / FPS * 3.5)
		if self.attacks < 100:
			frame = int(self.attacks // 40)
			if self.direction == 1:
				mirrored = [pygame.transform.flip(i, True, False) for i in self.attack_]
				self.image = mirrored[frame]
			else:
				self.image = self.attack_[frame]
			self.attacks += 300 / FPS
		if self.attacks < 150:
			self.attacks += 300 / FPS
		if self.dash < 300:
			self.jump_fase = 300
			if self.direction == -1:
				self.image = self.walk[0]
			else:
				mirrored = pygame.transform.flip(self.walk[0], True, False)
				self.image = mirrored
			if not self.check_walls():
				self.rect = self.rect.move(1000 / FPS * self.direction, 0)
			self.dash += 900 / FPS
		if self.dash < 800:
			self.dash += 900 / FPS

	def on_ground(self):
		return not (self.rect.y + self.image.get_height() < 500)

	def check_walls(self):
		if self.direction == -1 and self.rect.x <= 0:
			return True
		elif self.direction == 1 and self.rect.x >= width - self.image.get_size()[0]:
			return True

	def go(self):
		if self.check_walls():
			pass
		else:
			self.is_moving = True

			self.frame += 1
			if self.frame % 10 == 0:
				if self.direction == -1:
					self.image = self.walk[self.cur_frame]
				else:
					mirrored = [pygame.transform.flip(i, True, False) for i in self.walk]
					self.image = mirrored[self.cur_frame]
				lim = len(self.walk)
				self.cur_frame += 1
				self.cur_frame -= self.cur_frame // lim * lim
			self.rect.x += self.direction * self.v / FPS


class Nail(pygame.sprite.Sprite):
	image = load_image('other/nail/0.bmp', colorkey=-1)
	def __init__(self, coords, direction):
		super().__init__(all_sprites)
		self.direction = direction
		if self.direction == -1:
			self.image = Nail.image
		else:
			mirrored = pygame.transform.flip(Nail.image, True, False)
			self.image = mirrored
		self.rect = self.image.get_rect()
		self.rect.x = coords[0]
		self.rect.y = coords[1]
		self.v = 1000

	def update(self):
		self.rect.x += self.direction * self.v / FPS

		if self.rect.x < -100 or self.rect.x > width:
			self.kill()
		if self.rect.y > height + 100 or self.rect.y < -100:
			self.kill()


class PureVessel(pygame.sprite.Sprite):
	image = load_image('bosses/pure_vessel/0.bmp', colorkey=-1)
	attacks_ = [
		load_image('bosses/pure_vessel/1.bmp', colorkey=-1),
		load_image('bosses/pure_vessel/2.bmp', colorkey=-1),
		load_image('bosses/pure_vessel/3.bmp', colorkey=-1)
	]
	def __init__(self, *group):
		super().__init__(*group)
		self.image = PureVessel.image
		self.rect = self.image.get_rect()
		self.rect.x = 700
		self.rect.y = height - self.image.get_height() - 100
		self.dash = 1000
		self.direction = -1
		self.v = 1500
		self.attacks = False
		self.last_attack = 0
		self.delay = 0
		self.nails_buffer = []
	
	def set_target(self, target):
		self.target = target

	def attack(self, type):
		self.attacks = True
		if type == 0:
			if self.direction == -1:
				self.rect.x = 700
				self.image = self.attacks_[0]
			else:
				self.rect.x = 50
				mirrored = pygame.transform.flip(self.attacks_[0], True, False)
				self.image = mirrored
			self.delay = 500
			self.dash = 0
		if type == 1:
			self.image = self.attacks_[1]
			self.rect.x = self.target.rect.x + self.target.image.get_width() // 2 - self.image.get_width() // 2
			self.rect.y = 25
			self.delay = 500
		if type == 2:
			nails_coords = []
			if self.direction == -1:
				self.image = self.attacks_[2]
				self.rect.x = 700
				for i in range(-1, 9):
					x = self.rect.x - Nail.image.get_width() - 50
					y = self.rect.y + i * 100
					nails_coords.append((x, y))
			elif self.direction == 1:
				mirrored = pygame.transform.flip(self.attacks_[2], True, False)
				self.image = mirrored
				self.rect.x = 50
				for i in range(-1, 9):
					x = self.rect.x + self.image.get_width() + 50
					y = self.rect.y + i * 100
					nails_coords.append((x, y))
			self.delay = 1000
			self.nails_buffer = nails_coords


	def on_ground(self):
		return not (self.rect.y + self.image.get_height() < 500)

	def update(self):
		if self.delay > 0:
			self.delay -= 1000 / FPS
			return

		if self.dash < 1000:
			self.rect = self.rect.move(self.direction * self.v / FPS, 0)
			self.dash += 2200 / FPS
		if self.dash >= 1000 and self.on_ground():
			self.attacks = False
			if self.direction == -1:
				self.image = PureVessel.image
			else:
				mirrored = pygame.transform.flip(PureVessel.image, True, False)
				self.image = mirrored
		if not self.on_ground():
			self.rect = self.rect.move(0, 1000 / FPS)
		if self.last_attack < 1000:
			self.last_attack += 750 / FPS
		if self.last_attack >= 1000:
			self.direction = -1 if randint(0, 1) == 0 else 1
			self.attack(randint(0, 2))
			self.last_attack = 0
		if len(self.nails_buffer) > 0 and self.delay <= 0:
			for i in self.nails_buffer:
				Nail(i, self.direction)
			self.nails_buffer.clear()


levels = [
	['level0', PureVessel],
	['level1'],
	['level2'],
	['level3', PureVessel],
]

def level(level):
	pygame.mixer.music.fadeout(500)
	pygame.mixer.music.load(music[levels[level][0]])
	pygame.mixer.music.play(-1)

	all_sprites.empty()
	background_image = load_image(f'levels/{level}/background.bmp')
	background = UniqueSprite(all_sprites, background_image)

	enemy = levels[level][1](all_sprites)
	player = MainCharacter(all_sprites)
	enemy.set_target(player)

	running = True
	enemy.direction = -1

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
					sounds['kick'].play()
				if event.key == config['dash'] and player.dash >= 800:
					sounds['dash'].play()
					player.dash = 0
				if event.key == config['magic'] and player.magic_cooldown >= 1000:
					data = [player.direction, [player.rect.x, player.rect.y]]
					sounds['magic'].play()
					player.magic_cooldown = 0
					Magic(all_sprites, data)
			else:
				pass
				#print(event)
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
	background_image = load_image('menu/background.bmp')
	background = UniqueSprite(all_sprites, background_image)

	font = pygame.font.Font(FONT_NAME, 30)
	font_color = "white"

	text = font.render("HOLLOW KNIGHT MINI", True, font_color)
	text_x = width // 2 - text.get_width() // 2
	text_y = height // 2 - text.get_height() // 2 - 130
	texts.append([text, text_x, text_y])


	button_image = load_image('menu/button.bmp', colorkey=-1)

	buttons = [
		['Тестовая комната', 0],
		['Уровень 1', 1],
		['Уровень 2', 2],
		['Уровень 3', 3]
	]

	font = pygame.font.Font(FONT_NAME, 15)
	font_color = "white"

	for i, button in enumerate(buttons):
		x = width // 2 - button_image.get_width() // 2
		y = height // 2 - button_image.get_height() // 2 + i * 80 - 40
		btn = Button(all_sprites, [button_image, button[1], [x, y]])

		text = font.render(button[0], True, font_color)
		text_x = width // 2 - text.get_width() // 2
		text_y = height // 2 - text.get_height() // 2 + i * 80 - 40
		texts.append([text, text_x, text_y])


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