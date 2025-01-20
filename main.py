import pygame
import os
import chess
import chess.engine
import sys

pygame.init()

# Get screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Set up the screen and frame rate
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Chess Game")

# Colors for UI elements
WHITE = (235, 236, 208)
BLACK = (115, 149, 82)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
TEXT_COLOR = (255, 255, 255)

# Chessboard setup (dynamic size based on screen)
BOARD_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 50
SQUARE_SIZE = BOARD_SIZE // 8
X_OFFSET = (SCREEN_WIDTH - BOARD_SIZE) // 2
Y_OFFSET = (SCREEN_HEIGHT - BOARD_SIZE) // 2

# Font for labels on the board
font = pygame.font.SysFont("Arial", 18)

# Path to the folder where piece images are stored
piece_image_path = "assets/pieces"

# Load piece images
def load_piece_images(color):
    return {
        "pawn": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-pawn.png")), (SQUARE_SIZE, SQUARE_SIZE)),
        "rook": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-rook.png")), (SQUARE_SIZE, SQUARE_SIZE)),
        "knight": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-knight.png")), (SQUARE_SIZE, SQUARE_SIZE)),
        "bishop": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-bishop.png")), (SQUARE_SIZE, SQUARE_SIZE)),
        "queen": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-queen.png")), (SQUARE_SIZE, SQUARE_SIZE)),
        "king": pygame.transform.scale(pygame.image.load(os.path.join(piece_image_path, f"{color}-king.png")), (SQUARE_SIZE, SQUARE_SIZE)),
    }

# Load both white and black piece images
white_images = load_piece_images("white")
black_images = load_piece_images("black")

# Initialize the chessboard
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

# Handle Stockfish move
def stockfish_move():
    result = engine.play(board, chess.engine.Limit(time=1.0))
    board.push(result.move)
    return result.move

# Draw the chessboard and labels
def draw_chessboard_with_labels(last_move=None):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            x = X_OFFSET + col * SQUARE_SIZE
            y = Y_OFFSET + row * SQUARE_SIZE

            if last_move:
                from_square, to_square = last_move
                if chess.square(col, 7 - row) == from_square or chess.square(col, 7 - row) == to_square:
                    color = (245, 246, 129)

            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            label_color = BLACK if color == WHITE else WHITE

            if row == 7:
                label = chr(97 + col)
                label_surface = font.render(label, True, label_color)
                label_x = x + SQUARE_SIZE // 2 - label_surface.get_width() + 35
                label_y = y + SQUARE_SIZE - label_surface.get_height() - 5
                screen.blit(label_surface, (label_x, label_y))

            if col == 0:
                label = str(8 - row)
                label_surface = font.render(label, True, label_color)
                label_x = x + 5
                label_y = y + SQUARE_SIZE // 2 - label_surface.get_height() - 10
                screen.blit(label_surface, (label_x, label_y))

# Draw the pieces on the board
def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = "white" if piece.color == chess.WHITE else "black"
            piece_type = piece.piece_type
            piece_name = {chess.PAWN: "pawn", chess.ROOK: "rook", chess.KNIGHT: "knight", chess.BISHOP: "bishop", chess.QUEEN: "queen", chess.KING: "king"}[piece_type]
            x = X_OFFSET + (square % 8) * SQUARE_SIZE
            y = Y_OFFSET + (7 - (square // 8)) * SQUARE_SIZE
            screen.blit(white_images[piece_name] if color == "white" else black_images[piece_name], (x, y))

# Draw valid moves as circles
def draw_valid_moves(valid_moves):
    for move in valid_moves:
        col, row = move % 8, 7 - (move // 8)
        x = X_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = Y_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 10)

# Handle mouse click events
def handle_click(pos):
    global selected_square, valid_moves, last_move

    col, row = (pos[0] - X_OFFSET) // SQUARE_SIZE, (pos[1] - Y_OFFSET) // SQUARE_SIZE
    square = chess.square(col, 7 - row)

    if selected_square is None:
        piece = board.piece_at(square)
        if piece and piece.color == board.turn:
            selected_square = square
            valid_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
    else:
        if square in valid_moves:
            move = chess.Move(selected_square, square)
            if move in board.legal_moves:
                board.push(move)
                last_move = (selected_square, square)
            selected_square = None
            valid_moves = []
        else:
            selected_square = None
            valid_moves = []

    return valid_moves

# Draw the menu screen
def draw_menu():
    screen.fill(BLACK)

    title_font = pygame.font.SysFont("Arial", 50)
    title_text = title_font.render("Chess Game", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    button_width = 300
    button_height = 100
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT // 2 - button_height // 2

    button_2p = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_2p)
    button_2p_text = font.render("Two Player", True, TEXT_COLOR)
    screen.blit(button_2p_text, button_2p.move(50, 30))

    button_bot = pygame.Rect(button_x, button_y + button_height + 20, button_width, button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_bot)
    button_bot_text = font.render("Bot vs Player", True, TEXT_COLOR)
    screen.blit(button_bot_text, button_bot.move(50, 30))

    pygame.display.flip()

    return button_2p, button_bot

# Initialize variables
clock = pygame.time.Clock()
running = True
game_mode = None

while running:
    if game_mode is None:
        button_2p, button_bot = draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_2p.collidepoint(event.pos):
                        game_mode = "2p"
                    elif button_bot.collidepoint(event.pos):
                        game_mode = "bot"

    if game_mode:
        board = chess.Board()
        selected_square = None
        valid_moves = []
        last_move = None

        while game_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    game_mode = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        valid_moves = handle_click(event.pos)

            if game_mode == "bot" and board.turn != chess.WHITE and not board.is_game_over():
                move = stockfish_move()
                last_move = (move.from_square, move.to_square)

            screen.fill((200, 200, 200))
            draw_chessboard_with_labels(last_move)
            draw_pieces()
            draw_valid_moves(valid_moves)
            pygame.display.flip()
            clock.tick(FPS)

pygame.quit()
engine.quit()
sys.exit()
