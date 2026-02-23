import pygame
import time
from public.settings import *


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self,pos:tuple,offset:tuple):
        super().__init__()
        w,h =16,16
        s= 2
        self.sheet = pygame.image.load('src/assets/bombSheet.png').convert_alpha()
        self.animations = [
            self._get_sprite(self.sheet, 0, 114, w, h, s),
            self._get_sprite(self.sheet, 18, 114, w, h, s),
            self._get_sprite(self.sheet, 3, 114, w, h, s),
            self._get_sprite(self.sheet, 100, 114, w, h, s),
            self._get_sprite(self.sheet, 118, 114, w, h, s),
            self._get_sprite(self.sheet, 82, 114, w, h, s),
            
            
        ]
        self.frame_index = 0
        self.offset_x, self.offset_y = offset
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()
        self.state = 0 #0: armada, 1: explodida

        #tempo
        self.spawn_time = pygame.time.get_ticks()
        self.bomb_time = 3000 # 3 sec
        
    
    
    
    
    def _get_sprite(self,
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
    
    
    def _update(self)->None:
       # ESTADO 0: ARMADA (Pulsando)
        if self.state == 0:
            current_time = pygame.time.get_ticks()
            self._animate_bomb()
            # Se passou 3 segundos, muda para o estado de explosão
            if current_time - self.spawn_time >= 3000: 
                self.state = 1
                self.frame_index = 0 # Reseta para começar a animação de fogo
                self.spawn_time = current_time # Reaproveita a variável para o tempo do fogo

        # ESTADO 1: EXPLODINDO (Fogo na tela)
        elif self.state == 1:
            self._animate_explosion()
            # Se o fogo ficou na tela por 500ms, a bomba some
            if current_time - self.spawn_time >= 500:
                self.kill() # Remove o sprite do jogo
                
    
    def _animate_bomb(self):
        """Animação da bomba pulsando (State 0)"""
        self.frame_index += 0.1 # Velocidade lenta para o pulsar
        if self.frame_index >= 3: # Supondo que você tenha 3 frames de bomba
            self.frame_index = 0
        self.image = self.animations[int(self.frame_index)]

    def _animate_explosion(self):
        """Animação do fogo (State 1)"""
        # Aqui usamos os frames de fogo que você captou na sheet
        # Supondo que os frames de fogo comecem após o índice 3
        self.frame_index += 0.2 
        if self.frame_index >= len(self.animations):
            self.frame_index = len(self.animations) - 1
        self.image = self.animations[int(self.frame_index)]

    
    def draw(self, surface:pygame.surface)->None:
        self.rect.topleft = (self.offset_x, self.offset_y)
        surface.blit(self.image, self.rect)
        self._update()