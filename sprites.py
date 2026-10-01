import math
from functools import lru_cache

import pygame

from settings import ASSETS, BULLET_SPEED, SCREEN_RECT


@lru_cache(maxsize=None)
def load_image(name, size=None, trim=False):
    """Load an image from assets/ once and reuse it afterwards."""
    image = pygame.image.load(name).convert_alpha()
    if trim:  # cut away transparent margins so the rect matches the visible sprite
        image = image.subsurface(image.get_bounding_rect()).copy()
    if size:
        image = pygame.transform.scale(image, size)
    return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, owner):
        super().__init__()
        self.owner = owner
        heading = math.radians(angle + 90)
        # bullet.png points right, so rotate it to face the direction of travel
        self.image = pygame.transform.rotate(load_image("bullet.png"), angle + 90)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(math.cos(heading), -math.sin(heading)) * BULLET_SPEED

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not SCREEN_RECT.colliderect(self.rect):
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    """A rock that fires bullets in a fixed direction."""

    def __init__(self, x, y, image, angle):
        super().__init__()
        self.image = load_image(image, size=(150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top + 20, self.angle, self)


class ChargingStation(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = load_image(image, size=(150, 150))
        self.rect = self.image.get_rect(center=(x, y))
