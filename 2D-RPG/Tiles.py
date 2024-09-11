from Config import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image, layer, tile_size_multiplier):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                                            (TILESIZE * tile_size_multiplier, TILESIZE * tile_size_multiplier))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.layer = layer


class TransitionTile(Tile):
    def __init__(self, screen, x, y, image, layer, tile_size_multiplier):
        super().__init__(screen, x, y, image, layer, tile_size_multiplier)
        self.is_transition_key_pressed = False

    def is_key_pressed(self, player):
        keys = pygame.key.get_pressed()
        if player.rect.colliderect(self) and keys[pygame.K_e]:
            self.is_transition_key_pressed = True
        return self.is_transition_key_pressed

    def tilemap_transition_handler(self, reset_boolean_database, create_tilemap):
        self.is_transition_key_pressed = False
        reset_boolean_database
        create_tilemap


class Chest(Tile):
    def __init__(self, screen, x, y, image, layer, tile_size_multiplier, chest_contents):
        super().__init__(screen, x, y, image, layer, tile_size_multiplier)
        self.chest_contents = chest_contents
        self.number_of_items_inside_chest = len(chest_contents)
        self.is_chest_open = False
        self.cooldown = 0
        self.cooldown_time = 200

        self.columns = 4
        self.rows = 6
        self.chest_array_representation = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.selected_chest_slot = [[False for _ in range(self.rows)] for _ in range(self.columns)]
        self.item_rectangle_array_representation = [[None for _ in range(self.rows)] for _ in range(self.columns)]

    def on_chest_open(self, player):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown > self.cooldown_time:
            if player.rect.y in range(self.rect.bottom - 2, self.rect.bottom + 2):
                if keys[pygame.K_SPACE]:
                    self.is_chest_open = not self.is_chest_open
                    self.cooldown = current_time
            if player.rect.x not in range(self.rect.x - 30, self.rect.x + 30):
                self.is_chest_open = False
            if player.rect.y not in range(self.rect.bottom - 30, self.rect.bottom + 30):
                self.is_chest_open = False

    def draw_chest_slots(self, screen, selected_chest_slot_image, unselected_chest_slot_image):
        x_pos = 1000
        y_pos = 50
        item_index = 0
        for row in range(self.rows):
            for col in range(self.columns):

                chest_slot = pygame.Rect(x_pos, y_pos, TILESIZE * 2, TILESIZE * 2)
                self.chest_array_representation[col][row] = chest_slot
                pygame.draw.rect(screen, BLACK, chest_slot)
                x_pos = x_pos + TILESIZE * 2

                if self.selected_chest_slot[col][row]:
                    screen.blit(selected_chest_slot_image, self.chest_array_representation[col][row])
                else:
                    screen.blit(unselected_chest_slot_image, self.chest_array_representation[col][row])

                if item_index < self.number_of_items_inside_chest:
                    item_image = self.chest_contents[item_index].image
                    item_rect = item_image.get_rect(center=chest_slot.center)
                    self.chest_array_representation[col][row] = item_rect
                    self.item_rectangle_array_representation[col][row] = item_rect
                    screen.blit(item_image, item_rect)
                    item_index += 1

            x_pos = 1000
            y_pos = y_pos + TILESIZE * 2

    def select_chest_slot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row in range(self.rows):
            for col in range(self.columns):
                if self.chest_array_representation[col][row].collidepoint(mouse_x, mouse_y):
                    if self.chest_array_representation[col][row] == self.item_rectangle_array_representation[col][row]:
                        pass
                    for c in range(self.columns):
                        for r in range(self.rows):
                            self.selected_chest_slot[c][r] = False
                    self.selected_chest_slot[col][row] = not self.selected_chest_slot[col][row]

    def move_items_around(self):
        pass


class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)

    def apply(self, sprite):
        return sprite.rect.move(self.offset)

    def update(self, target_group):
        if target_group.sprites():
            target_sprite = target_group.sprites()[0]
            target_center = pygame.math.Vector2(target_sprite.rect.x + target_sprite.rect.width / 2,
                                                target_sprite.rect.y + target_sprite.rect.height / 2)
            self.offset = pygame.math.Vector2(self.display_surface.get_width() / 2,
                                              self.display_surface.get_height() / 2) - target_center
