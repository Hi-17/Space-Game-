from pathlib import Path

import pygame

ASSETS = Path(__file__).parent / "assets"

WIDTH = 1100
HEIGHT = 680
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
FPS = 60

# Ship physics (per frame)
ROTATION_SPEED = 3       # degrees
THRUST = 0.12
GRAVITY = 0.01
DRAG = 0.98              # velocity is multiplied by this every frame
NOSE_OFFSET = 50         # bullets spawn this far in front of the ship

# Fuel and score
START_FUEL = 1000
START_SCORE = 100
WIN_SCORE = 150
THRUST_FUEL_COST = 0.25  # fuel burned per frame while thrusting
HIT_PENALTY = 10         # score lost when hit by a bullet
STATION_REWARD = 10      # score gained at the charging station
STATION_REFUEL = 150     # fuel gained at the charging station
STATION_COOLDOWN = 5000  # ms between station rewards

# Bullets
BULLET_SPEED = 6
ROCK_FIRE_INTERVAL = 2000  # ms between shots from the rock

WHITE = (255, 255, 255)
