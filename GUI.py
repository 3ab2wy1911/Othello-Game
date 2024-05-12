# Implement the pygame GUI for the application
import pygame
from src.Board import Board
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Set up the window
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Othello")

# Load tile sprites
empty_tile_unscaled = pygame.image.load("Images/Empty Tile.bmp")
black_tile_unscaled = pygame.image.load("Images/Black Tile.bmp")
white_tile_unscaled = pygame.image.load("Images/White Tile.bmp")
open_tile_unscaled = pygame.image.load("Images/Open Tile.bmp")
hover_tile_unscaled = pygame.image.load("Images/Hover Tile.bmp")
hover_white_tile_unscaled = pygame.image.load("Images/Hover White Tile.bmp")
hover_black_tile_unscaled = pygame.image.load("Images/Hover Black Tile.bmp")
hover_open_tile_unscaled = pygame.image.load("Images/Hover Open Tile.bmp")

# Setup tiles
tile_size = int(WINDOW_SIZE / 8)
empty_tile = pygame.transform.scale(empty_tile_unscaled, (tile_size, tile_size))
black_tile = pygame.transform.scale(black_tile_unscaled, (tile_size, tile_size))
white_tile = pygame.transform.scale(white_tile_unscaled, (tile_size, tile_size))
open_tile = pygame.transform.scale(open_tile_unscaled, (tile_size, tile_size))
hover_tile = pygame.transform.scale(hover_tile_unscaled, (tile_size, tile_size))
hover_white_tile = pygame.transform.scale(hover_white_tile_unscaled, (tile_size, tile_size))
hover_black_tile = pygame.transform.scale(hover_black_tile_unscaled, (tile_size, tile_size))
hover_open_tile = pygame.transform.scale(hover_open_tile_unscaled, (tile_size, tile_size))
board = Board().board

# Piece sound
move_sound = pygame.mixer.Sound("Sounds/Piece_Sound.wav")


# NOTE: the (x, y) points are reversed in pygame, where (x) is columns and (y) is rows
# For updating the board sprites
def draw_board(boardc):
    board = boardc
    pos = pygame.mouse.get_pos()
    x = pos[0] // tile_size
    y = pos[1] // tile_size

    for i in range(8):
        for j in range(8):
            # For hover
            if i == x and j == y and board[i][j] == 0:
                screen.blit(hover_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 1:
                screen.blit(hover_black_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 2:
                screen.blit(hover_white_tile, (i * tile_size, j * tile_size))
            elif i == x and j == y and board[i][j] == 3:
                screen.blit(hover_open_tile, (i * tile_size, j * tile_size))
            
            # For normal tiles
            elif board[i][j] == 0:
                screen.blit(empty_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 1:
                screen.blit(black_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 2:
                screen.blit(white_tile, (i * tile_size, j * tile_size))
            elif board[i][j] == 3:
                screen.blit(open_tile, (i * tile_size, j * tile_size))
    pygame.display.flip()


# This detects all the valid moves you can make based on your turn
def detect_valid_moves(turn, board):
    # This clears all the previously assigned valid moves so we can detect new ones
    for i in range(8):
        for j in range(8):
            if board[i][j] == 3:
                    board[i][j] = 0
    
    # This detects the valid moves and assigns them (Must be in a straight line)
    reverse_turn = 2 if turn == 1 else 1
    for i in range(8):
        for j in range(8):
            if board[i][j] == reverse_turn:
                if i < 7 and board[i + 1][j] == 0 and board[i - 1][j] == turn: # Check down
                    board[i + 1][j] = 3
                if j < 7 and board[i][j + 1] == 0 and board[i][j - 1] == turn: # Check right
                    board[i][j + 1] = 3
                if i > 0 and board[i - 1][j] == 0 and board[i + 1][j] == turn: # Check up
                    board[i - 1][j] = 3
                if j > 0 and board[i][j - 1] == 0 and board[i][j + 1] == turn: # Check left
                    board[i][j - 1] = 3


screen.fill((255, 255, 255))
running = True
turn = 1

# Main loop
while running:
    for event in pygame.event.get():
        detect_valid_moves(turn, board)
        draw_board(board)

        pos = pygame.mouse.get_pos()
        x = pos[0] // tile_size
        y = pos[1] // tile_size

        # Closing the game
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and board[x][y] == 3:
            # Adding new pieces
            if turn == 1:
                board[x][y] = 1
                turn = 2
            elif turn == 2:
                board[x][y] = 2
                turn = 1
                
            move_sound.play()
            print(x, y)
            
    pygame.display.flip()