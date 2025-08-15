
import pygame, random
from constants import WIDTH, HEIGHT, BLOCK_SIZE, ROWS, COLS
from pieces import Piece, get_shape
from grid import create_grid, valid_space, clear_rows, check_lost
from draw import draw_window

pygame.init()
pygame.mixer.init()

# Musiqi və səs
pygame.mixer.music.load('assets/theme.mp3')
pygame.mixer.music.play(-1)
clear_sound = pygame.mixer.Sound('assets/clear.wav')

def convert_shape_format(piece):
    positions = []
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                positions.append((piece.x + j, piece.y + i))
    return positions

def draw_next_piece(surface, piece):
    font = pygame.font.SysFont('comicsans', 20)
    label = font.render("Next:", True, (255,255,255))
    surface.blit(label, (WIDTH + 10, 30))
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(surface, piece.color, (WIDTH + 10 + j*BLOCK_SIZE, 50 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    screen = pygame.display.set_mode((WIDTH+150, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_shape()
    next_piece = get_shape()
    run = True
    score = 0
    level = 1
    lines_cleared = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                cleared = clear_rows(grid, locked_positions)
                if cleared > 0:
                    score += cleared * 10
                    lines_cleared += cleared
                    clear_sound.play()
                    # Səviyyə artır
                    if lines_cleared >= level * 5:
                        level += 1
                        fall_speed *= 0.8
                current_piece = next_piece
                next_piece = get_shape()
                if check_lost(locked_positions):
                    print("Game Over!")
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                    if not valid_space(current_piece, grid):
                        current_piece.shape = [list(row) for row in zip(*current_piece.shape)][::-1]

        for pos in convert_shape_format(current_piece):
            x, y = pos
            if y >= 0:
                pygame.draw.rect(screen, current_piece.color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        draw_window(screen, grid, score)
        draw_next_piece(screen, next_piece)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
