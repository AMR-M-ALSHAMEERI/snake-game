# File: /snake-game/snake-game/src/snake_game.py

#IMPORT NECESSARY LIBRARIES
import random
import curses
import time

def welcome_screen(window):
    window.clear()
    window.border(0)
    screenHeight, screenWidth = window.getmaxyx()

    # ASCII Art Title
    title = [
        "  _____             _        ",
        " / ____|           | |       ",
        "| (___   ___   ___ | | _____ ",
        " \\___ \\ / _ \\ / _ \\| |/ / _ \\",
        " ____) | (_) | (_) |   <  __/",
        "|_____/ \\___/ \\___/|_|\\_\\___|",
        "",
        "         S N A K E   G A M E "
    ]

    min_height = 20
    min_width = 40
    if screenHeight < min_height or screenWidth < min_width:
        msg = "Please resize your terminal window!"
        window.addstr(screenHeight // 2, (screenWidth - len(msg)) // 2, msg)
        window.refresh()
        window.getch()
        return False

    # Color for title if supported
    if curses.has_colors():
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        title_color = curses.color_pair(3)
    else:
        title_color = 0

    # Draw ASCII art centered
    for idx, line in enumerate(title):
        y = screenHeight // 2 - 8 + idx
        x = max(0, (screenWidth - len(line)) // 2)
        if 0 <= y < screenHeight:
            window.addstr(y, x, line[:screenWidth], title_color)

    # Add developer name and version below the title
    dev_info = "Developed by AMR | Version 2.0"
    y_info = screenHeight // 2 + 1
    x_info = max(0, (screenWidth - len(dev_info)) // 2)
    if 0 <= y_info < screenHeight:
        window.addstr(y_info, x_info, dev_info, title_color | curses.A_BOLD)

    # Interactive menu
    options = ["Start", "Quit"]
    selected = 0

    while True:
        # Draw options
        for i, option in enumerate(options):
            y = screenHeight // 2 + 2 + i
            x = max(0, (screenWidth - len(option)) // 2)
            attr = curses.A_REVERSE | title_color if i == selected else title_color
            if 0 <= y < screenHeight:
                window.addstr(y, x, option[:screenWidth], attr)
        window.refresh()

        key = window.getch()
        if key in [curses.KEY_UP, ord('w')]:
            selected = (selected - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord('s')]:
            selected = (selected + 1) % len(options)
        elif key in [curses.KEY_ENTER, 10, 13]:
            return selected == 0
        elif key == ord('q'):
            return False

def display_score(window, score, high_score, screenWidth):
    score_text = f"Score: {score}   High Score: {high_score}"
    window.addstr(0, (screenWidth - len(score_text)) // 2, score_text)

def place_food(snake, screenHeight, screenWidth):
    while True:
        food = [
            random.randint(1, screenHeight - 2),
            random.randint(1, screenWidth - 2)
        ]
        if food not in snake:
            return food

def instructions_screen(window):
    window.clear()
    window.border(0)
    instructions = [
        "How to Play Snake:",
        "",
        "Use arrow keys to move the snake.",
        "Eat the diamonds to grow and score points.",
        "Don't hit the walls or yourself!",
        "",
        "Press 'p' to pause/resume.",
        "Press 'q' after Game Over to quit.",
        "",
        "Press 's' to Start or 'q' to Quit..."
    ]
    screenHeight, screenWidth = window.getmaxyx()
    for idx, line in enumerate(instructions):
        window.addstr(screenHeight // 2 - len(instructions) // 2 + idx, (screenWidth - len(line)) // 2, line)
    window.refresh()
    while True:
        key = window.getch()
        if key == ord('s'):
            return True
        elif key == ord('q'):
            return False

def fancy_game_over(window, screenHeight, screenWidth):
    window.clear()
    window.border(0)
    # ASCII Art for Game Over
    game_over_art = [
        "   _____                         ____                 ",
        "  / ____|                       / __ \\                ",
        " | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ",
        " | | |_ |/ _` | '_ ` _ \\ / _ \\ | |  | \\ \\ / / _ \\ '__|",
        " | |__| | (_| | | | | | |  __/ | |__| |\\ V /  __/ |   ",
        "  \\_____|\\__,_|_| |_| |_|\\___|  \\____/  \\_/ \\___|_|   ",
        "",
        "      Press 's' to Start Again or 'q' to Quit"
    ]
    # Color for Game Over if supported
    if curses.has_colors():
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        art_color = curses.color_pair(4)
    else:
        art_color = 0

    # Animate the Game Over message moving from left to center
    for offset in range(-40, (screenWidth - len(game_over_art[0])) // 2 + 1, 2):
        window.clear()
        window.border(0)
        for idx, line in enumerate(game_over_art):
            y = screenHeight // 2 - len(game_over_art) // 2 + idx
            x = max(0, offset)
            if 0 <= y < screenHeight:
                window.addstr(y, x, line[:screenWidth], art_color)
        window.refresh()
        time.sleep(0.03)

    # Wait for user to choose
    while True:
        window.refresh()
        key = window.getch()
        if key == ord('q'):
            curses.endwin()
            quit()
        elif key == ord('s'):
            window.clear()
            window.border(0)
            break

def main(stdscr):
    #INITIALIZE THE CURSES LIBRARY TO CREATE THE SCREEN
    screen = stdscr

    #HIDE THE CURSOR
    curses.curs_set(0)

    #GET MAX HEIGHT AND WIDTH OF THE SCREEN
    screenHeight, screenWidth = screen.getmaxyx()

    #CREATE A NEW WINDOW FOR THE GAME
    window = curses.newwin(screenHeight, screenWidth, 0, 0)

    #ALLOW KEYBOARD TO RECEIVE USER INPUT
    window.keypad(1)

    #SET THE DELAY FOR UPDATING THE SCREEN
    window.timeout(120)

    # Show welcome screen
    if not welcome_screen(window):
        curses.endwin()
        return

    # Show instructions screen and let player decide
    if not instructions_screen(window):
        curses.endwin()
        return

    high_score = 0  # Track high score

    # Initialize color pairs if supported
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Snake color (changed to yellow)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food color

    while True:  # Allow restarting the game
        # Recalculate window size in case it changed
        screenHeight, screenWidth = window.getmaxyx()

        # Ensure snake starts inside the border
        safe_x = max(2, min(screenWidth - 3, screenWidth // 4))
        safe_y = max(2, min(screenHeight - 3, screenHeight // 2))
        snake = [[safe_y, safe_x], [safe_y, safe_x - 1], [safe_y, safe_x - 2]]
        food_location = place_food(snake, screenHeight, screenWidth)
        key = curses.KEY_RIGHT
        score = 0
        game_over = False

        base_timeout = 120  # Initial speed (ms)
        min_timeout = 40    # Fastest speed (ms)

        window.clear()
        window.border(0)  # Draw border ONCE at the start of each game

        while not game_over:
            # Increase speed as score increases
            speed = max(min_timeout, base_timeout - score * 5)
            window.timeout(speed)

            # DO NOT clear or redraw border here!
            display_score(window, score, high_score, screenWidth)

            next_key = window.getch()
            key = key if next_key == -1 else next_key

            # Pause feature
            if key == ord('p'):
                window.addstr(screenHeight // 2, (screenWidth - len("Paused - Press 'p' to resume")) // 2, "Paused - Press 'p' to resume")
                window.refresh()
                while True:
                    pause_key = window.getch()
                    if pause_key == ord('p'):
                        break

            if (snake[0][0] in [0, screenHeight - 1] or
                snake[0][1] in [0, screenWidth - 1] or
                snake[0] in snake[1:]):
                game_over = True
                if score > high_score:
                    high_score = score
                fancy_game_over(window, screenHeight, screenWidth)
                # After break, game restarts

            #SET THE NEW SNAKE'S HEAD POSITION BASED ON THE DIRECTION
            new_head = [snake[0][0], snake[0][1]]
            if key == curses.KEY_DOWN:
                new_head[0] += 1
            if key == curses.KEY_UP:
                new_head[0] -= 1
            if key == curses.KEY_RIGHT:
                new_head[1] += 1
            if key == curses.KEY_LEFT:
                new_head[1] -= 1

            snake.insert(0, new_head)

            if snake[0] == food_location:
                score += 1
                food_location = place_food(snake, screenHeight, screenWidth)
                # Draw food at new location
                if curses.has_colors():
                    window.addch(food_location[0], food_location[1], curses.ACS_DIAMOND, curses.color_pair(2))
                else:
                    window.addch(food_location[0], food_location[1], curses.ACS_DIAMOND)
            else:
                tail = snake.pop()
                window.addch(tail[0], tail[1], ' ')

            # Draw food every frame at its current location as a small box/square
            if curses.has_colors():
                window.addch(food_location[0], food_location[1], curses.ACS_BLOCK, curses.color_pair(2))  # ACS_BLOCK is a solid square
            else:
                window.addch(food_location[0], food_location[1], curses.ACS_BLOCK)

            # Draw only the changed parts for the snake
            if 1 <= snake[0][0] < screenHeight - 1 and 1 <= snake[0][1] < screenWidth - 1:
                if curses.has_colors():
                    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD, curses.color_pair(1))
                else:
                    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

            window.refresh()

if __name__ == "__main__":
    curses.wrapper(main)