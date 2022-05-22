from bfs import BFS
from pygame import gfxdraw

import numpy as np
import pygame
import random
import time
import os

pygame.init()

WIDTH, HEIGHT = 700, 800

BG_COLOR = 'white'
ROWS, COLS = 20, 20
BOMBS = 30
FIELDS_TO_UNCOVER = (ROWS * COLS) - BOMBS

SIZE = WIDTH // ROWS
NUM_FONT = pygame.font.SysFont('Arial', 20)
NUM_COLORS = {
    1: 'blue',
    2: (0, 100, 0),
    3: 'red',
    4: 'purple',
    5: 'brown',
    6: 'cyan',
    7: 'black',
    8: 'grey'
}

FLAGS_NUM_COLOS = 'green'
FLAGS_NUM_BG = 'black'
FLAGS_NUM_WIDTH = 100
FLAGS_NUM_HEIGHT = 80
FLAGS_WIN_XPOS = WIDTH - FLAGS_NUM_WIDTH - 10
FLAGS_WIN_YPOS = HEIGHT - FLAGS_NUM_HEIGHT - 10

RECT_COLOR = (111, 111, 111)
CLICKED_RECT_COLOR = (211, 211, 211)
FLAG_RECT_COLOR = 'red'
BOMB_RECT_COLOR = 'black'

# cover_field legend:
#  0 = covered
# -1 = uncovered
# -2 = flag
# -3 = bomb

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Some game")


def get_grid_pos(mouse_position):
    mx, my = mouse_position

    col = mx // SIZE
    row = my // SIZE

    return row, col


def create_grid(rows, cols, mines):
    field = np.zeros((rows, cols))
    mines_positions = set()

    while len(mines_positions) < mines:
        r, c = random.randint(0, ROWS-1), random.randint(0, COLS-1)

        if (r, c) in mines_positions:
            continue

        mines_positions.add((r, c))

        field[r][c] = -1

    for mine in mines_positions:
        neighbours = BFS.get_neighbours(*mine, rows, cols)

        for r, c in neighbours:
            if field[r][c] != -1:
                field[r][c] += 1

    return field, mines_positions


def draw_circle(surface, color, x, y, radius):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def draw(win: pygame.Surface, field: np.ndarray, cover_field: np.ndarray, flags_positions: set):
    win.fill(BG_COLOR)

    pygame.draw.rect(win, FLAGS_NUM_BG, (
        FLAGS_WIN_XPOS, FLAGS_WIN_YPOS, FLAGS_NUM_WIDTH, FLAGS_NUM_HEIGHT))

    flag_text = NUM_FONT.render(
        str(int(BOMBS - len(flags_positions))), 1, FLAGS_NUM_COLOS)

    win.blit(flag_text, (FLAGS_WIN_XPOS + (FLAGS_NUM_WIDTH / 2 - flag_text.get_width() / 2),
                         FLAGS_WIN_YPOS + (FLAGS_NUM_HEIGHT / 2 - flag_text.get_height() / 2)))

    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            is_flagged = cover_field[i][j] == -2
            is_bombed = cover_field[i][j] == -3

            if is_flagged:
                pygame.draw.rect(win, FLAG_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, 'black', (x, y, SIZE, SIZE), 2)
                continue

            if is_bombed:
                draw_circle(win, (0, 0, 0),
                            x + SIZE//2, y + SIZE//2, SIZE//2 - 5)
                pygame.draw.rect(win, 'black', (x, y, SIZE, SIZE), 2)
                continue

            if is_covered:
                pygame.draw.rect(win, RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, 'black', (x, y, SIZE, SIZE), 2)
                continue

            else:
                pygame.draw.rect(win, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(win, 'black', (x, y, SIZE, SIZE), 2)

            if value > 0:
                text = NUM_FONT.render(str(int(value)), 1, NUM_COLORS[value])
                win.blit(text, (x + (SIZE / 2 - text.get_width() / 2),
                                y + (SIZE / 2 - text.get_height() / 2)))

    pygame.display.update()


def uncover_fields(field, cover_field, row, col):
    value = field[row][col]
    if cover_field[row][col] == -2:
        pass
    elif value == 0:
        cover_field = BFS(field, cover_field, row, col, -1).uncover_fields()
    elif value == -1:
        cover_field = BFS(field, cover_field, row, col, -3).uncover_bombs()
    elif value > 0:
        cover_field[row][col] = -1

    return cover_field


def check_victory(mines_positions, flags_positions, cover_field):
    try:
        uncovered_dict = get_uncovered(cover_field)
        if mines_positions == flags_positions and uncovered_dict[-1] == FIELDS_TO_UNCOVER:
            return True
        return False
    except:
        return False


def get_uncovered(cover_field):
    unique, counts = np.unique(cover_field, return_counts=True)
    return dict(zip(unique, counts))


def check_flags(flags_positions: set, cover_field, mines_positions, row, col):
    flags = len(flags_positions)
    cf_value = int(cover_field[row][col])
    if cf_value == -2:
        flags_positions.remove((row, col))
        flags -= 1
        cover_field[row][col] = 0
    elif cf_value == -1:
        cover_field[row][col] = -1
    elif cf_value == 0:
        flags_positions.add((row, col))
        flags += 1
        cover_field[row][col] = -2

    return flags_positions, cover_field


def main():
    run = True
    field, mines_positions = create_grid(ROWS, COLS, BOMBS)
    cover_field = np.zeros((ROWS, COLS))

    flag_positions = set()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button = pygame.mouse.get_pressed()
                row, col = get_grid_pos(pygame.mouse.get_pos())
                if mouse_button[0]:
                    cover_field = uncover_fields(field, cover_field, row, col)
                elif mouse_button[2]:
                    flags_positions, cover_field = check_flags(
                        flag_positions, cover_field, mines_positions, row, col)

                victory = check_victory(
                    mines_positions, flag_positions, cover_field)
                if victory:
                    print("YOU WON!!!!!")
                # os.system('cls')
                #print(field, end='\n\n')
                # print(cover_field)

        draw(win, field, cover_field, flag_positions)


if __name__ == '__main__':
    main()
