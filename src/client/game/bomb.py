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
        self.spawn_time = pygame.time.get_ticks()
        self.explosion_area_images = {
            "center":    self._get_sprite(self.sheet, 30, 175, 18, 18, 2), # Centro da explosão
            
            # Meios (Usados quando o max_range é maior que 1)
            "mid_v":     self._get_sprite(self.sheet, 30, 157, 18, 18, 2), # Meio Vertical
            "mid_h":     self._get_sprite(self.sheet, 48, 175, 18, 18, 2), # Meio Horizontal
            
            # Pontas (Finais da explosão)
            "tip_up":    self._get_sprite(self.sheet, 30, 139, 18, 18, 2), # Ponta Cima
            "tip_down":  self._get_sprite(self.sheet, 30, 193, 18, 18, 2), # Ponta Baixo
            "tip_left":  self._get_sprite(self.sheet, 12, 175, 18, 18, 2), # Ponta Esquerda
            "tip_right": self._get_sprite(self.sheet, 66, 175, 18, 18, 2)  # Ponta Direita
        }
        self.image = self.explosion_area_images["center"]
        self.rect = self.image.get_rect(center=self.pos)
        self.range = {"up": 0, "right": 0, "down": 0, "left": 0}
        self.level = level
        self.expired = False
        self._get_range()
        self._calculate_propagation(grid, self.level)
        


    

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

    
    def _calculate_propagation(self, grid:list, max_range: int):
        """Calculates the propagation of the explosion, did this and had a bug,
        need more logical thinking
        
        # - directions
        

        Args:
            grid (_type_): _description_
            max_range (int): _description_
        """
        
        directions = {
            "up":(0,-1),
            "down":(0,1),
            "left":(-1,0),
            "right":(1,0)
        }
       
        
        gx = int((self.pos[0]- OFFSET_X) // TILE_SIZE)
        gy = int((self.pos[1]- OFFSET_Y) // TILE_SIZE)
        
        for direction, (dx, dy) in directions.items():
            self.range[direction] = 0
            
            for step in range(1, max_range + 1):
                tx = gx + (dx * step)
                ty = gy + (dy * step)
                
                # 2. Verifica limites: ty (linhas) e tx (colunas)
                if 0 <= ty < len(grid) and 0 <= tx < len(grid[0]):
                    tile = grid[ty][tx] # RIGOROSAMENTE grid[linha][coluna]
                    
                    # 3. Compara os valores
                    if tile == BLOCK_WALL:
                        break 
                    
                    self.range[direction] = step
                    
                    if tile == BLOCK_BRICK:
                        # 4. Remove o bloco usando a mesma lógica de índice do mapa
                        grid[ty][tx] = BLOCK_EMPTY 
                        break 
                else:
                    break
            
        
    
    
    def draw(self, surface:pygame.surface)->None:
        # 1. Desenha o centro da explosão
        surface.blit(self.explosion_area_images["center"],self.pos)

        # 2. Percorre as 4 direções para desenhar as pontas da explosão
        for direction, distance in self.range.items():
            if distance == 0:
                continue
            
            for a in range(1,distance+1):
                dx,dy = 0,0
                
                if direction == "up":
                    dy = -a * TILE_SIZE
                elif direction == "down":
                    dy = a * TILE_SIZE
                elif direction == "left":
                    dx = -a * TILE_SIZE
                elif direction == "right":
                    dx = a * TILE_SIZE
                
                draw_pos = (self.pos[0] + dx, self.pos[1] + dy)
                
                # 3 Define se vai usar o meio ou a ponta da explosão
                if a == distance:
                    img_key = f"tip_{direction}"
                    surface.blit(self.explosion_area_images[img_key], draw_pos)
                else:
                    if direction in ["up", "down"]:
                        surface.blit(self.explosion_area_images[f"mid_h"], draw_pos)
                    else:
                        surface.blit(self.explosion_area_images[f"mid_v"], draw_pos)
                    
        
    def update(self,grid:list)->None:
        now = pygame.time.get_ticks()
        time_passed = now - self.spawn_time
        
        
        if time_passed >= self.duration:
            self.expired = True
        
            