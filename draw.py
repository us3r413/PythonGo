import pygame
import chess

class display:
    pygame.init()
    WHITE_SQUARE = (255, 255, 255)
    BLACK_SQUARE = (125, 135, 150)
    HIGHLIGHT_COLOR = (78, 240, 161)
    PIECE_IMAGES = {
        chess.PAWN: ('images/wP.png','images/bP.png'),
        chess.KNIGHT: ('images/wN.png','images/bN.png'),
        chess.BISHOP: ('images/wB.png','images/bB.png'),
        chess.ROOK: ('images/wR.png','images/bR.png'),
        chess.QUEEN: ('images/wQ.png','images/bQ.png'),
        chess.KING: ('images/wK.png','images/bK.png')
    }
    SQUARE_SIZE = 60
    BOARD_SIZE = SQUARE_SIZE * 8
    WIDTH, HEIGHT = BOARD_SIZE, BOARD_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')

    def draw_board(self, board, highlights=[]):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, row)
                color = self.HIGHLIGHT_COLOR if square in highlights else (
                    self.WHITE_SQUARE if (row + col) % 2 == 0 else self.BLACK_SQUARE
                )
                pygame.draw.rect(self.screen, color, (
                    col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE, self.SQUARE_SIZE))

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece.piece_type
                color = 0 if piece.color else 1
                piece_image = pygame.image.load(self.PIECE_IMAGES[piece_type][color])
                piece_image = pygame.transform.scale(piece_image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                row, col = divmod(square, 8)
                self.screen.blit(piece_image, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
        pygame.display.flip()