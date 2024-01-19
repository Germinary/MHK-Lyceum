import pygame

sounds = {
	'jump': pygame.mixer.Sound('data/sounds/hero_jump.wav'),
	'dash': pygame.mixer.Sound('data/sounds/hero_dash.wav'),
	'land': pygame.mixer.Sound('data/sounds/hero_land.wav'),
	'kick': pygame.mixer.Sound('data/sounds/hero_kick.wav'),
	'ui': pygame.mixer.Sound('data/sounds/other_ui.wav'),
	'magic': pygame.mixer.Sound('data/sounds/hero_magic.wav'),
	'damage': pygame.mixer.Sound('data/sounds/hero_damage.wav'),
	'pv_attack': pygame.mixer.Sound('data/sounds/pv_attack_prepare.wav'),
	'teleport_out': pygame.mixer.Sound('data/sounds/other_teleport_out.wav'),
	'teleport_in': pygame.mixer.Sound('data/sounds/other_teleport_in.wav'),
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