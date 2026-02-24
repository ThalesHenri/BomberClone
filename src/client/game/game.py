import pygame
import sys
from public.settings import *
from .player import Player
import random
from .bomb import Bomb

"""
Este script deve ter:

- Classe que represente o jogo
- Esta classe vai:
    - Iniciar o jogo
    - Atualizar o jogo
    - Renderizar o jogo 
    - Lidar com os eventos do jogo
    - Finalizar o jogo
    


"""

class Game:
    def __init__(self):
        
        # --- Inicializando o jogo ---
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(SCREEN_TITLE)
        pygame.mixer_music.load(MUSIC_GAME)
        self.running = True
        self.match_running = False
        self.screen:pygame.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock:pygame.time = pygame.time.Clock()
        self.font:pygame.font = pygame.font.SysFont("Arial", 30)
        
        # --- Inicializando o mapa ---
        self.grid = None
        self.map_pixel_width = GRID_WIDTH * TILE_SIZE
        self.map_pixel_height = GRID_HEIGHT * TILE_SIZE
        self.offset_x = (SCREEN_WIDTH - self.map_pixel_width) // 2
        self.offset_y = (SCREEN_HEIGHT - self.map_pixel_height) // 2
        
        # --- Inicializando o menu ---
        self.menu_running = True
        self.menu_index = 0 #0: offline, 1: online
        self.menu_options = ["Offline", "Online (Beta)","Sair"]
        self.pulse_strength = 0
        self.pulse_direction = 1
    
        # --- Player e afins ---
        self.player:Player = Player((self.offset_x + 50, self.offset_y + 50),(255,0,0),(self.offset_x, self.offset_y)) #inicializando Zerado
        self.map_data:list = None
        self.bombs:list[Bomb] = []
        
    def run(self)->None:
        while self.running:
            self._update()
            self._render()
            self._events()
            self.clock.tick(FPS)
            
           
           
    def _menu_animations_math(self):
        self.pulse_strength += 0.05 * self.pulse_direction
        # Pulsação
        # Se a pulsação for maior que 1 ou menor que 0, inverte a direção
        if self.pulse_strength >= 1 or self.pulse_strength <= 0:
            self.pulse_direction *= -1
            
    def _update(self):
        pass    
    
    
    def _render(self):
        self.screen.fill(COLOR_BG)# fundo escuro
        # menu principal
        if self.menu_running: 
            # 1. Título Pulsante
            size = 60 + int(self.pulse_strength * 5)
            font_title = pygame.font.SysFont("Arial", size, bold=True)
            color = (255, 215 + int(40 * self.pulse_strength), 0)
            
            title_surf = font_title.render("BOMBERMAN", True, color)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 120))
            self.screen.blit(title_surf, title_rect)

            self._menu_animations_math()
                # renderiza as opções
            for i, option in enumerate(self.menu_options):
                color = (255, 255, 255) if i == self.menu_index else (255, 255, 0)
                option_text = self.font.render(option, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 50))
                option_surf = self.font.render(option, True, color)
                self.screen.blit(option_surf, option_rect)
            desc_surf = self.font.render("CLONE DO LENDÁRIO BOMBERMAN", True, (100, 100, 100))
            self.screen.blit(desc_surf, (SCREEN_WIDTH // 2 - desc_surf.get_width() // 2, SCREEN_HEIGHT - desc_surf.get_height() - 50)) # centraliza no rodapé
            pygame.display.flip()

        if self.match_running:
            self._draw_map(self.grid)
            self._draw_player()
            for bomb in self.bombs:
                bomb.draw(self.screen)
            
            pygame.display.flip()
            
        
    
    def close(self):
        self.running = False
        pygame.quit()
    
    
    def _events(self):
        # --- Lidar com os eventos globais ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if self.menu_running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                    
                    elif event.key in [pygame.K_SPACE, pygame.K_KP_ENTER]:
                        if self.menu_index == 0 :# offline
                            self.match_running = True
                            self.grid = self._generate_map()
                            self.menu_running = False
                        elif self.menu_index == 1 :# online
                            print("online")
                        elif self.menu_index == 2 :# sair
                            self.close()
        # --- Lidar com os eventos da partida ---
            if self.match_running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.grid = self._generate_map() 
                        self._render()
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                    if event.key == pygame.K_m:
                        pygame.mixer.music.stop()
                        self.match_running = False
                        self.menu_running = True
                    if event.key == pygame.K_b:
                        already_bomb = any([bomb.rect.topleft == (self.player.x, self.player.y) for bomb in self.bombs])
                        if already_bomb:
                            print("ja tem bomba")
                        else:
                            bomb = self.player.place_bomb()
                            if bomb:
                                self.bombs.append(bomb)
                                print("bomba colocada")
                                print(f"bomba colocada na posicao {self.player.x},{self.player.y} Numero da bomba- {self.player.bombs_placed}")
                        
                        
                                               
        # Dividndo para ficar mais legivel
       
        
        if self.match_running:
            direction = 0
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                direction = 3
                self.player.move(-1, 0,self.grid,direction)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                direction = 1
                self.player.move(1, 0,self.grid,direction)
            if pygame.key.get_pressed()[pygame.K_UP]:
                direction = 0
                self.player.move(0, -1,self.grid,direction)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                direction = 2
                self.player.move(0, 1,self.grid, direction)
                
                
                        


    def _draw_player(self):
        self.player.draw(self.screen)
                            
             
             
    def _draw_bomb(self):
       pass
    
                            
    def _generate_map(self) -> list:
    # 1. CRIAR A MATRIZ: Precisamos criar as sublistas primeiro!
    # Isso cria uma lista de listas preenchida com BLOCK_EMPTY
        grid = [[BLOCK_EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        # 2. PREENCHER O MAPA
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                # Paredes indestrutíveis (Bordas e Pilares)
                if row == 0 or row == GRID_HEIGHT - 1 or col == 0 or col == GRID_WIDTH - 1:
                    grid[row][col] = BLOCK_WALL
                elif row % 2 == 0 and col % 2 == 0:
                    grid[row][col] = BLOCK_WALL
                    
                # Tijolos destrutíveis (Lógica de chance e proteção dos cantos)
                else:
                    # Sua lógica de proteção dos 4 cantos está ótima!
                    nao_nos_cantos = not(
                        (row <= 2 and col <= 2) or 
                        (row >= GRID_HEIGHT - 3 and col <= 2) or 
                        (row <= 2 and col >= GRID_WIDTH - 3) or 
                        (row >= GRID_HEIGHT - 3 and col >= GRID_WIDTH - 3)
                    )
                    
                    if nao_nos_cantos:
                        if random.random() < 0.75:
                            grid[row][col] = BLOCK_BRICK
                    
        return grid

    def _draw_map(self, grid):
        self.screen.fill(COLOR_BG) 

        for row_index, row in enumerate(grid):
            for col_index, cell in enumerate(row):
                # A mágica acontece aqui: somamos o offset no X e no Y
                x = self.offset_x + (col_index * TILE_SIZE)
                y = self.offset_y + (row_index * TILE_SIZE)
                rect = (x, y, TILE_SIZE, TILE_SIZE)
                
                # Desenha o chão de grama para todas as células do grid
                # (Fica melhor do que desenhar grama só onde está vazio)
                pygame.draw.rect(self.screen, COLOR_BG, rect)

                if cell == BLOCK_WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                    pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                elif cell == BLOCK_BRICK:
                    pygame.draw.rect(self.screen, COLOR_BRICK, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)