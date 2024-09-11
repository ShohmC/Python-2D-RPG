import pygame
import Player
from Tiles import *
from Config import *


class Sword(pygame.sprite.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.image = pygame.image.load("Items/Sword.png")
        self.damage = damage


class Bow(pygame.sprite.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.image = pygame.image.load("Items/Bow.png")
        self.damage = damage


class SwordAttack(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y):
        super().__init__()
        self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_right.png")
        self.rect = self.image.get_rect(center=(initial_x, initial_y))
        self.cooldown = 0
        self.cooldown_time = 500
        self.despawn_counter = 0
        self.sword_attack_group = pygame.sprite.LayeredUpdates()
        self.velocity = pygame.math.Vector2(0, 0)
        self.hit_enemies = set()  # Keep track of hit enemies to avoid repeated damage

    def attack(self, player_up, player_left, player_down, player_right, player_x, player_y):
        time = pygame.time.get_ticks()

        if time - self.cooldown >= self.cooldown_time:
            if player_up:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_up.png")
                self.sword_attack_sprite = SwordAttack(player_x + 10, player_y - 10)
            elif player_left:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_left.png")
                self.sword_attack_sprite = SwordAttack(player_x - 10, player_y + 10)
            elif player_down:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_down.png")
                self.sword_attack_sprite = SwordAttack(player_x + 10, player_y + 30)
            elif player_right:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_right.png")
                self.sword_attack_sprite = SwordAttack(player_x + 30, player_y + 10)

            self.sword_attack_group.add(self.sword_attack_sprite)
            self.cooldown = time

    def check_collision(self, tile_collision_group, enemy_collision_group, sword_object):
        tile_collision = pygame.sprite.spritecollide(self, tile_collision_group, False)
        enemy_collision = pygame.sprite.spritecollide(self, enemy_collision_group, False)

        if enemy_collision:
            for enemy in enemy_collision:
                if enemy not in self.hit_enemies:  # Check if enemy was already hit
                    enemy.health -= sword_object.damage
                    self.hit_enemies.add(enemy)  # Mark enemy as hit

        if tile_collision:
            self.kill()

    def draw(self, screen, camera):
        for sword in self.sword_attack_group:
            screen.blit(self.image, camera.apply(sword))

    def update(self, tile_collision_group, enemy_collision_group, sword_object):
        self.despawn_slash()
        self.check_collision(tile_collision_group, enemy_collision_group, sword_object)
        self.sword_attack_group.update(tile_collision_group, enemy_collision_group, sword_object)

    def despawn_slash(self):
        self.despawn_counter += 1
        if self.despawn_counter >= 10:
            self.kill()


class BowAttack(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y, velocity_x, velocity_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Player/Bow_Animations/arrow_up.png")
        self.rect = self.image.get_rect(center=(initial_x, initial_y))
        self.cooldown = 0
        self.cooldown_time = 1000
        self.velocity = pygame.math.Vector2(velocity_x, velocity_y)
        self.arrow_distance_travelled = 0
        self.bow_attack_group = pygame.sprite.LayeredUpdates()

    def attack(self, player_up, player_left, player_down, player_right, initial_x, initial_y):
        time = pygame.time.get_ticks()

        if time - self.cooldown >= self.cooldown_time:
            if player_up:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_up.png")
                self.bow_attack_sprite = BowAttack(initial_x, initial_y, 0, -3)
            if player_left:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_left.png")
                self.bow_attack_sprite = BowAttack(initial_x, initial_y, -3, 0)
            if player_down:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_down.png")
                self.bow_attack_sprite = BowAttack(initial_x, initial_y, 0, 3)
            if player_right:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_right.png")
                self.bow_attack_sprite = BowAttack(initial_x, initial_y, 3, 0)

            self.bow_attack_group.add(self.bow_attack_sprite)
            self.cooldown = time

    def check_collision(self, tile_collision_group, enemy_collision_group, bow_object):
        tile_collision = pygame.sprite.spritecollide(self, tile_collision_group, False)
        enemy_collision = pygame.sprite.spritecollide(self, enemy_collision_group, False)

        if enemy_collision:
            for enemy in enemy_collision:
                enemy.health -= bow_object.damage

        if tile_collision or enemy_collision:
            self.kill()

    def draw(self, screen, camera):
        for arrow in self.bow_attack_group:
            arrow.rect.move_ip(arrow.velocity)
            screen.blit(self.image, camera.apply(arrow))

    def update(self, player_up, player_left, player_down, player_right, tile_collision_group, enemy_collision_group,
               initial_x, initial_y, bow_object):
        self.check_collision(tile_collision_group, enemy_collision_group, bow_object)
        self.bow_attack_group.update(player_up, player_left, player_down, player_right, tile_collision_group,
                                     enemy_collision_group, initial_x, initial_y, bow_object)
        self.despawn_arrow()

    def despawn_arrow(self):
        self.arrow_distance_travelled += self.velocity.length()
        if self.arrow_distance_travelled >= TILESIZE * 4:
            self.kill()