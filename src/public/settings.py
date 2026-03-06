# ===============================================================================
# TH SISTEMAS - CONFIGURACOES GERAIS -
# Sinta-se a vontade para modificar ao seu bel-prazer
# ===============================================================================
import pathlib
# --- DIMENSOES DA ARENA ---
TILE_SIZE = 48        # Tamanho de cada quadrado (em pixels)
GRID_WIDTH = 15       # Numero de colunas (Sempre impar para o design clássico)
GRID_HEIGHT = 13      # Numero de linhas (Sempre impar)
BLOCK_EMPTY = 0
BLOCK_WALL = 1
BLOCK_BRICK = 2


# --- DIMENSOES DA TELA ---
SCREEN_WIDTH = 1200#TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = 800#TILE_SIZE * GRID_HEIGHT
SCREEN_TITLE = "Bomberman - TH Sistemas"
MAP_PIXEL_WIDTH = TILE_SIZE * GRID_WIDTH
MAP_PIXEL_HEIGHT = TILE_SIZE * GRID_HEIGHT
OFFSET_X = (SCREEN_WIDTH - MAP_PIXEL_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - MAP_PIXEL_HEIGHT) // 2

# --- CORES RGB ---
COLOR_BG = (54, 53, 53)      # Fundo Escuro
COLOR_WALL = (240, 247, 243)    # Parede Indestrutivel
COLOR_BRICK = (100, 100, 100)  # Tijolo Destrutivel
COLOR_PLAYER = (0, 255, 0)   # Verde Alquimista
COLOR_BOMB = (255, 0, 0)     # Vermelho Perigo

# --- LOGICA DE JOGO ---
FPS = 60                     # Frames por segundo
BOMB_TIMER = 3000            # Milissegundos para explodir (3 seg)
PLAYER_SPEED = 4            # Pixels por frame
ENEMY_SPEED = 2             # Pixels por frame
ENEMIES = 4                 # Quantidade de inimigos na arena
MUSIC_GAME ="src/assets/MrCrowley8Bits.mp3"
MUSIC_VOLUME = 0.5
