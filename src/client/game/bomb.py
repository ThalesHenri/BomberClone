import pygame
from public.settings import *


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.pos = (x, y)
        self.sheet = pygame.image.load('src/assets/bombSheet.png')
        self.image = self._get_sprite(self.sheet, 0, 48, 18, 18, 2)
        self.rect = self.image.get_rect(center=self.pos)
        self.state = 0 # 0: explodindo, 1: explodiu
        self.timer = 0
        
    
    def explode(self)->None:
        self.state = 1
        # chamar a explosão
        explosion = Explosion(self.pos[0], self.pos[1], self.image)
        return explosion
    
    
    def draw(self, surface:pygame.surface)->None:
        self.state = 0
        self.rect.topleft = (self.pos[0], self.pos[1])
        surface.blit(self.image, self.rect)

        
    
    def _get_sprite(
            self,
            sheet:pygame.surface,
            x:int,
            y:int,
            width:int,
            height:int,
            scale:int=1
        )->None:
        image = pygame.Surface((width, height))
        image.blit(sheet, (0, 0), (x, y, width, height))

        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        if scale != 1:
            new_size = int(width * scale), int(height * scale)
            image = pygame.transform.scale(image, new_size)
        image = pygame.transform.scale(image, (TILE_SIZE-4, TILE_SIZE-4))

        return image.convert_alpha()
        
        
        
        


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.surface):
        super().__init__()
        self.pos = (x, y)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.timer = 0
        self.range = {"up": 0, "right": 0, "down": 0, "left": 0}