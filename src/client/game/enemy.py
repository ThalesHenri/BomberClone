import pygame
import random
from public.settings import *



class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos:tuple,offset:tuple):
        super().__init__()
        self.x,self.y = pos
        self.offset_x,self.offset_y = offset
        self.speed = ENEMY_SPEED
        self.frame_index = 0
        self.animation_timer = 0
        self.sheet = pygame.image.load('src/assets/bombSheet.png').convert_alpha()
        self.direction = random.choice([0, 1, 2, 3])  # 0: up, 1: right, 2: down, 3: left
        self.change_direction_timer = 0
        
        # Animações para direita e esquerda
        self.animations = {
            1: [  # right
                self._get_sprite(self.sheet, 0, 240, 18, 18, 2),
                self._get_sprite(self.sheet, 30, 240, 18, 18, 2),
                self._get_sprite(self.sheet, 47, 240, 18, 18, 2),
            ],
            3: [  # left
                pygame.transform.flip(self._get_sprite(self.sheet, 0, 240, 18, 18, 2), True, False),
                pygame.transform.flip(self._get_sprite(self.sheet, 30, 240, 18, 18, 2), True, False),
                pygame.transform.flip(self._get_sprite(self.sheet, 47, 240, 18, 18, 2), True, False),
            ],
        }
        
        # Imagem padrão
        self.image = self.animations.get(self.direction, [self._get_sprite(self.sheet, 0, 240, 18, 18, 2)])[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
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
    
    def _update_animation(self):
        """Atualiza a animação do inimigo para direita e esquerda"""
        if self.direction in self.animations:
            self.animation_timer += 1
            # Muda de frame a cada 10 updates
            if self.animation_timer >= 10:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            
            self.image = self.animations[self.direction][self.frame_index]

    def update(self, game_map, bombs=None):
        """Atualiza a posição do inimigo com colisão e mudança de direção"""
        if bombs is None:
            bombs = []
        
        # Atualiza animação
        self._update_animation()
        
        # Tenta mover na direção atual
        dx, dy = self._get_direction_vector(self.direction)
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Verifica colisão com mapa e bombas
        if self._check_collision(new_x, new_y, game_map) or self._check_bomb_collision(new_x, new_y, bombs):
            # Se colidiu, tenta outras direções
            directions = [0, 1, 2, 3]
            random.shuffle(directions)
            moved = False
            
            for new_direction in directions:
                dx, dy = self._get_direction_vector(new_direction)
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                
                if not self._check_collision(new_x, new_y, game_map) and not self._check_bomb_collision(new_x, new_y, bombs):
                    self.direction = new_direction
                    self.frame_index = 0
                    self.animation_timer = 0
                    self.x = new_x
                    self.y = new_y
                    moved = True
                    break
            
            # Se não conseguiu mover para nenhuma direção, tenta virar
            if not moved:
                self.direction = random.choice([0, 1, 2, 3])
                self.frame_index = 0
                self.animation_timer = 0
        else:
            # Se não colidiu, segue em frente
            self.x = new_x
            self.y = new_y
        
        # Muda de direção aleatoriamente de vez em quando
        self.change_direction_timer += 1
        if self.change_direction_timer > 120:  # A cada 120 frames (~2 segundos)
            self.change_direction_timer = 0
            self.direction = random.choice([0, 1, 2, 3])
            self.frame_index = 0
            self.animation_timer = 0
        
        # Atualiza o rect
        self.rect.topleft = (self.x, self.y)
    
    def _get_direction_vector(self, direction):
        """Retorna o vetor de movimento baseado na direção"""
        if direction == 0:  # up
            return (0, -1)
        elif direction == 1:  # right
            return (1, 0)
        elif direction == 2:  # down
            return (0, 1)
        elif direction == 3:  # left
            return (-1, 0)
        return (0, 0)
    
    def _check_collision(self, new_x, new_y, game_map):
        """Verifica colisão com paredes e tijolos verificando todas as células ocupadas"""
        # Tamanho do inimigo
        enemy_size = TILE_SIZE - 4
        
        # Calcula os cantos do inimigo na nova posição
        left = new_x
        right = new_x + enemy_size
        top = new_y
        bottom = new_y + enemy_size
        
        # Converte para índices de grid
        col_left = (left - self.offset_x) // TILE_SIZE
        col_right = (right - self.offset_x - 1) // TILE_SIZE
        row_top = (top - self.offset_y) // TILE_SIZE
        row_bottom = (bottom - self.offset_y - 1) // TILE_SIZE
        
        # Verifica se está fora dos limites
        if col_left < 0 or col_right >= GRID_WIDTH or row_top < 0 or row_bottom >= GRID_HEIGHT:
            return True
        
        # Verifica todas as células que o inimigo ocupa
        for row in range(max(0, row_top), min(GRID_HEIGHT, row_bottom + 1)):
            for col in range(max(0, col_left), min(GRID_WIDTH, col_right + 1)):
                if game_map[row][col] == BLOCK_WALL or game_map[row][col] == BLOCK_BRICK:
                    return True
        
        return False
    
    def _check_bomb_collision(self, new_x, new_y, bombs):
        """Verifica colisão com bombas sólidas"""
        # Tamanho do inimigo
        enemy_size = TILE_SIZE - 4
        
        # Rect do inimigo na nova posição
        enemy_rect = pygame.Rect(new_x, new_y, enemy_size, enemy_size)
        
        # Verifica colisão com cada bomba sólida
        for bomb in bombs:
            if bomb.is_solid and enemy_rect.colliderect(bomb.rect):
                return True
        
        return False
    
    def draw(self, surface:pygame.surface)->None:
        surface.blit(self.image, self.rect)