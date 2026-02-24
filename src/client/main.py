import sys
import os


# Add the path for the game
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from game import Game


game = Game()
game.run()