import pygame
from Config import *
from Tiles import Camera


class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen, initial_x_location, initial_y_location, initial_image, up_img_1, up_img_2, down_img_1,
                 down_img_2, left_img_1, left_img_2, right_img_1, right_img_2, health, damage, exp_on_kill):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.initial_x_location = initial_x_location
        self.initial_y_location = initial_y_location
        self.image = pygame.transform.scale(pygame.image.load(initial_image).convert_alpha(), (28, 28))
        self.up_img_1 = self.image = pygame.transform.scale(pygame.image.load(up_img_1).convert_alpha(),
                                                            (28, 28))
        self.up_img_2 = self.image = pygame.transform.scale(pygame.image.load(up_img_2).convert_alpha(),
                                                            (28, 28))
        self.left_img_1 = self.image = pygame.transform.scale(pygame.image.load(left_img_1).convert_alpha(),
                                                              (28, 28))
        self.left_img_2 = self.image = pygame.transform.scale(pygame.image.load(left_img_2).convert_alpha(),
                                                              (28, 28))
        self.down_img_1 = self.image = pygame.transform.scale(pygame.image.load(down_img_1).convert_alpha(),
                                                              (28, 28))
        self.down_img_2 = self.image = pygame.transform.scale(pygame.image.load(down_img_2).convert_alpha(),
                                                              (28, 28))
        self.right_img_1 = self.image = pygame.transform.scale(pygame.image.load(right_img_1).convert_alpha(),
                                                               (28, 28))
        self.right_img_2 = self.image = pygame.transform.scale(pygame.image.load(right_img_2).convert_alpha(),
                                                               (28, 28))
        self.rect = self.image.get_rect(topleft=(initial_x_location, initial_y_location))
        self._layer = ENEMY_LAYER
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2
        self.health = health
        self.max_health = health
        self.previous_x_location = self.rect.x
        self.previous_y_location = self.rect.y
        self.up_counter = 0
        self.left_counter = 0
        self.down_counter = 0
        self.right_counter = 0
        self.damage = damage
        self.exp_on_kill = exp_on_kill

    def draw_health_bar(self, camera):
        health_bar_rect = pygame.Rect(0, 0, TILESIZE, 5)
        health_bar_rect.topleft = camera.apply(self).topleft
        health_bar_rect.y += 30
        pygame.draw.rect(self.screen, RED, health_bar_rect)  # Red background
        health_bar_rect.width = TILESIZE * (self.health / self.max_health)
        pygame.draw.rect(self.screen, GREEN, health_bar_rect)

    def animation(self):
        if self.rect.y < self.previous_y_location:
            self.up_counter = (self.up_counter + 1) % 20
            if self.up_counter in range(0, 10):
                self.image = self.up_img_1
            else:
                self.image = self.up_img_2

        elif self.rect.y > self.previous_y_location:
            self.down_counter = (self.down_counter + 1) % 20
            if self.down_counter in range(0, 10):
                self.image = self.down_img_1
            else:
                self.image = self.down_img_2

        elif self.rect.x < self.previous_x_location:
            self.left_counter = (self.left_counter + 1) % 20
            if self.left_counter in range(0, 10):
                self.image = self.left_img_1
            else:
                self.image = self.left_img_2

        elif self.rect.x > self.previous_x_location:
            self.right_counter = (self.right_counter + 1) % 20
            if self.right_counter in range(0, 10):
                self.image = self.right_img_1
            else:
                self.image = self.right_img_2

        self.previous_x_location = self.rect.x
        self.previous_y_location = self.rect.y

    def idle_animation(self):
        pass

    def check_collision(self, tile_collision_group, player_collision_group):
        tile_collision = pygame.sprite.spritecollide(self, tile_collision_group, False)
        player_collision = pygame.sprite.spritecollide(self, player_collision_group, False)
        if self.health <= 0:
            for player in player_collision_group:
                player.exp += self.exp_on_kill
            self.kill()
        if tile_collision or player_collision:
            self.rect.move_ip(-self.velocity.x, -self.velocity.y)
            self.velocity = pygame.math.Vector2(-1, -1)

    def update_movement(self, player_rect, tile_collision_group, player_collision_group):
        distance = pygame.math.Vector2(player_rect.x - self.rect.x, player_rect.y - self.rect.y).length()
        if distance <= TILESIZE * 8:
            direction = pygame.math.Vector2(player_rect.x - self.rect.x, player_rect.y - self.rect.y)
            if distance > 0:
                direction.normalize_ip()
                self.velocity = direction * self.speed
                self.check_collision(tile_collision_group, player_collision_group)
            else:
                self.idle_animation()
            self.rect.move_ip(self.velocity)
            self.animation()


class Bat(Enemies):
    def __init__(self, screen, initial_x_location, initial_y_location, health):
        super().__init__(screen, initial_x_location, initial_y_location, "Enemy/Bat/left1.png",
                         "Enemy/Bat/left1.png", "Enemy/Bat/left2.png",
                         "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", "Enemy/Bat/left1.png",
                         "Enemy/Bat/left2.png", "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", health, 1,
                         35)


class TestEnemy(Enemies):
    def __init__(self, screen, initial_x_location, initial_y_location, health):
        super().__init__(screen, initial_x_location, initial_y_location, "Enemy/Bat/left1.png",
                         "Enemy/Bat/left1.png", "Enemy/Bat/left2.png",
                         "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", "Enemy/Bat/left1.png",
                         "Enemy/Bat/left2.png", "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", health, 1,
                         35)
