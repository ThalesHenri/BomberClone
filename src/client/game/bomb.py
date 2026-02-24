import pygame
from public.settings import *


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int,player:object):
        super().__init__()
        self.pos = (x, y)
        self.sheet = pygame.image.load('src/assets/bombSheet.png')
        self.image = self._get_sprite(self.sheet, 0, 48, 18, 18, 2)
        self.rect = self.image.get_rect(center=self.pos)
        self.spawn_time = pygame.time.get_ticks()
        self.state = 0 # 0: explodindo, 1: explodiu
        self.fuse_time = 3000
        self.explosion_duration = 500
        self.expired = False
        self.is_solid = False
        self.player = player
        
    
    def explode(self,grid:list)->object:
        # chamar a explosão
        explosion_level = 1
        explosion_x = self.pos[0] 
        explosion_y = self.pos[1] 
        explosion = Explosion(explosion_x, explosion_y, self.explosion_duration, grid, explosion_level)
        return explosion
    
    
    def draw(self, surface:pygame.surface)->None:
        self.state = 0
        self.rect.topleft = (self.pos[0], self.pos[1])
        surface.blit(self.image, self.rect)
        
        
    def update(self)->None:
        now = pygame.time.get_ticks()
        time_passed = now - self.spawn_time

        
        if not self.is_solid:
            if not self.rect.colliderect(self.player.rect):
                self.is_solid = True
                print("bomba agora é solida")
        
        # Armada
        if self.state == 0:
            if time_passed >= self.fuse_time:
                self.state = 1
                self.spawn_time = now
                
            
        # Explodindo
        if self.state == 1:
            if time_passed >= self.explosion_duration:
                self.state = 2
                self.expired = True
        
                # chamar a explosão
        
        
        

        
    
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
    def __init__(self, x: int , y: int, duration: int, grid:list, level:int=1):
        super().__init__()
        self.pos = (x, y)
        self.duration = duration
        self.grid = grid
        self.sheet = pygame.image.load('src/assets/bombSheet.png')
        self.image = self._get_sprite(self.sheet, 30, 175, 18, 18, 2)
        self.spawn_time = pygame.time.get_ticks()
        self.explosion_area_images = {
            "up": self._get_sprite(self.sheet, 30, 150, 18, 18, 2),
            "right": self._get_sprite(self.sheet, 18, 0, 18, 18, 2),
            "down": self._get_sprite(self.sheet, 30, 190, 18, 18, 2),
            "left": self._get_sprite(self.sheet, 54, 0, 18, 18, 2)
        }
        self.rect = self.image.get_rect(center=self.pos)
        self.range = {"up": 0, "right": 0, "down": 0, "left": 0}
        self.level = level
        self.expired = False
        self._get_range()
        self._calculate_propagation(grid, self.range["up"])
        


    

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
    
    
    def _get_range(self)->dict:
        if self.level == 1:
            self.range = {"up": 1, "right": 1, "down": 1, "left": 1}
        return self.range

    
    def _calculate_propagation(self, grid, max_range: int):
        """Calculates the propagation of the explosion, did this and haved a bug,
        need more logical thinking

        Args:
            grid (_type_): _description_
            max_range (int): _description_
        """
        pass
            
        
    
    
    def draw(self, surface:pygame.surface)->None:
        surface.blit(self.image, self.pos)
        
        
        
    def update(self,grid:list)->None:
        now = pygame.time.get_ticks()
        time_passed = now - self.spawn_time
        
        
        if time_passed >= self.duration:
            self.expired = True
        
            