import chess
from numpy import iinfo, int32

class Bot:
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
            return self.evaluate(board)

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

    def evaluate(self, board: chess.Board):
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
