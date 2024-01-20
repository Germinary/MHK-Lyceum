import pygame
from const import *
from share import *
from utils import *
from particles import *

masks = pygame.sprite.Group()


class Mask(pygame.sprite.Sprite):
	default_ = load_image('images/mask.bmp', colorkey=-1)

	data = MaskData()

	def __init__(self, number):
		super().__init__(all_sprites, masks)
		self.image = self.default_
		self.rect = self.image.get_rect()
		self.rect.x = self.data.start_x + number * 40
		self.rect.y = self.data.y

	def update(self):
		pass


def create_masks():
	for i in range(5):
		Mask(i)


class Magic(pygame.sprite.Sprite):
	images = [load_image(f'images/magic_{i}.bmp', colorkey=-1) for i in range(3)]

	def __init__(self, direction, pos, target):
		super().__init__(all_sprites)
		if direction == 1:
			image = pygame.transform.flip(Magic.images[0], True, False)
			self.image = image
		else:
			self.image = Magic.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.frame = 0
		self.cur_frame = 0
		self.direction = direction
		self.v = 1200
		self.target = target

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
		try:
			if self.rect.colliderect(self.target.rect):
				self.target.damage(self.direction, 25)
				self.kill()
		except AttributeError:
			pass


class Nail(pygame.sprite.Sprite):
	image = load_image('images/nail.bmp', colorkey=-1)

	def __init__(self, coords, direction, target):
		super().__init__(all_sprites)
		self.direction = direction
		self.target = target
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

		if not self.rect.colliderect(screen_rect):
			self.kill()

		if self.rect.colliderect(self.target.rect) and self.target.immunity_frames >= 1:
			self.target.damage(self.direction, 10)
	

class Bullet(pygame.sprite.Sprite):
	images = [load_image(f'images/bullet_{i}.bmp', colorkey=-1) for i in range(2)]
	data = BulletData()

	def __init__(self, coords, target):
		super().__init__(all_sprites)
		self.target = target
		self.dx = self.target.rect.x - coords[0]
		self.dy = self.target.rect.y - coords[1]
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = coords[0]
		self.rect.y = coords[1]
		self.speed = self.data.speed
		self.frame = 0
		self.cur_frame = 0

	def update(self):
		dist = (self.dx ** 2 + self.dy ** 2) ** 0.5
		x = self.dx / FPS / (dist / self.speed)
		y = self.dy / FPS / (dist / self.speed)
		self.rect = self.rect.move(x, y)
		self.frame += 1
		if self.frame % 5 == 0:
			self.cur_frame += 1
			self.cur_frame -= self.cur_frame // len(self.images) * len(self.images)
			self.image = self.images[self.cur_frame]

		if not self.rect.colliderect(screen_rect):
			self.kill()

		if self.rect.colliderect(self.target.rect) and self.target.immunity_frames >= 1:
			direction = -1 if self.dx < 1 else 1
			self.target.damage(direction, 10)


class SoulWarriorMagic(pygame.sprite.Sprite):
	images = [load_image(f'images/bullet_{i}.bmp', colorkey=-1) for i in range(2)]
	data = SoulWarriorMagicData()

	def __init__(self, coords, direction, target):
		super().__init__(all_sprites)
		self.target = target
		self.direction = direction
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = coords[0]
		self.rect.y = coords[1]
		self.speed = self.data.speed
		self.frame = 0
		self.cur_frame = 0

	def update(self):
		self.rect = self.rect.move(self.direction * self.speed / FPS, 0)

		self.frame += 1
		if self.frame % 5 == 0:
			self.cur_frame += 1
			self.cur_frame -= self.cur_frame // len(self.images) * len(self.images)
			self.image = self.images[self.cur_frame]

		if not self.rect.colliderect(screen_rect):
			self.kill()

		if self.rect.colliderect(self.target.rect) and self.target.immunity_frames >= 1:
			self.target.damage(self.direction, 10)