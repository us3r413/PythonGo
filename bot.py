import chess
from numpy import iinfo, int32

class Bot:
    pawn_pos_val = [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10,-20,-20, 10, 10,  5,
         5, -5,-10,  0,  0,-10, -5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
         0,  0,  0,  0,  0,  0,  0,  0
    ]
    knight_pos_val = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    bishop_pos_val = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    rook_pos_val = [
         0,  0,  5,  10, 10, 5,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         5,  10, 10, 10, 10, 10, 10, 5,
         0,  0,  0,  0,  0,  0,  0,  0
    ]
    queen_pos_val = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
          0,  0,  5,  5,  5,  5,  0, -5,
         -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    king_pos_val = [
         20,  30,  10,  0,   0,   10,  30,  20,
         20,  20,  0,   0,   0,   0,   20,  20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]

    def __init__(self, whiteSide: bool = True):
        self.whiteSide = whiteSide

    def makeNextMove(self, currentFen: str):
        board = chess.Board(currentFen)
        best_move = None
        best_value = iinfo(int32).min if self.whiteSide else iinfo(int32).max

        for move in board.legal_moves:
            board.push(move)
            value = self.alphabeta(board, 4, iinfo(int32).min, iinfo(int32).max, not self.whiteSide)
            board.pop()

            if self.whiteSide and value > best_value:
                best_value = value
                best_move = move
            elif not self.whiteSide and value < best_value:
                best_value = value
                best_move = move

        return best_move if best_move else None

    def alphabeta(self, board: chess.Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
        if depth == 0 or board.is_game_over():
            return self.evaluate2(board) # 這裡可以改需要用的 evaluate function

        if maximizingPlayer:
            max_eval = iinfo(int32).min
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = iinfo(int32).max
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def evaluate1(self, board: chess.Board):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100
        }

        multiplier = 1 if self.whiteSide else -1
        value = 0
        for piece_type, piece_value in piece_values.items():
            value += len(board.pieces(piece_type, chess.WHITE)) * piece_value
            value -= len(board.pieces(piece_type, chess.BLACK)) * piece_value

        return value * multiplier
    
    def evaluate2(self, board: chess.Board):
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 2000
        }

        multiplier = 1 if self.whiteSide else -1
        value = 0
        for piece_type, piece_value in piece_values.items():
            for square in board.pieces(piece_type, chess.WHITE):
                if piece_type == chess.PAWN:
                    value += self.pawn_pos_val[square] * piece_value
                elif piece_type == chess.KNIGHT:
                    value += self.knight_pos_val[square] * piece_value
                elif piece_type == chess.BISHOP:
                    value += self.bishop_pos_val[square] * piece_value
                elif piece_type == chess.ROOK:
                    value += self.rook_pos_val[square] * piece_value
                elif piece_type == chess.QUEEN:
                    value += self.queen_pos_val[square] * piece_value
                else:
                    value += self.king_pos_val[square] * piece_value

        for piece_type, piece_value in piece_values.items():
            for square in board.pieces(piece_type, chess.BLACK):
                if piece_type == chess.PAWN:
                    value -= self.pawn_pos_val[square] * piece_value
                elif piece_type == chess.KNIGHT:
                    value -= self.knight_pos_val[square] * piece_value
                elif piece_type == chess.BISHOP:
                    value -= self.bishop_pos_val[square] * piece_value
                elif piece_type == chess.ROOK:
                    value -= self.rook_pos_val[square] * piece_value
                elif piece_type == chess.QUEEN:
                    value -= self.queen_pos_val[square] * piece_value
                else:
                    value -= self.king_pos_val[square] * piece_value

        return value * multiplier
