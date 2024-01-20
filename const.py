from dataclasses import dataclass
from share import *

FPS = 60
FONT_NAME = 'data/other/font.ttf'
GRAVITY = 1


@dataclass(frozen=True)
class MainCharacterData():
	start_x: int = width // 2
	start_y: int = height - 250
	speed: int = 400
	gravity: int = 300


@dataclass(frozen=True)
class PureVesselData():
	attacks_interval: int = 1
	gravity: int = 1000
	start_x: int = width - 300
	speed: int = 1500
	hp = 1000


@dataclass(frozen=True)
class SoulWarriorData():
	attacks_interval: int = 2
	gravity: int = 1000
	start_x: int = 700
	speed: int = 100
	hp = 500


@dataclass(frozen=True)
class XeroData():
	attacks_interval: int = 1
	start_x: int = 700
	start_y: int = height - 450
	speed_x: int = 200
	speed_y: int = 100
	hp: int = 750


@dataclass(frozen=True)
class MaskData():
	start_x: int = 50
	y: int = 50


@dataclass(frozen=True)
class BulletData():
	speed: int = 800


@dataclass(frozen=True)
class SoulWarriorMagicData():
	speed: int = 800