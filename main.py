import pygame, random
from constants import WIDTH, HEIGHT, BLOCK_SIZE
from pieces import Piece, get_shape
from grid import create_grid, valid_space, clear_rows, check_lost
from draw import draw_window

pygame.init()

def convert_shape_format(piece):
    positions = []
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                positions.append((piece.x + j, piece.y + i))
    return positions

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
                score += clear_rows(grid, locked_positions) * 10
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

    pygame.quit()

if __name__ == "__main__":
    main()
