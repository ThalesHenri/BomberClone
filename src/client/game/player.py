import pygame
from public.settings import *

class Player:
    
    def __init__(self,pos:tuple,color:tuple): #por equanto vai ser cor pra diferenciar
        self.x, self.y = pos
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE -10 , TILE_SIZE - 10)
        self.speed = PLAYER_SPEED
        self.bombs = 1
        self.bombs_placed = 0
        
    def move(self,dx:int,dy:int,game_map:list)->None:
        """Defines the movements of the player in the field

        Args:
            dx (int): x
            dy (int): y
            game_map (list): map of the game
        """
        self.x += dx
        self.rect.x = self.x
        if self.check_collision(game_map):
            self.x -= dx
            self.rect.x = self.x

        # Movimento Vertical
        self.y += dy
        self.rect.y = self.y
        if self.check_collision(game_map):
            self.y -= dy
            self.rect.y = self.y
            
    def check_colision(self, game_map)->bool:
       for row_index, row in enumerate(game_map):
            for col_index, cell in enumerate(row):
                if cell == 1:  # 1 é parede indestrutível nas nossas leis
                    wall_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(wall_rect):
                        return True
            return False
    def place_bomb(self)->None:
        if self.bombs_placed < self.max_bombs:
            # Permissao para colocar bomba
            return True
        return False
    
    
    
    
    def draw(self, surface:pygame.Surface)->None:
        """Renderiza o herói na superfície da arena"""
        pygame.draw.rect(surface, self.color, self.rect)
        # Detalhe: Um pequeno retângulo interno para dar profundidade ao "sprite"
        inner_rect = self.rect.inflate(-8, -8)
        pygame.draw.rect(surface, (255, 255, 255), inner_rect, 2)
    