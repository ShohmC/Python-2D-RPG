from Items import *
import pygame


class ItemUpgradeMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_menu_enabled = False
        self.cooldown = 0
        self.cooldown_time = 200
        self.rectangle_upgrade_button = []

    def draw_menu(self, screen, player, sword, bow):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        initial_x = 400
        initial_y = 280
        main_surface = pygame.Surface((960, 750), pygame.SRCALPHA)
        main_surface.fill((0, 0, 0, 128))

        for i in range(3):
            self.rectangle_upgrade_button.append(
                pygame.draw.rect(screen, (0, 129, 255), (initial_x, initial_y, 75, 35)))
            initial_y += 100

        screen.blit(pygame.font.Font(None, 64).render("Upgrade Menu", True, (0, 0, 0)), (200, 135))
        screen.blit(pygame.font.Font(None, 64).render(f"Skill Points: {player.upgrade_points}", True, (0, 0, 0)),
                    (750, 135))
        screen.blit(pygame.font.Font(None, 64).render("Sword", True, (0, 0, 0)), (200, 275))
        screen.blit(pygame.font.Font(None, 64).render("Bow", True, (0, 0, 0)), (200, 375))
        screen.blit(pygame.font.Font(None, 64).render("Health", True, (0, 0, 0)), (200, 475))
        screen.blit(pygame.font.Font(None, 24).render(f"{sword.damage}", True, (0, 0, 0)), (432, 290))
        screen.blit(pygame.font.Font(None, 24).render(f"{bow.damage}", True, (0, 0, 0)), (428, 390))
        screen.blit(pygame.font.Font(None, 24).render(f"{player.health}", True, (0, 0, 0)), (422, 490))
        screen.blit(main_surface, (160, 105))

        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                if self.rectangle_upgrade_button[0].collidepoint(mouse_x, mouse_y) and player.upgrade_points > 0:
                    sword.damage += 1
                    player.upgrade_points -= 1
                if self.rectangle_upgrade_button[1].collidepoint(mouse_x, mouse_y) and player.upgrade_points > 0:
                    bow.damage += 0.5
                    player.upgrade_points -= 1
                if self.rectangle_upgrade_button[2].collidepoint(mouse_x, mouse_y) and player.upgrade_points > 0:
                    player.health += 5
                    player.upgrade_points -= 1

    def on_menu_open(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown > self.cooldown_time:
            if keys[pygame.K_m]:
                self.is_menu_enabled = not self.is_menu_enabled
                self.cooldown = current_time


class Hotbar(pygame.sprite.Sprite):
    def __init__(self, unselected_hotbar_image, selected_hotbar_image):
        pygame.sprite.Sprite.__init__(self)
        self.unselected_hotbar_image = unselected_hotbar_image
        self.selected_hotbar_image = selected_hotbar_image
        self.current_slot_index = 0
        self.hotbar_slots = [None] * 9
        self.hotbar_x_position = []
        self.sword_item = Sword(5)
        self.bow_item = Bow(2)

    def draw_hotbar(self, screen):
        initial_x = 354
        initial_y = 850
        for i in range(len(self.hotbar_slots)):
            hotbar_slot = pygame.Rect(initial_x, initial_y, TILESIZE * 2, TILESIZE * 2)
            self.hotbar_slots[i] = hotbar_slot
            pygame.draw.rect(screen, (0, 0, 0), hotbar_slot)
            if i == self.current_slot_index:
                screen.blit(self.selected_hotbar_image, self.hotbar_slots[i])
            else:
                screen.blit(self.unselected_hotbar_image, (initial_x, initial_y))
            initial_x += TILESIZE * 2

        self.hotbar_slots[0] = Sword(0).image.get_rect(center=self.hotbar_slots[0].center)
        self.hotbar_slots[1] = Bow(0).image.get_rect(center=self.hotbar_slots[1].center)
        screen.blit(Sword(0).image, self.hotbar_slots[0])
        screen.blit(Bow(0).image, self.hotbar_slots[1])

    def select_next_hotbar_slot(self, increment):
        self.current_slot_index = (self.current_slot_index - increment) % len(self.hotbar_slots)


class Inventory(pygame.sprite.Sprite):
    def __init__(self, inventory_slot_image, inventory_selected_slot_image):
        pygame.sprite.Sprite.__init__(self)
        self.inventory_slot_image = inventory_slot_image
        self.inventory_selected_slot_image = inventory_selected_slot_image
        self.is_inventory_enabled = False
        self.cooldown = 0
        self.cooldown_time = 200
        self.counter = 0

        self.rows = 9
        self.columns = 3
        self.inventory = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.selected_slot = [[False for _ in range(self.rows)] for _ in range(self.columns)]

    def enable_inventory(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown > self.cooldown_time:
            if keys[pygame.K_i]:
                self.is_inventory_enabled = not self.is_inventory_enabled
                self.cooldown = current_time

    def draw_inventory(self, screen):
        x_pos = 354
        y_pos = 754
        for row in range(self.columns):
            for col in range(self.rows):
                slot = pygame.Rect(x_pos, y_pos, TILESIZE * 2, TILESIZE * 2)
                self.inventory[row][col] = slot
                pygame.draw.rect(screen, BLACK, slot)
                x_pos = x_pos + TILESIZE * 2

                if self.selected_slot[row][col]:
                    screen.blit(self.inventory_selected_slot_image, self.inventory[row][col])
                else:
                    screen.blit(self.inventory_slot_image, self.inventory[row][col])
            x_pos = 354
            y_pos = y_pos - TILESIZE * 2

    def select_inventory_slot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row in range(self.columns):
            for col in range(self.rows):
                if self.inventory[row][col].collidepoint(mouse_x, mouse_y):
                    for r in range(self.columns):
                        for c in range(self.rows):
                            self.selected_slot[r][c] = False
                    self.selected_slot[row][col] = not self.selected_slot[row][col]
