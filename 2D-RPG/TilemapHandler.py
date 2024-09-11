import pygame
from Tiles import *
from Enemies import *
from Player import *
from Items import *
from Tilemaps import *
from NPC import *


class TilemapHandler(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.tutorial_tilemap_boolean = True
        self.tilemap_boolean = False
        self.tilemap_boolean_2 = False

        self.tile_sprite_group = pygame.sprite.LayeredUpdates()
        self.collision_tile_sprite_group = pygame.sprite.LayeredUpdates()
        self.enemy_sprite_group = pygame.sprite.LayeredUpdates()
        self.collision_enemy_sprite_group = pygame.sprite.LayeredUpdates()
        self.npc_sprite_group = pygame.sprite.LayeredUpdates()
        self.chest_sprite_group = pygame.sprite.LayeredUpdates()
        self.item_sprite_group = pygame.sprite.LayeredUpdates()
        self.player_sprite_group = pygame.sprite.LayeredUpdates()

    def draw_tile(self, column, tile_letter, j, i, image, layer, is_a_collision_tile, tile_size_multiplier):
        if column == tile_letter:
            self.tile_name = Tile(self.screen, j * TILESIZE, i * TILESIZE, image, layer, tile_size_multiplier)
            self.tile_sprite_group.add(self.tile_name)
            if is_a_collision_tile:
                self.collision_tile_sprite_group.add(self.tile_name)
        if column == "C":
            self.chest_tile = Chest(self.screen, j * TILESIZE, i * TILESIZE, image, layer, tile_size_multiplier,
                                    [Sword(5), Bow(3)])
            self.chest_sprite_group.add(self.chest_tile)
            for items in self.chest_tile.chest_contents:
                self.item_sprite_group.add(items)

    def spawn_enemy(self, enemy_name, j, i, health):
        enemy = enemy_name(self.screen, j * TILESIZE, i * TILESIZE, health)
        self.enemy_sprite_group.add(enemy)
        self.collision_enemy_sprite_group.add(enemy)

    def create_tutorial_tilemap(self):
        self.clear_all_tiles()
        self.tutorial_tilemap_boolean = True
        for i, row in enumerate(TUTORIAL_TILEMAP):
            for j, column in enumerate(row):
                grass_tiles = Tile(self.screen, j * TILESIZE, i * TILESIZE, tiles_dictionary["Grass Tile"], GRASS_LAYER,
                                   TILESIZE_MULTIPLIER)
                self.tile_sprite_group.add(grass_tiles)
                if column == "P":
                    self.player_character = PlayerCharacter(self.screen, j * TILESIZE, i * TILESIZE)
                    self.player_sprite_group.add(self.player_character)
                if column == "t":
                    transition_tile = TransitionTile(self.screen, j * TILESIZE, i * TILESIZE,
                                                     tiles_dictionary["Dirt Tile"], 2, TILESIZE_MULTIPLIER)
                    self.tile_sprite_group.add(transition_tile)
                if column == "M":
                    npc_tile = NPC(self.screen, j * TILESIZE, i * TILESIZE, "SillyMan.png", 2, TILESIZE)
                    self.npc_sprite_group.add(npc_tile)
                    self.draw_tile(column, "M", j, i, "SillyMan.png", 2, True, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "F", j, i, "fountain.png", 2, True, 5)
                self.draw_tile(column, "C", j, i, tiles_dictionary["Chests"], 2, True, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "T", j, i, tiles_dictionary["Tree Tile"], 2, True, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "D", j, i, tiles_dictionary["Dirt Tile"], 2, False, TILESIZE_MULTIPLIER)

    def create_tilemap(self):
        self.clear_all_tiles()
        self.tilemap_boolean = True
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                grass_tiles = Tile(self.screen, j * TILESIZE, i * TILESIZE, tiles_dictionary["Grass Tile"], GRASS_LAYER,
                                   TILESIZE_MULTIPLIER)
                self.tile_sprite_group.add(grass_tiles)
                if column == "P":
                    self.player_character.rect.topleft = (j * TILESIZE, i * TILESIZE)
                    self.player_sprite_group.add(self.player_character)
                if column == "t":
                    transition_tile = TransitionTile(self.screen, j * TILESIZE, i * TILESIZE,
                                                     tiles_dictionary["Dirt Tile"], 2, TILESIZE_MULTIPLIER)
                    self.tile_sprite_group.add(transition_tile)
                if column == "E":
                    self.spawn_enemy(Bat, j, i, 20)
                if column == "L":
                    self.spawn_enemy(TestEnemy, j, i, 150)
                self.draw_tile(column, "2", j, i, tiles_dictionary["Grass Ledge Down"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "3", j, i, tiles_dictionary["Grass Ledge Left"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "4", j, i, tiles_dictionary["Grass Ledge Right"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "D", j, i, tiles_dictionary["Dirt Tile"], 2, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "5", j, i, tiles_dictionary["Dirt Ledge Up"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "6", j, i, tiles_dictionary["Dirt Ledge Down"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "7", j, i, tiles_dictionary["Dirt Ledge Left"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "8", j, i, tiles_dictionary["Dirt Ledge Right"], 1, False, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "w", j, i, tiles_dictionary["Wall Tile"], 2, True, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "W", j, i, tiles_dictionary["Water Tile"], 2, True, TILESIZE_MULTIPLIER)
                self.draw_tile(column, "T", j, i, tiles_dictionary["Tree Tile"], 2, True, TILESIZE_MULTIPLIER * 2)
                self.draw_tile(column, "C", j, i, tiles_dictionary["Chests"], 2, True, TILESIZE_MULTIPLIER)

    def create_tilemap2(self):
        self.clear_all_tiles()
        self.tilemap_boolean_2 = True
        for i, row in enumerate(TILEMAP2):
            for j, column in enumerate(row):
                grass_tiles = Tile(self.screen, j * TILESIZE, i * TILESIZE, tiles_dictionary["Grass Tile"], GRASS_LAYER,
                                   TILESIZE_MULTIPLIER)
                self.tile_sprite_group.add(grass_tiles)
                if column == "P":
                    self.player_character.rect.topleft = (j * TILESIZE, i * TILESIZE)
                    self.player_sprite_group.add(self.player_character)
                if column == "t":
                    transition_tile = TransitionTile(self.screen, j * TILESIZE, i * TILESIZE,
                                                     tiles_dictionary["Dirt Tile"], 2, TILESIZE_MULTIPLIER)
                    self.tile_sprite_group.add(transition_tile)

    def clear_all_tiles(self):
        self.tile_sprite_group.empty()
        self.collision_tile_sprite_group.empty()
        self.enemy_sprite_group.empty()
        self.collision_enemy_sprite_group.empty()
        self.chest_sprite_group.empty()
        self.item_sprite_group.empty()
        self.player_sprite_group.empty()

    def reset_boolean_database(self):
        self.tutorial_tilemap_boolean = False
        self.tilemap_boolean = False
        self.tilemap_boolean_2 = False

    def update(self):
        for tiles in self.tile_sprite_group.sprites():
            if isinstance(tiles, TransitionTile) and tiles.is_key_pressed(self.player_character):
                if self.tutorial_tilemap_boolean:
                    tiles.tilemap_transition_handler(self.reset_boolean_database(), self.create_tilemap())
                elif self.tilemap_boolean:
                    tiles.tilemap_transition_handler(self.reset_boolean_database(), self.create_tilemap2())
                elif self.tilemap_boolean_2:
                    tiles.tilemap_transition_handler(self.reset_boolean_database(), self.create_tilemap())
