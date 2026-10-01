import sys

import pygame

from settings import (
    HEIGHT, FPS, HIT_PENALTY, ROCK_FIRE_INTERVAL, START_FUEL, STATION_COOLDOWN,
    STATION_REFUEL, STATION_REWARD, WHITE, WIDTH, WIN_SCORE,
)
from ship import Ship
from sprites import ChargingStation, Obstacle, load_image

P1_CONTROLS = {
    "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
    "thrust": pygame.K_UP, "fire": pygame.K_SPACE,
}
P2_CONTROLS = {
    "left": pygame.K_a, "right": pygame.K_d,
    "thrust": pygame.K_w, "fire": pygame.K_s,
}


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Duel")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 80)
        self.background = pygame.transform.scale(
            load_image("background.jpeg"), (WIDTH, HEIGHT))
        self.rock_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.rock_event, ROCK_FIRE_INTERVAL)

        self.player1 = Ship(100, 300, 270, P1_CONTROLS, "Player 1")
        self.player2 = Ship(1030, 300, 90, P2_CONTROLS, "Player 2")
        self.ships = [self.player1, self.player2]
        self.ship_group = pygame.sprite.Group(self.ships)
        self.stations = pygame.sprite.Group(
            ChargingStation(1030, 60, "station.png"),
            ChargingStation(1030, 100, "platform.png"),
        )
        self.rock = Obstacle(550, 550, "rock.png", 360)
        self.bullets = pygame.sprite.Group()
        self.winner = None
        self.running = True

    def restart(self):
        for ship in self.ships:
            ship.reset()
        self.bullets.empty()
        self.winner = None


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.winner:
                    if event.key == pygame.K_r:
                        self.restart()
                else:
                    for ship in self.ships:
                        if event.key == ship.controls["fire"]:
                            self.bullets.add(ship.shoot())
            elif event.type == self.rock_event and not self.winner:
                self.bullets.add(self.rock.shoot())


    def check_collisions(self):
        now = pygame.time.get_ticks()
        for ship in self.ships:
            hits = pygame.sprite.spritecollide(
                ship, self.bullets, False, pygame.sprite.collide_mask)
            for bullet in hits:
                if bullet.owner is not ship:
                    ship.score -= HIT_PENALTY
                    bullet.kill()

            at_station = pygame.sprite.spritecollideany(
                ship, self.stations, pygame.sprite.collide_mask)
            if at_station and now - ship.last_station_time >= STATION_COOLDOWN:
                ship.score += STATION_REWARD
                ship.fuel = min(START_FUEL, ship.fuel + STATION_REFUEL)
                ship.last_station_time = now

    def check_winner(self):
        for ship, opponent in ((self.player1, self.player2), (self.player2, self.player1)):
            if ship.score >= WIN_SCORE or opponent.score <= 0:
                self.winner = ship
                return


    def draw_panel(self, text, **anchor):
        label = self.font.render(text, True, WHITE)
        panel = pygame.Surface((label.get_width() + 20, label.get_height() + 12), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 130))
        panel.blit(label, (10, 6))
        self.screen.blit(panel, panel.get_rect(**anchor))

    def draw_hud(self):
        for ship, anchor in ((self.player1, {"topleft": (15, 15)}),
                             (self.player2, {"topright": (930, 15)})):
            self.draw_panel(f"{ship.name}   Score {ship.score}   Fuel {int(ship.fuel)}", **anchor)
        self.draw_panel(
            "P1: arrows + space      P2: A / D / W + S",
            midbottom=(WIDTH // 2, HEIGHT - 10))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        title = self.big_font.render(f"{self.winner.name} wins!", True, WHITE)
        hint = self.font.render("Press R to play again or Esc to quit", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.stations.draw(self.screen)
        self.screen.blit(self.rock.image, self.rock.rect)
        self.ship_group.draw(self.screen)
        self.bullets.draw(self.screen)
        self.draw_hud()
        if self.winner:
            self.draw_game_over()
        pygame.display.flip()


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if not self.winner:
                self.ship_group.update()
                self.bullets.update()
                self.check_collisions()
                self.check_winner()
            self.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
