# sudoku_game.py
import pygame
from random import sample
from copy import deepcopy

# Initialize pygame
pygame.init()

# Screen setup
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (99, 200,167)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
HOVER_COLOR = (220, 220, 220)  # Color for hover effect on buttons

# Fonts
font = pygame.font.Font(None, 30)
win_font = pygame.font.Font(None, 60)

# Size variables
cell_size = 50
offset_x, offset_y = 30, 30

# Generate a random 9x9 Sudoku grid
def generate_sudoku():
    base = 3
    side = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    def shuffle(s): return sample(s, len(s))

    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, side + 1))
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

# Create a partial board with some cells set to 0 (blank)
def make_partial_board(board, blanks):
    partial_board = deepcopy(board)
    for _ in range(blanks):
        x, y = sample(range(9), 2)
        partial_board[x][y] = 0
    return partial_board

# Start the game with the selected difficulty level
def start_game(selected_difficulty):
    # Set the number of blanks based on difficulty level
    if selected_difficulty == 'Easy':
        blanks = 30
    elif selected_difficulty == 'Medium':
        blanks = 50
    else:  # Hard
        blanks = 65

    full_board = generate_sudoku()  # Generate the full solved board
    initial_board = make_partial_board(deepcopy(full_board), blanks)  # Create a playable board with blanks
    solved_board = deepcopy(initial_board)  # Initialize the player’s board

    # Helper functions
    def draw_grid():
        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, LIGHT_BLUE if (row // 3 + col // 3) % 2 == 0 else WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if initial_board[row][col] != 0:
                    num_text = font.render(str(initial_board[row][col]), True, BLACK)
                    screen.blit(num_text, (offset_x + col * cell_size + 15, offset_y + row * cell_size + 10))
                elif solved_board[row][col] != 0:
                    color = GREEN if solved_board[row][col] == full_board[row][col] else RED
                    num_text = font.render(str(solved_board[row][col]), True, color)
                    screen.blit(num_text, (offset_x + col * cell_size + 15, offset_y + row * cell_size + 10))

        # Draw thicker lines for 3x3 subgrids
        for i in range(0, 10, 3):
            pygame.draw.line(screen, BLACK, (offset_x, offset_y + i * cell_size),
                             (offset_x + 9 * cell_size, offset_y + i * cell_size), 2)
            pygame.draw.line(screen, BLACK, (offset_x + i * cell_size, offset_y),
                             (offset_x + i * cell_size, offset_y + 9 * cell_size), 2)

    def draw_buttons():
        # Display draggable number buttons from 1 to 9 in a 2x5 grid format
        for i in range(1, 10):
            row = (i - 1) // 2
            col = (i - 1) % 2
            x_pos = 540 + col * 60
            y_pos = 40 + row * 60
            num_text = font.render(str(i), True, BLACK)
            num_rect = pygame.Rect(x_pos - 15, y_pos - 15, 50, 50)

            # Highlight the button if hovered over
            if num_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, HOVER_COLOR, num_rect)
            else:
                pygame.draw.rect(screen, GRAY, num_rect)

            pygame.draw.rect(screen, BLACK, num_rect, 2)  # Border for each button
            # Center the text
            text_rect = num_text.get_rect(center=num_rect.center)
            screen.blit(num_text, text_rect)

    def check_win():
        for i in range(9):
            for j in range(9):
                if solved_board[i][j] != full_board[i][j]:
                    return False
        return True

    # Game loop
    running = True
    dragging = False
    selected_num = None
    mouse_x, mouse_y = 0, 0

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_buttons()

        # Display the dragged number if dragging
        if dragging and selected_num is not None:
            num_text = font.render(str(selected_num), True, RED)
            screen.blit(num_text, (mouse_x - 15, mouse_y - 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if a number button is clicked to start dragging
                for i in range(1, 10):
                    row = (i - 1) // 2
                    col = (i - 1) % 2
                    x_pos = 540 + col * 60
                    y_pos = 40 + row * 60
                    num_rect = pygame.Rect(x_pos - 15, y_pos - 15, 50, 50)
                    if num_rect.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        selected_num = i
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    if selected_num is not None:
                        # Calculate the grid cell where the number is dropped
                        grid_x = (mouse_x - offset_x) // cell_size
                        grid_y = (mouse_y - offset_y) // cell_size
                        # Place the number if in a valid cell
                        if 0 <= grid_x < 9 and 0 <= grid_y < 9 and initial_board[grid_y][grid_x] == 0:
                            solved_board[grid_y][grid_x] = selected_num
                            if check_win():
                                win_text = win_font.render("You Win!", True, GREEN)
                                screen.blit(win_text, (200, 220))
                                pygame.display.flip()
                                pygame.time.delay(5000)
                                running = False
                        selected_num = None
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()

        pygame.display.flip()

    pygame.quit()
