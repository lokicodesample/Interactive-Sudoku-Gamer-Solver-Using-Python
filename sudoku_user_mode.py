import pygame
import numpy as np
from copy import deepcopy

# Initialize pygame
pygame.init()

# Screen setup for 700x500
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Game - User Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (99, 200, 167)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
HOVER_COLOR = (220, 220, 220)

# Fonts
font = pygame.font.Font(None, 30)

# Size variables
cell_size = 50
offset_x, offset_y = 20, 20  # Offset to center board in 700x500


# Function to check if the board is valid
def is_valid_board(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0
                if not is_valid(board, row, col, num):
                    board[row][col] = num  # Restore the value before returning
                    return False
                board[row][col] = num
    return True


# Function to check if placing a number is valid
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x, box_y = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[box_x + i][box_y + j] == num:
                return False
    return True


# Function to solve Sudoku using backtracking
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


# Main menu function
def main_menu():
    menu_running = True

    while menu_running:
        screen.fill(WHITE)

        # Display the title
        title_text = font.render("Sudoku Game", True, BLACK)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

        # Create Start Game button
        start_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2, 150, 50)
        pygame.draw.rect(screen, GREEN, start_button)
        start_text = font.render("Start Game", True, BLACK)
        text_rect_start = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, text_rect_start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    menu_running = False  # Exit menu and start the game

        pygame.display.flip()

    start_game()


# Start the game with a new board
def start_game():
    initial_board = [[0] * 9 for _ in range(9)]
    solved_board = deepcopy(initial_board)

    # Game loop
    running = True
    dragging = False
    selected_num = None
    mouse_x, mouse_y = 0, 0
    solution_found = False
    invalid_board = False

    while running:
        screen.fill(WHITE)

        # Draw Sudoku grid with empty cells clearly visible
        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(offset_x + col * cell_size, offset_y + row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, LIGHT_BLUE if (row // 3 + col // 3) % 2 == 0 else WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if initial_board[row][col] != 0:
                    num_text = font.render(str(initial_board[row][col]), True, BLACK)
                    screen.blit(num_text, (offset_x + col * cell_size + 15, offset_y + row * cell_size + 10))

        # Display draggable number buttons from 1 to 9 in a 2x5 grid format
        for i in range(1, 10):
            row = (i - 1) // 2
            col = (i - 1) % 2
            x_pos = screen_width - 160 + col * 60
            y_pos = offset_y + 30 + row * 50  # Adjusted y position for buttons
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

        # Draw Find Solution button below number buttons
        find_solution_button = pygame.Rect(screen_width - 190, offset_y + 300, 155, 40)
        pygame.draw.rect(screen, GREEN if is_valid_board(initial_board) else RED, find_solution_button)
        solution_text = font.render(" Find Solution", True, BLACK)
        text_rect_solution = solution_text.get_rect(center=find_solution_button.center)
        screen.blit(solution_text, text_rect_solution)

        # Draw Exit button below Find Solution button
        exit_button = pygame.Rect(screen_width - 170, offset_y + 350, 120, 40)
        pygame.draw.rect(screen, GRAY, exit_button)
        exit_text = font.render("Exit", True, BLACK)
        text_rect_exit = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, text_rect_exit)

        # Handle dragging and dropping numbers into empty cells
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if a number button is clicked to start dragging
                for i in range(1, 10):
                    row = (i - 1) // 2  # Adjusted to match button layout
                    col = (i - 1) % 2
                    x_pos = screen_width - 160 + col * 60
                    y_pos = offset_y + 30 + row * 50
                    num_rect = pygame.Rect(x_pos - 15, y_pos - 15, 50, 50)
                    if num_rect.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        selected_num = i
                        break
                # Check if Find Solution button is clicked
                if find_solution_button.collidepoint(mouse_x, mouse_y):
                    if is_valid_board(initial_board):
                        solution_board = deepcopy(initial_board)
                        solution_found = solve_sudoku(solution_board)
                        if solution_found:
                            solved_board = solution_board
                        else:
                            print("No solution exists")
                    else:
                        invalid_board = True
                # Check if Exit button is clicked
                if exit_button.collidepoint(mouse_x, mouse_y):
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_num is not None:
                    dragging = False
                    grid_x = (mouse_x - offset_x) // cell_size
                    grid_y = (mouse_y - offset_y) // cell_size
                    if 0 <= grid_x < 9 and 0 <= grid_y < 9:
                        # Update the board with the selected number, replacing any existing value
                        initial_board[grid_y][grid_x] = selected_num
                    selected_num = None
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()

        # Display solution if found
        if solution_found:
            for row in range(9):
                for col in range(9):
                    if solved_board[row][col] != 0:
                        # Use the same font and color as user-entered numbers
                        num_text = font.render(str(solved_board[row][col]), True, BLACK)
                        screen.blit(num_text, (offset_x + col * cell_size + 15, offset_y + row * cell_size + 10))
        elif invalid_board:
            invalid_text = font.render("Invalid Board!", True, RED)
            screen.blit(invalid_text, (screen_width // 2 - invalid_text.get_width() // 2, screen_height // 2))

        pygame.display.flip()

    pygame.quit()


# Start the application
if __name__ == "__main__":
    main_menu()
