import pygame
import sys
import sudoku_game
import sudoku_user_mode
#from sudoku_user_mode import start_game  # Import the user mode script

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
mode = "menu"
difficulty_blanks = 2 # Default difficulty (Easy)

# Function to display the main menu
def display_main_menu():
    screen.fill(WHITE)
    title_text = font.render("Sudoku Game", True, BLACK)
    mode1_text = font.render("1. Start Game", True, BLACK)
    mode2_text = font.render("2. User Mode", True, BLACK)
    exit_text = font.render("3. Exit", True, BLACK)

    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
    screen.blit(mode1_text, (screen_width // 2 - mode1_text.get_width() // 2, 150))
    screen.blit(mode2_text, (screen_width // 2 - mode2_text.get_width() // 2, 200))
    screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 250))

# Function to display the difficulty menu
def display_difficulty_menu():
    screen.fill(WHITE)
    title_text = font.render("Select Difficulty", True, BLACK)
    easy_text = font.render("1. Easy", True, BLACK)
    medium_text = font.render("2. Medium", True, BLACK)
    hard_text = font.render("3. Hard", True, BLACK)
    back_text = font.render("4. Back to Main Menu", True, BLACK)

    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
    screen.blit(easy_text, (screen_width // 2 - easy_text.get_width() // 2, 150))
    screen.blit(medium_text, (screen_width // 2 - medium_text.get_width() // 2, 200))
    screen.blit(hard_text, (screen_width // 2 - hard_text.get_width() // 2, 250))
    screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, 300))

# Function to exit the game after a delay
def exit_game_with_delay(message, delay=500):
    print(message)  # Print the selected difficulty

    # Display the goodbye message
    screen.fill(WHITE)
    goodbye_text = font.render("Goodbye!", True, BLACK)
    screen.blit(goodbye_text, (screen_width // 2 - goodbye_text.get_width() // 2, screen_height // 2 - goodbye_text.get_height() // 2))
    pygame.display.flip()  # Update the display
    pygame.time.delay(2000)  # Show goodbye message for 2 seconds

    pygame.quit()  # Clean up and close the window
    sys.exit()  # Exit the program

# Game loop
running = True
while running:
    if mode == "menu":  # Main menu
        display_main_menu()
    elif mode == "difficulty":  # Difficulty selection
        display_difficulty_menu()
    elif mode == "user_mode":  # User mode
        print("User mode is selected")
        sudoku_user_mode.start_game()  # Call the function from the us.py file

    pygame.display.flip()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mode == "menu":  # Main menu interaction
                if 150 < mouse_y < 180:  # Start Game
                    mode = "difficulty"
                elif 200 < mouse_y < 230:  # User Mode
                    mode = "user_mode"  # Switch to user mode
                elif 250 < mouse_y < 280:  # Exit
                    running = False
            elif mode == "difficulty":  # Difficulty selection
                if 150 < mouse_y < 180:
                    # Easy
                    sudoku_game.start_game("Easy")
                    exit_game_with_delay("Selected Difficulty: Easy")  # Print and exit
                elif 200 < mouse_y < 230:

                    sudoku_game.start_game("Medium")
                    exit_game_with_delay("Selected Difficulty: Medium")  # Print and exit
                elif 250 < mouse_y < 280:

                    sudoku_game.start_game("Hard")
                    exit_game_with_delay("Selected Difficulty: Hard")  # Print and exit
                elif 300 < mouse_y < 330:  # Back to Main Menu
                    mode = "menu"

pygame.quit()
