import pygame
from const import *
from share import *
from utils import *
from audio import *
from particles import *
from other import *


class Character(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__(all_sprites)

	def on_ground(self):
		return self.rect.y + self.image.get_height() >= height - height * (1 / 6)

class Enemy(Character):
	def __init__(self):
		super().__init__()

	def damage(self, direction, hp):
		self.hp -= hp
		sounds['hit'].play()
		create_particles(
			'images/particles_enemy.bmp', 
			(self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2), 
			x_vel_change=direction
		)


class MainCharacter(Character):
	default_ = load_image('images/hero.bmp', colorkey=-1)
	walk = [load_image(f'images/hero_walk_{i}.bmp', colorkey=-1) for i in range(2)]
	attack_ = [load_image(f'images/hero_attack_{i}.bmp', colorkey=-1) for i in range(3)]

	data = MainCharacterData()

	def __init__(self):
		super().__init__()
		self.image = pygame.transform.flip(self.default_, True, False)
		self.rect = self.image.get_rect()
		self.rect.x = self.data.start_x
		self.rect.y = self.data.start_y

		self.speed = self.data.speed
		self.gravity = self.data.gravity

		self.jump_fase = 300

		self.attacks = 100

		self.cur_frame = 0
		self.frame = 0

		self.dash = 300

		self.is_moving = False
		self.direction = 1
		self.grounded = False
		self.magic_cooldown = 1000

		self.hp = 50
		self.immunity_frames = 1
		self.recline = 0
		self.heartbeat = False

	def damage(self, direction, hp):
		masks.sprites()[-1].kill()
		self.hp -= hp
		sounds['damage'].play()
		create_particles(
			'images/particles_hero.bmp', 
			(self.rect.x + self.image.get_width() // 2, self.rect.y + self.image.get_height() // 2), 
			x_vel_change=direction
		)
		self.recline = direction
		self.immunity_frames = 0

	def update(self):
		if self.recline != 0:
			if self.recline < -0.25 or self.recline > 0.25:
				self.dash = 300
			self.recline -= self.recline / FPS * 4
			if self.rect.colliderect(vis_screen_rect):
				self.rect = self.rect.move(self.recline / FPS * 1500, 0)
		if self.magic_cooldown < 1000:
			self.magic_cooldown += 300 / FPS
		if not self.grounded and self.on_ground() and self.jump_fase >= self.gravity:
			sounds['land'].play()
			self.grounded = True
		if not self.on_ground() and self.dash >= 300:
			self.rect = self.rect.move(0, self.gravity / FPS)
		if not self.is_moving:
			if self.direction == -1:
				self.image = self.default_
			else:
				mirrored = pygame.transform.flip(self.default_, True, False)
				self.image = mirrored

		if self.jump_fase < self.gravity:
			self.jump_fase += 200 / FPS * 4
			if self.dash >= 300:
				self.rect = self.rect.move(0, -250 / FPS * 3.5)
				
		if self.immunity_frames < 1:
			self.immunity_frames += 1 / FPS
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

		if not self.heartbeat and self.hp == 20:
			self.heartbeat = True
			pygame.mixer.music.set_volume(0.50)
			sounds['heartbeat'].play(-1)

		if self.hp == 10:
			pygame.mixer.music.fadeout(500) 

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
			self.rect.x += self.direction * self.speed / FPS


class PureVessel(Enemy):
	default_ = load_image('images/pv_0.bmp', colorkey=-1)
	attacks_ = [load_image(f'images/pv_{i}.bmp', colorkey=-1) for i in range(1, 4)]
	data = PureVesselData()
	def __init__(self):
		super().__init__()
		self.image = self.default_
		self.rect = self.image.get_rect()
		self.rect.x = self.data.start_x
		self.rect.y = height - self.image.get_height() - 100
		self.dash = 1000
		self.direction = -1
		self.speed = self.data.speed
		self.attacks = False
		self.last_attack = 0
		self.last_attack_type = 0
		self.delay = 0
		self.nails_buffer = []
		self.sound_buffer = None
		self.hp = self.data.hp
		self.immunity_frames = 1000
	def set_target(self, target):
		self.target = target

	def attack(self, type):
		self.attacks = True
		if type == 0:
			if self.direction == -1:
				self.rect.x = width - 300
				self.image = self.attacks_[0]
			else:
				self.rect.x = 50
				mirrored = pygame.transform.flip(self.attacks_[0], True, False)
				self.image = mirrored
			self.delay = 1000
			self.dash = 0
			self.sound_buffer = sounds['pv_attack']
		if type == 1:
			self.image = self.attacks_[1]
			self.rect.x = self.target.rect.x + self.target.image.get_width() // 2 - self.image.get_width() // 2
			self.rect.y = 25
			self.delay = 500
			self.sound_buffer = sounds['pv_attack']
		if type == 2:
			nails_coords = []
			if self.direction == -1:
				self.image = self.attacks_[2]
				self.rect.x = width - 300
				for i in range(-1, 9):
					x = self.rect.x - Nail.image.get_width() - 50
					y = (height - 280 * (height / 280)) + i * 125
					nails_coords.append((x, y))
			elif self.direction == 1:
				mirrored = pygame.transform.flip(self.attacks_[2], True, False)
				self.image = mirrored
				self.rect.x = 50
				for i in range(-1, 9):
					x = self.rect.x + self.image.get_width() + 50
					y = (height - 280 * (height / 280)) + i * 125
					nails_coords.append((x, y))
			self.delay = 1000
			self.nails_buffer = nails_coords


	def update(self):
		if self.rect.colliderect(self.target.rect) and self.target.attacks == 50:
			direction = 1 if self.rect.x + self.image.get_width() // 2 > self.target.rect.x + self.target.image.get_width() // 2 else -1
			self.damage(direction, 25)

		if self.delay > 0:
			self.delay -= 1000 / FPS
			return

		if self.delay <= 0:
			if not self.sound_buffer is None:
				self.sound_buffer.play()
				self.sound_buffer = None

		if self.dash < 1000:
			self.rect = self.rect.move(self.direction * self.speed / FPS, 0)
			self.dash += 2200 / FPS

		if self.dash >= 1000 and self.on_ground():
			self.attacks = False
			if self.direction == -1:
				self.image = self.default_
			else:
				mirrored = pygame.transform.flip(self.default_, True, False)
				self.image = mirrored

		if not self.on_ground():
			self.rect = self.rect.move(0, self.data.gravity / FPS)

		if self.last_attack < self.data.attacks_interval:
			try:
				self.last_attack += 1 * (self.data.hp / self.hp) ** 0.2 / FPS
			except ZeroDivisionError:
				pass

		if self.last_attack >= self.data.attacks_interval:
			sounds['teleport'].play()
			self.direction = -1 if randint(0, 1) == 0 else 1
			type = randint(0, 2)
			while type == self.last_attack_type:
				type = randint(0, 2)
			self.attack(type)
			self.last_attack_type = type
			self.last_attack = 0

		if len(self.nails_buffer) > 0 and self.delay <= 0:
			for i in self.nails_buffer:
				Nail(i, self.direction, self.target)
			self.nails_buffer.clear()

		if self.rect.colliderect(self.target.rect) and (self.attacks or not self.on_ground()) and self.target.immunity_frames >= 1:
			direction = -1 if self.rect.x + self.image.get_width() // 2 > self.target.rect.x + self.target.image.get_width() // 2 else 1
			self.target.damage(direction, 10)


class Xero(Enemy):
	default_ = load_image('images/xero.bmp', colorkey=-1)
	data = XeroData()
	def __init__(self):
		super().__init__()
		self.image = self.default_
		self.rect = self.image.get_rect()
		self.rect.x = self.data.start_x
		self.rect.y = self.data.start_y
		self.direction = -1
		self.speed_x = self.data.speed_x
		self.speed_y = self.data.speed_y
		self.nails_buffer = []
		self.sound_buffer = None
		self.hp = self.data.hp
		self.last_attack = 0
		self.direction_x = -1
		self.direction_y = -1

	def set_target(self, target):
		self.target = target

	def attack(self):
		sides = [self.rect.x - 50, self.rect.x + self.image.get_width() + 50]
		Bullet([choice(sides), 100], self.target)


	def update(self):
		if self.rect.colliderect(self.target.rect) and self.target.attacks == 50:
			direction = 1 if self.rect.x + self.image.get_width() // 2 > self.target.rect.x + self.target.image.get_width() // 2 else -1
			self.damage(direction, 25)

		if self.last_attack < self.data.attacks_interval:
			try:
				self.last_attack += 1 * (self.data.hp / self.hp) ** 0.1 / FPS
			except ZeroDivisionError:
				pass

		if self.last_attack >= self.data.attacks_interval:
			sounds['enemy_attack'].play()
			self.attack()
			self.last_attack = 0

		if self.rect.x <= 100:
			self.direction_x = 1
		elif self.rect.x + self.image.get_width() >= width - 100:
			self.direction_x = -1

		if self.rect.y <= height - 500:
			self.direction_y = 1
		elif self.rect.y >= height - 400:
			self.direction_y = -1

		x = self.direction_x * self.speed_x / FPS
		y = self.direction_y * self.speed_y / FPS
		self.rect = self.rect.move(x, y)


class SoulWarrior(Enemy):
	default_ = [
		load_image('images/sw_0.bmp', colorkey=-1),
		load_image('images/sw_1.bmp', colorkey=-1)
	]
	attack_ = [
		load_image('images/sw_3.bmp', colorkey=-1),
		load_image('images/sw_4.bmp', colorkey=-1),
		load_image('images/sw_5.bmp', colorkey=-1)
	]
	magic_ = load_image('images/sw_2.bmp', colorkey=-1)
	data = SoulWarriorData()
	def __init__(self):
		super().__init__()
		self.image = self.default_[0]
		self.rect = self.image.get_rect()
		self.rect.x = self.data.start_x
		self.rect.y = height - self.image.get_height() - 100
		self.direction = -1
		self.speed = self.data.speed
		self.attacks = 0
		self.last_attack = 0
		self.last_attack_type = 0
		self.delay = 0
		self.magic_buffer = []
		self.sound_buffer = None
		self.hp = self.data.hp
		self.attack_frame = 0
		self.frame = 0
		self.cur_frame = 0

	def set_target(self, target):
		self.target = target

	def attack(self, type):
		if type == 0:
			mirrored = pygame.transform.flip(self.attack_[0], True, False)
			self.image = self.attack_[0] if self.direction == -1 else mirrored
			self.delay = 350
			self.attacks = 1
			self.sound_buffer = sounds['enemy_kick']
		elif type == 1:
			mirrored = pygame.transform.flip(self.magic_, True, False)
			self.image = self.magic_ if self.direction == -1 else mirrored
			self.delay = 350
			sounds['enemy_attack'].play()
			if self.direction == -1:
				x = self.rect.x - 50
			else:
				x = self.rect.x + self.image.get_width() + 50
			y = self.rect.y + self.image.get_height() // 2
			self.magic_buffer.append((x, y))


	def update(self):
		self.direction = 1 if self.target.rect.x > self.rect.x else -1
		if self.rect.colliderect(self.target.rect) and self.target.attacks == 50:
			direction = 1 if self.rect.x + self.image.get_width() // 2 > self.target.rect.x + self.target.image.get_width() // 2 else -1
			self.damage(direction, 25)

		if self.delay > 0:
			self.delay -= 1000 / FPS
			return

		if self.delay <= 0:
			if not self.sound_buffer is None:
				self.sound_buffer.play()
				self.sound_buffer = None

		self.rect = self.rect.move(self.direction * self.speed / FPS, 0)

		if self.rect.colliderect(self.target.rect) and self.attacks == 0:
			self.attack(0)

		if self.rect.x + self.image.get_width() + 400 < self.target.rect.x or self.rect.x - 400 > self.target.rect.x and self.attacks == 0 and len(self.magic_buffer) == 0:
			self.attack(1)

		if self.attacks == 0:
			self.frame += 1
			if self.frame % 10 == 0:
				self.cur_frame += 1
				self.cur_frame -= len(self.default_) * (self.cur_frame // len(self.default_))
				if self.direction == -1:
					self.image = self.default_[self.cur_frame]
				else:
					mirrored = [pygame.transform.flip(i, True, False) for i in self.default_]
					self.image = mirrored[self.cur_frame]
		if self.attacks > 0:
			self.attack_frame += 12 / FPS
			self.attacks -= 1 / FPS
			mirrored = [pygame.transform.flip(i, True, False) for i in self.attack_]
			if self.attack_frame > 1:
				self.image = self.attack_[1] if self.direction == -1 else mirrored[1]
			if self.attack_frame > 2:
				self.image = self.attack_[2] if self.direction == -1 else mirrored[2]
			if self.attack_frame > 3:
				self.attacks = 0
				self.attack_frame = 0

		if len(self.magic_buffer) > 0:
			SoulWarriorMagic(self.magic_buffer[0], self.direction, self.target)
			self.magic_buffer.clear()
			self.delay = 1000

		if self.rect.colliderect(self.target.rect) and self.attacks > 0 and self.attacks < 0.9 and self.target.immunity_frames >= 1:
			direction = -1 if self.rect.x + self.image.get_width() // 2 > self.target.rect.x + self.target.image.get_width() // 2 else 1
			self.target.damage(direction, 10)