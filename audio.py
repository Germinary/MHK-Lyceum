import pygame

sounds = {
	'jump': pygame.mixer.Sound('data/sounds/hero_jump.wav'),
	'dash': pygame.mixer.Sound('data/sounds/hero_dash.wav'),
	'land': pygame.mixer.Sound('data/sounds/hero_land.wav'),
	'enemy_kick': pygame.mixer.Sound('data/sounds/enemy_kick.wav'),
	'ui': pygame.mixer.Sound('data/sounds/other_ui.wav'),
	'magic': pygame.mixer.Sound('data/sounds/hero_magic.wav'),
	'damage': pygame.mixer.Sound('data/sounds/hero_damage.wav'),
	'pv_attack': pygame.mixer.Sound('data/sounds/pv_attack_prepare.wav'),
	'enemy_attack': pygame.mixer.Sound('data/sounds/enemy_attack.wav'),
	'teleport': pygame.mixer.Sound('data/sounds/other_teleport.wav'),
	'sword': [pygame.mixer.Sound(f'data/sounds/sword_{i}.wav') for i in range(1, 6)],
	'hit': pygame.mixer.Sound(f'data/sounds/sword_hit.wav'),
	'heartbeat': pygame.mixer.Sound(f'data/sounds/hero_heartbeat.wav')
}

music = {
	'menu': 'data/music/menu.mp3',
	'level0': 'data/music/level0.mp3',
	'level1': 'data/music/level1.mp3',
	'level2': 'data/music/level2.mp3', 
	'level3': 'data/music/level3.mp3',
}