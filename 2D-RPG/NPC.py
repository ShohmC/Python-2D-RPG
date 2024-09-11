from Tiles import *
from Player import *


class NPC(Tile):
    def __init__(self, screen, x, y, image, layer, tile_size_multiplier):
        super().__init__(screen, x, y, image, layer, tile_size_multiplier)

    def idle_movement(self):
        pass

    def interaction(self, player):
        if player.rect.x in range(self.rect.x - 30, self.rect.x + 30):
            pass
            # create rectangle above npc and blit the fuckin exclam image on top of it



