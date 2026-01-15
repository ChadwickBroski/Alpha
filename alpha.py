import chess
import time

name = "ALPHA"
version = "0.2.0b"

board = chess.Board()
number_of_lines = 30   # how many top moves to keep each ply
depth = 5              # how many plies of reply-minimization
i = 0

piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 340,
    chess.BISHOP: 350,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

central_squares = {
    chess.C4, chess.C5, chess.D4, chess.D5,
    chess.E4, chess.E5, chess.F4, chess.F5
}

def evaluate_position():
    """Evaluate current board from Black's perspective (positive = good for Black)."""
    score = 0

    # Material balance
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if not p:
            continue
        val = piece_value[p.piece_type]
        score += val if p.color == chess.BLACK else -val

    # Central pawn presence (light touch)
    for csq in central_squares:
        p = board.piece_at(csq)
        if p and p.piece_type == chess.PAWN:
            score += 15 if p.color == chess.BLACK else -15

    # Bishop mobility (both sides, symmetric)
    directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
    for color in [chess.BLACK, chess.WHITE]:
        mobility_total = 0
        for bsq in board.pieces(chess.BISHOP, color):
            f0, r0 = chess.square_file(bsq), chess.square_rank(bsq)
            for df, dr in directions:
                f, r = f0, r0
                while 0 <= f+df <= 7 and 0 <= r+dr <= 7:
                    f += df; r += dr
                    sq = chess.square(f, r)
                    p = board.piece_at(sq)
                    if p:
                        if p.color != color:
                            mobility_total += 1  # can capture
                        break
                    mobility_total += 1
        score += mobility_total * (2 if color == chess.BLACK else -2)

    # Attacker/defender logic: free captures and simple profitable trades
    for sq in chess.SQUARES:
        victim = board.piece_at(sq)
        if not victim:
            continue
        vval = piece_value[victim.piece_type]

        # Black attacking White piece
        b_atk = [board.piece_at(a) for a in board.attackers(chess.BLACK, sq)]
        w_def = [board.piece_at(d) for d in board.attackers(chess.WHITE, sq)]
        if b_atk:
            if not w_def:
                score += vval  # free capture available
            else:
                ca = min(piece_value[a.piece_type] for a in b_atk if a)
                cd = min(piece_value[d.piece_type] for d in w_def if d)
                if ca < vval and cd > ca:
                    score += (vval - ca)

        # White attacking Black piece
        w_atk = [board.piece_at(a) for a in board.attackers(chess.WHITE, sq)]
        b_def = [board.piece_at(d) for d in board.attackers(chess.BLACK, sq)]
        if w_atk:
            if not b_def:
                score -= vval  # free capture for White
            else:
                ca = min(piece_value[a.piece_type] for a in w_atk if a)
                cd = min(piece_value[d.piece_type] for d in b_def if d)
                if ca < vval and cd > ca:
                    score -= (vval - ca)

    # Checkmate (from side-to-move perspective)
    if board.is_checkmate():
        # If it's checkmate, the side to move just got mated
        score += -1000000 if board.turn == chess.BLACK else 1000000

    return score

def evaluate_move(move):
    """Evaluate a move by making it, scoring the position, then undoing."""
    board.push(move)
    s = evaluate_position()
    board.pop()
    return s

def find_best_move():
    # initial candidates: all legal moves scored
    candidates = []
    for move in board.legal_moves:
        candidates.append((evaluate_move(move), move))

    candidates.sort(reverse=True, key=lambda x: x[0])
    candidates = candidates[:number_of_lines]

    # reply-minimization loop (no minimax): assume opponent picks worst for us
    for _ in range(depth - 1):
        new_candidates = []
        for score, move in candidates:
            board.push(move)

            reply_scores = []
            for reply in board.legal_moves:
                reply_scores.append(evaluate_move(reply))

            board.pop()

            new_score = min(reply_scores) if reply_scores else score
            new_candidates.append((new_score, move))

        new_candidates.sort(reverse=True, key=lambda x: x[0])
        candidates = new_candidates[:number_of_lines]

    # Debug: print top candidates
    print(candidates)
    return candidates[0][1]

def computer():
    best_move = find_best_move()
    print(f"Computer plays: {best_move}")
    board.push(best_move)
    print(board)

def play():
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            user_move = input("Your move: ")
            try:
                board.push_san(user_move)
                print(board)
            except:
                if user_move == "quit":
                    break
                elif user_move == "fen":
                    print(board.fen())
                else:
                    print("Invalid move")
                    continue
        else:
            start_time = time.perf_counter()
            computer()
            end_time = time.perf_counter()
            elapsed_time = round(end_time - start_time, 4)
            print(f"Computer thought for {elapsed_time} seconds.")

    print("Game over:", board.result())

print(f"{name} {version} is starting...")
print("San moves are accepted.")
play()
