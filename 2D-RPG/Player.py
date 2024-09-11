import pygame
from Config import *


# Player.py
class PlayerCharacter(pygame.sprite.Sprite):
    def __init__(self, screen, initial_x_location, initial_y_location):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = pygame.math.Vector2(0, 0)
        self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                            (TILESIZE - 4, TILESIZE - 4))  # -4 so player can go through one block gaps
        self.rect = self.image.get_rect(topleft=(initial_x_location, initial_y_location))
        self.screen = screen
        self._layer = PLAYER_LAYER
        self.cooldown = 0
        self.cooldown_time = 200

        self.up_counter = 0
        self.left_counter = 0
        self.down_counter = 0
        self.right_counter = 0

        self.up_boolean = False
        self.left_boolean = False
        self.down_boolean = False
        self.right_boolean = False

        self.counter_booleans = [self.up_boolean, self.left_boolean, self.down_boolean, self.right_boolean]
        self.health = 100

        self.exp = 0
        self.level = 1
        self.upgrade_points = 0

    def level_up_formula(self):
        a, b, c = 10, 25, 35
        exp = a * (self.level * self.level) + b * self.level + c
        return exp

    def set_counter_boolean(self, element):
        for i in range(len(self.counter_booleans)):
            self.counter_booleans[i] = False
        self.counter_booleans[element] = True

    def draw_player_health_bar(self, screen):
        screen.blit(pygame.font.Font(None, 48).render(f"Health", True, BLACK), (50, 50))
        pygame.draw.rect(screen, RED, (175, 55, 150, 25))
        pygame.draw.rect(screen, GREEN, (175, 55, 150 * (self.health / 100), 25))
        screen.blit(pygame.font.Font(None, 36).render(f"{self.health}", True, BLACK), (230, 56))

    def draw_player_exp_bar(self, screen):
        if self.exp > self.level_up_formula():
            self.exp = 0
            self.level += 1
            self.upgrade_points += 1
        screen.blit(pygame.font.Font(None, 36).render(f"{self.level}", True, (0, 0, 0)), (632, 800))
        pygame.draw.rect(screen, BLACK, (354, 830, 576, 15))
        pygame.draw.rect(screen, BLUE, (354, 830, 576 * (self.exp / self.level_up_formula()), 15))

    def check_collision(self, tile_collision_group, enemy_collision_group):
        current_time = pygame.time.get_ticks()
        self.rect.move_ip(self.velocity)
        tile_collisions = pygame.sprite.spritecollide(self, tile_collision_group, False)
        enemy_collisions = pygame.sprite.spritecollide(self, enemy_collision_group, False)

        if tile_collisions:
            self.rect.move_ip(-self.velocity.x, -self.velocity.y)
            return

        if enemy_collisions:
            self.rect.move_ip(-self.velocity.x, -self.velocity.y)
            if enemy_collisions:
                if current_time - self.cooldown > self.cooldown_time:
                    for enemy in enemy_collisions:
                        self.health -= enemy.damage
                    self.cooldown = current_time
                if self.health <= 0:
                    self.kill()

    def sword_movement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.set_counter_boolean(0)
            self.up_counter = (self.up_counter + 1) % 20
            if self.up_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_up_1, (28, 28))
            elif self.up_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_up_2, (28, 28))
            self.velocity.y = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_a]:
            self.set_counter_boolean(1)
            self.left_counter = (self.left_counter + 1) % 20
            if self.left_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_left_1, (28, 28))
            elif self.left_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_left_2, (28, 28))
            self.velocity.x = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_s]:
            self.set_counter_boolean(2)
            self.down_counter = (self.down_counter + 1) % 20
            if self.down_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_down_1, (28, 28))
            elif self.down_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_down_2, (28, 28))
            self.velocity.y = PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_d]:
            self.set_counter_boolean(3)
            self.right_counter = (self.right_counter + 1) % 20
            if self.right_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_right_1, (28, 28))
            elif self.right_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_right_2, (28, 28))
            self.velocity.x = PLAYER_X_VELOCITY * dt

    def bow_movement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.set_counter_boolean(0)
            self.up_counter = (self.up_counter + 1) % 20
            if self.up_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_up_1, (28, 28))
            elif self.up_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_up_2, (28, 28))
            self.velocity.y = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_a]:
            self.set_counter_boolean(1)
            self.left_counter = (self.left_counter + 1) % 20
            if self.left_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_left_1, (28, 28))
            elif self.left_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_left_2, (28, 28))
            self.velocity.x = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_s]:
            self.set_counter_boolean(2)
            self.down_counter = (self.down_counter + 1) % 20
            if self.down_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_down_1, (28, 28))
            elif self.down_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_down_2, (28, 28))
            self.velocity.y = PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_d]:
            self.set_counter_boolean(3)
            self.right_counter = (self.right_counter + 1) % 20
            if self.right_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_right_1, (28, 28))
            elif self.right_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_right_2, (28, 28))
            self.velocity.x = PLAYER_X_VELOCITY * dt

    def movement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.set_counter_boolean(0)
            self.up_counter = (self.up_counter + 1) % 20
            if self.up_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_up_1, (28, 28))
            elif self.up_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_up_2, (28, 28))
            self.velocity.y = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_a]:
            self.set_counter_boolean(1)
            self.left_counter = (self.left_counter + 1) % 20
            if self.left_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_left_1, (28, 28))
            elif self.left_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_left_2, (28, 28))
            self.velocity.x = -PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_s]:
            self.set_counter_boolean(2)
            self.down_counter = (self.down_counter + 1) % 20
            if self.down_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_down_1, (28, 28))
            elif self.down_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_down_2, (28, 28))
            self.velocity.y = PLAYER_Y_VELOCITY * dt

        if keys[pygame.K_d]:
            self.set_counter_boolean(3)
            self.right_counter = (self.right_counter + 1) % 20
            if self.right_counter in range(0, 10):
                self.image = pygame.transform.scale(player_image_right_1, (28, 28))
            elif self.right_counter in range(10, 20):
                self.image = pygame.transform.scale(player_image_right_2, (28, 28))
            self.velocity.x = PLAYER_X_VELOCITY * dt

    def update(self, tile_collision_group, enemy_collision_group, hotbar):
        if hotbar.current_slot_index == 0:
            self.sword_movement()

        if hotbar.current_slot_index == 1:
            self.bow_movement()

        if hotbar.current_slot_index != 0 and hotbar.current_slot_index != 1:
            self.movement()
        self.check_collision(tile_collision_group, enemy_collision_group)
