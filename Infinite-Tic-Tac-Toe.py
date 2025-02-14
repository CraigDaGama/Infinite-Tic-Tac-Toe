import pygame
from collections import deque

pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 3 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Tic-Tac-Toe")

# Colors
WHITE = (240, 240, 240)
BLACK = (50, 50, 50)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 8
BORDER_COLOR = (30, 30, 30)

# Game variables
moves = {}  # Dictionary to store moves {(x, y): 'X' or 'O'}
history = deque(maxlen=6)  # Keep track of last 6 moves
current_player = "X"
running = True

font = pygame.font.Font(None, 120)
small_font = pygame.font.Font(None, 50)

def draw_grid():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), 10, border_radius=20)  # Border with rounded corners
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)

def draw_moves():
    for (gx, gy), player in moves.items():
        text = font.render(player, True, RED if player == 'X' else BLUE)
        text_rect = text.get_rect(center=((gx + 0.5) * CELL_SIZE, (gy + 0.5) * CELL_SIZE))
        screen.blit(text, text_rect)

def check_win():
    for (x, y), player in moves.items():
        if (
            all(moves.get((x + i, y)) == player for i in range(3)) or  
            all(moves.get((x, y + i)) == player for i in range(3)) or 
            all(moves.get((x + i, y + i)) == player for i in range(3)) or 
            all(moves.get((x + i, y - i)) == player for i in range(3)) 
        ):
            return player
    return None

def show_popup(winner):
    screen.fill(WHITE)
    message = f"{winner} Wins!"
    text = small_font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)
    
    button_width, button_height = 150, 50
    button_spacing = 50
    total_width = (2 * button_width) + button_spacing
    start_x = (WIDTH - total_width) // 2
    
    pygame.draw.rect(screen, RED, (start_x, HEIGHT // 2, button_width, button_height))
    pygame.draw.rect(screen, BLUE, (start_x + button_width + button_spacing, HEIGHT // 2, button_width, button_height))
    
    play_again_text = small_font.render("Replay", True, WHITE)
    quit_text = small_font.render("Quit", True, WHITE)
    
    screen.blit(play_again_text, (start_x + 25, HEIGHT // 2 + 10))
    screen.blit(quit_text, (start_x + button_width + button_spacing + 50, HEIGHT // 2 + 10))
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if WIDTH // 4 - 50 <= mx <= WIDTH // 4 + 100 and HEIGHT // 2 <= my <= HEIGHT // 2 + 50:
                    return True  
                elif WIDTH // 2 + 100 <= mx <= WIDTH // 2 + 250 and HEIGHT // 2 <= my <= HEIGHT // 2 + 50:
                    pygame.quit()
                    exit()
    return False

while running:
    screen.fill(WHITE)
    draw_grid()
    draw_moves()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            gx = mx // CELL_SIZE
            gy = my // CELL_SIZE
            if (gx, gy) not in moves:
                moves[(gx, gy)] = current_player
                history.append((gx, gy))
                if len(history) == 6:
                    oldest_move = history.popleft()
                    moves.pop(oldest_move, None)
                winner = check_win()
                if winner:
                    if show_popup(winner):
                        moves.clear()
                        history.clear()
                        current_player = "X"
                    else:
                        running = False
                current_player = "O" if current_player == "X" else "X"
    
    pygame.display.flip()

pygame.quit()
