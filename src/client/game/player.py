import pygame
from public.settings import *
from .bomb import Bomb

class Player(pygame.sprite.Sprite):
    
    def __init__(self,pos:tuple,color:tuple,offset:tuple): #por equanto vai ser cor pra diferenciar
        self.x, self.y = pos
        w,h = 18,26
        s = 2
        self.color = color
        self.sheet = pygame.image.load('src/assets/chars.png').convert_alpha()
        self.speed = PLAYER_SPEED
        self.bombs:int = 1
        self.current_direction = "down"
        self.frame_index = 0
        self.bombs_placed = 0
        self.offset_x, self.offset_y = offset
        self.direction = 0 # 0: up, 1: right, 2: down, 3: left como um relogio
        
        self.animations = {
        "down": [self._get_sprite(self.sheet, 4, 4, w, h, s), 
                 self._get_sprite(self.sheet, 20, 4, w, h, s), 
                 self._get_sprite(self.sheet, 38, 4, w, h, s)],
                 
        "up":   [self._get_sprite(self.sheet, 4, 30, w, h, s), 
                 self._get_sprite(self.sheet, 20, 30, w, h, s), 
                 self._get_sprite(self.sheet, 38, 30, w, h, s)],
                 
        "left": [self._get_sprite(self.sheet, 4, 57, w, h, s), 
                 self._get_sprite(self.sheet, 20, 57, w, h, s), 
                 self._get_sprite(self.sheet, 38, 57, w, h, s)]
    }
        self.animations["right"] = [pygame.transform.flip(img, True, False) for img in self.animations["left"]]
        self.image = self.animations[self.current_direction][self.frame_index]
        self.rect = self.image.get_rect()
        
        self.anim_speed = 0.15
    def move(self,dx:int,dy:int,game_map:list,direction:int, bombs:list)->None:
        """Defines the movements of the player in the field

        Args:
            dx (int): x
            dy (int): y
            game_map (list): map of the game
            direction (int): 0: up, 1: right, 2: down, 3: left

        """
        moving = False
        
        if direction == 0:
            self.direction = 0
            moving = True
        elif direction == 1:
            self.direction = 1
            moving = True
        elif direction == 2:
            self.direction = 2
            moving = True
        elif direction == 3:
            self.direction = 3
            moving = True
        
        self._animate(moving)
        
        
       # Movimento Horizontal
        self.x += dx * self.speed  # Movimento horizontal 4 pixels de uma vez
        self.rect.x = self.x
        
        
        if self._check_collision(game_map) or self._check_bomb_collision(bombs):
            self.x -= dx * self.speed
            self.rect.x = self.x

        # Movimento Vertical
        self.y += dy * self.speed
        self.rect.y = self.y
        
        if self._check_collision(game_map) or self._check_bomb_collision(bombs):
            self.y -= dy * self.speed
            self.rect.y = self.y
    
    
    def _animate(self,moving:bool)->None:
        # Mapeia o número da direção para a chave do dicionário
        directions = ["up", "right", "down", "left"]
        current_dir = directions[self.direction]

        if moving:
            # Incrementa o índice do frame baseado na velocidade definida no __init__
            self.frame_index += self.anim_speed
            
            # Reinicia a animação caso chegue ao fim da lista de sprites
            if self.frame_index >= len(self.animations[current_dir]):
                self.frame_index = 0
            
            # Define a imagem atual (converte o índice decimal para inteiro)
            self.image = self.animations[current_dir][int(self.frame_index)]
        else:
            # Se não estiver movendo, reseta para o frame de repouso (índice 0)
            self.frame_index = 0
            self.image = self.animations[current_dir][0]
        
    
           
    def _check_collision(self, game_map)->bool:
        # Transforma a posição de pixel do player de volta para índice da matriz
        # (Subtraímos o offset para saber a posição relativa ao grid)
        grid_x = (self.rect.centerx - self.offset_x) // TILE_SIZE
        grid_y = (self.rect.centery - self.offset_y) // TILE_SIZE

        # Checa apenas os 9 blocos ao redor do jogador (3x3)
        for row in range(grid_y - 1, grid_y + 2):
            for col in range(grid_x - 1, grid_x + 2):
                if 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
                    cell = game_map[row][col]
                    if cell in [BLOCK_WALL, BLOCK_BRICK]:
                        wall_rect = pygame.Rect(
                            self.offset_x + (col * TILE_SIZE),
                            self.offset_y + (row * TILE_SIZE),
                            TILE_SIZE, TILE_SIZE
                        )
                        if self.rect.colliderect(wall_rect):
                            return True
        return False

    
    def _check_bomb_collision(self,bombs:list)->bool:
        """check if there is a collision between the 
            player and the bomb

        Args:
            bombs (list): self.bombs

        Returns:
            bool: if there is a collision
        """
        for bomb in bombs:
            if bomb.is_solid:
                if self.rect.colliderect(bomb.rect):
                    return True
        return False 
    
    
    def place_bomb(self,)->Bomb:
        if self.bombs_placed < self.bombs:
            # Permissao para colocar bomba
            self.bombs_placed += 1
            print(f"Placou bomba {self.bombs_placed}")
            bomb = Bomb(self.x, self.y,self)
            
            return bomb
        else:
            return False
        
        
        
    def reset_bombs(self)->None:
        self.bombs = 1
        self.bombs_placed = 0
        
        

    
    
    def draw(self, surface:pygame.Surface)->None:
        """Renderiza o herói na superfície da arena"""
        self.rect.topleft = (self.x, self.y)

        if hasattr(self, 'image') and self.image:
            # 2. Desenha o sprite do Bomberman
            surface.blit(self.image, self.rect)
        else:
            # Plano B: Se o sprite não carregar, desenha o retângulo colorido
            # para você não ficar "no escuro" durante o desenvolvimento
            pygame.draw.rect(surface, self.color, self.rect)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
            inner_rect = self.rect.inflate(-8, -8)
            pygame.draw.rect(surface, (255, 255, 255), inner_rect, 2)
    
    
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
        