import pygame
from random import randint, choice
from share import *
from utils import *
from const import *


class Particle(pygame.sprite.Sprite): 
	def __init__(self, image, pos, dx, dy, x_vel_change):
		super().__init__(all_sprites)
		self.image = [load_image(image, colorkey=-1)]
		for scale in (5, 10, 20):
			self.image.append(pygame.transform.scale(self.image[0], (scale, scale)))
		self.image = choice(self.image)
		self.rect = self.image.get_rect()

		self.velocity = [dx, dy]
		self.rect.x, self.rect.y = pos

		self.gravity = 0.4
		self.x_vel_change = x_vel_change

	def update(self):
		self.velocity[1] += self.gravity
		self.velocity[0] += self.x_vel_change
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]
		if not self.rect.colliderect(screen_rect):
			self.kill()


def create_particles(image, position, x_vel_change=0):
	particle_count = 30
	numbers = range(-5, 6)
	for i in range(particle_count):
		Particle(image, position, choice(numbers), choice(numbers), x_vel_change)