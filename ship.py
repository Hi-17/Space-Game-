import math

import pygame

from settings import (
    DRAG, GRAVITY, HEIGHT, NOSE_OFFSET, ROTATION_SPEED, START_FUEL,
    START_SCORE, STATION_COOLDOWN, THRUST, THRUST_FUEL_COST, WIDTH,
)
from sprites import Bullet, load_image


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, controls, name):
        super().__init__()
        self.controls = controls
        self.name = name
        self.start = (x, y, angle)
        self.base_image = load_image("ship.png", trim=True)
        self.reset()

    def reset(self):
        x, y, angle = self.start
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2()
        self.angle = angle
        self.fuel = START_FUEL
        self.score = START_SCORE
        self.last_station_time = -STATION_COOLDOWN
        self._apply_rotation()

    def _apply_rotation(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))
        self.mask = pygame.mask.from_surface(self.image)

    def _heading(self):
        radians = math.radians(self.angle + 90)
        return pygame.Vector2(math.cos(radians), -math.sin(radians))

    def thrust(self):
        self.velocity += self._heading() * THRUST
        self.fuel = max(0, self.fuel - THRUST_FUEL_COST)

    def shoot(self):
        nose = self.pos + self._heading() * NOSE_OFFSET
        return Bullet(nose.x, nose.y, self.angle, self)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls["left"]]:
            self.angle += ROTATION_SPEED
        if keys[self.controls["right"]]:
            self.angle -= ROTATION_SPEED
        if keys[self.controls["thrust"]] and self.fuel > 0:
            self.thrust()

        self.velocity.y += GRAVITY
        self.velocity *= DRAG
        self.pos += self.velocity

        # rotate first so we know the sprite's size, then keep it on screen
        self._apply_rotation()
        half_w, half_h = self.image.get_width() / 2, self.image.get_height() / 2
        x = max(half_w, min(WIDTH - half_w, self.pos.x))
        y = max(half_h, min(HEIGHT - half_h, self.pos.y))
        if x != self.pos.x:
            self.velocity.x = 0
        if y != self.pos.y:
            self.velocity.y = 0
        self.pos.update(x, y)
        self.rect.center = (round(x), round(y))
