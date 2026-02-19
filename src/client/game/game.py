import pygame
import sys
from public.settings import *
from .player import Player

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
        pygame.display.set_caption(SCREEN_TITLE)
        self.running = True
        self.screen:pygame.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock:pygame.time = pygame.time.Clock()
        self.font:pygame.font = pygame.font.SysFont("Arial", 30)
        
        # --- Inicializando o menu ---
        self.menu_running = True
        self.menu_index = 0 #0: offline, 1: online
        self.menu_options = ["Offline", "Online (Beta)","Sair"]
        self.pulse_strength = 0
        self.pulse_direction = 1
    
        # --- Player e afins ---
        self.player:Player = Player((0,0),(255,255,255)) #inicializando Zerado
        self.map_data:list = None
        
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
    
    def close(self):
        self.running = False
    
    
    def _events(self):
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
                            print("offline")
                        elif self.menu_index == 1 :# online
                            print("online")
                        elif self.menu_index == 2 :# sair
                            self.close()
                        