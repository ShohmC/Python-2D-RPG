import time
from pygame.locals import *
from Menus import *
from TilemapHandler import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

hotbar_transform_scale = pygame.transform.scale(pygame.image.load(tiles_dictionary["Hotbar"]).convert_alpha(),
                                                (TILESIZE * 2, TILESIZE * 2))
selected_hotbar_transform_scale = pygame.transform.scale(
    pygame.image.load(tiles_dictionary["Selected Hotbar"]).convert_alpha(),
    (TILESIZE * 2, TILESIZE * 2))

sword_item = Sword(5)
bow_item = Bow(3)


class Game:
    def __init__(self):
        self.time_since_last_click = 0
        self.double_click_threshold = .2

        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = Camera()
        self.hotbar = Hotbar(hotbar_transform_scale, selected_hotbar_transform_scale)
        self.inventory = Inventory(hotbar_transform_scale, selected_hotbar_transform_scale)
        self.item_upgrade_menu = ItemUpgradeMenu()
        self.bow_attack_sprite = BowAttack(0, 0, 0, 0)
        self.sword_attack_sprite = SwordAttack(0, 0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == MOUSEWHEEL:
                if event.y > 0:
                    self.hotbar.select_next_hotbar_slot(1)
                else:
                    self.hotbar.select_next_hotbar_slot(-1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = time.time()
                time_since_last_click = current_time - self.time_since_last_click

                if (not self.inventory.is_inventory_enabled and not tm.chest_tile.is_chest_open and
                        self.hotbar.current_slot_index == 1):
                    self.bow_attack_sprite.attack(tm.player_character.counter_booleans[0],
                                                  tm.player_character.counter_booleans[1],
                                                  tm.player_character.counter_booleans[2],
                                                  tm.player_character.counter_booleans[3],
                                                  tm.player_character.rect.x, tm.player_character.rect.y)

                if (not self.inventory.is_inventory_enabled and not tm.chest_tile.is_chest_open and
                        self.hotbar.current_slot_index == 0):
                    self.sword_attack_sprite.attack(tm.player_character.counter_booleans[0],
                                                    tm.player_character.counter_booleans[1],
                                                    tm.player_character.counter_booleans[2],
                                                    tm.player_character.counter_booleans[3],
                                                    tm.player_character.rect.x, tm.player_character.rect.y)

                if self.inventory.is_inventory_enabled:
                    self.inventory.select_inventory_slot()

                    for row in range(self.inventory.columns):
                        for col in range(self.inventory.rows):
                            if (self.inventory.selected_slot[row][col] == any(
                                    self.inventory.selected_slot[col][row] for
                                    col in range(self.inventory.columns) for
                                    row in range(self.inventory.rows))
                                    and time_since_last_click <= self.double_click_threshold):
                                self.inventory.selected_slot[row][col] = False

                if tm.chest_tile.is_chest_open:
                    tm.chest_tile.select_chest_slot()

                    for row in range(tm.chest_tile.rows):
                        for col in range(tm.chest_tile.columns):
                            if (tm.chest_tile.selected_chest_slot[col][row] == any(
                                    tm.chest_tile.selected_chest_slot[col][row] for
                                    col in range(tm.chest_tile.columns) for
                                    row in range(tm.chest_tile.rows))
                                    and time_since_last_click <= self.double_click_threshold):
                                tm.chest_tile.selected_chest_slot[col][row] = False

                self.time_since_last_click = current_time

    def update(self):
        tm.player_sprite_group.update(tm.collision_tile_sprite_group,
                                      tm.collision_enemy_sprite_group, self.hotbar)

        self.camera.update(tm.player_sprite_group)
        for chests in tm.chest_sprite_group.sprites():
            chests.on_chest_open(tm.player_character)
        for enemies in tm.enemy_sprite_group.sprites():
            enemies.update_movement(tm.player_character.rect,
                                    tm.collision_tile_sprite_group, tm.player_sprite_group)

        for npc in tm.npc_sprite_group.sprites():
            npc.interaction(tm.player_character)

        self.bow_attack_sprite.update(tm.player_character.counter_booleans[0],
                                      tm.player_character.counter_booleans[1],
                                      tm.player_character.counter_booleans[2],
                                      tm.player_character.counter_booleans[3],
                                      tm.collision_tile_sprite_group, tm.collision_enemy_sprite_group,
                                      tm.player_character.rect.x, tm.player_character.rect.y, bow_item)

        self.sword_attack_sprite.update(tm.collision_tile_sprite_group, tm.collision_enemy_sprite_group, sword_item)

        self.inventory.enable_inventory()
        self.item_upgrade_menu.on_menu_open()
        tm.tile_sprite_group.update()
        tm.update()

    def draw(self):
        for tiles in tm.tile_sprite_group.sprites():
            screen.blit(tiles.image, self.camera.apply(tiles))

        for players in tm.player_sprite_group.sprites():
            screen.blit(players.image, self.camera.apply(players))
            players.draw_player_health_bar(screen)
            players.draw_player_exp_bar(screen)

        for enemy in tm.enemy_sprite_group.sprites():
            screen.blit(enemy.image, self.camera.apply(enemy))
            enemy.draw_health_bar(self.camera)

        if self.inventory.is_inventory_enabled:
            self.inventory.draw_inventory(screen)

        if self.item_upgrade_menu.is_menu_enabled:
            self.item_upgrade_menu.draw_menu(screen, tm.player_character, sword_item, bow_item)

        if tm.chest_tile.is_chest_open:
            tm.chest_tile.draw_chest_slots(screen, pygame.transform.scale(
                pygame.image.load(tiles_dictionary["Selected Hotbar"]).convert_alpha(), (TILESIZE * 2, TILESIZE * 2)),
                                           pygame.transform.scale(
                                               pygame.image.load(tiles_dictionary["Hotbar"]).convert_alpha(),
                                               (TILESIZE * 2, TILESIZE * 2)))

        self.hotbar.draw_hotbar(screen)
        self.bow_attack_sprite.draw(screen, self.camera)
        self.sword_attack_sprite.draw(screen, self.camera)

        self.clock.tick(FPS)
        pygame.display.flip()

    def main(self):
        tm.create_tutorial_tilemap()
        while self.running:
            screen.fill(RED)
            self.events()
            self.update()
            self.draw()


g = Game()
tm = TilemapHandler(screen)
while g.running:
    g.main()
pygame.quit()
