from constants import ROWS, COLS, BLACK

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        if BLACK not in grid[i]:
            increment += 1
            for j in range(len(grid[i])):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        new_locked = {}
        for (x, y), color in locked.items():
            new_y = y + increment if y < i else y
            new_locked[(x, new_y)] = color
        locked.clear()
        locked.update(new_locked)
    return increment

def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(COLS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_positions = [pos for sub in accepted_positions for pos in sub]
    shape_pos = []
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                shape_pos.append((piece.x + j, piece.y + i))
    for pos in shape_pos:
        if pos not in accepted_positions:
            if pos[1] >= 0:
                return False
    return True

def check_lost(positions):
    for _, y in positions:
        if y < 1:
            return True
    return False
