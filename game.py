import chess
from bot import Bot
import draw
import pygame
# START = "rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR w KQkq - 0 1"
START = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
def get_square_under_mouse(square_size):
    x, y = pygame.mouse.get_pos()
    col = x // square_size
    row = y // square_size
    return chess.square(col, row)
def main():
    pygame.init()
    board = chess.Board()
    disp = draw.display()
    selected_square = None
    legal_targets = []
    running = True
    botTurn = True
    bot = Bot(True)
    while running:
        disp.draw_board(board, highlights=legal_targets)

        if board.is_game_over() or len(board.pieces(chess.KING, chess.WHITE)) == 0 or len(board.pieces(chess.KING, chess.BLACK)) == 0:
            print('game over')
            running = False

        if botTurn and not board.is_game_over():
            move = bot.makeNextMove(board.fen())
            if move:
                board.push(move)
                # print(board.fen())
                
            botTurn = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_square = get_square_under_mouse(disp.SQUARE_SIZE)

                if selected_square is None:
                    piece = board.piece_at(clicked_square)
                    if piece and piece.color == board.turn:
                        selected_square = clicked_square
                        legal_targets = [move.to_square for move in board.pseudo_legal_moves if move.from_square == selected_square]

                else:
                    if clicked_square in legal_targets:
                        move = chess.Move(selected_square, clicked_square)
                        if move in board.pseudo_legal_moves:
                            board.push(move)
                            botTurn = True
                            # print(board.fen())
                    selected_square = None
                    legal_targets = []

    pygame.quit()

if __name__ == '__main__':
    main()