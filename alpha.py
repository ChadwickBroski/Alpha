import chess
import time

name = "ALPHA"
version = "0.1.0b"

board = chess.Board()
number_of_lines = 30   # change this to control how many top moves are examined
depth = 5  # change this to control how far it looks
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

central_values = {
    chess.C4: 100, chess.C5: 100,
    chess.D4: 150, chess.D5: 150,
    chess.E4: 200, chess.E5: 200
}

def evaluate(move):
    score = 0
    material=0

    # Reward captures
    if board.is_capture(move):
        captured = board.piece_at(move.to_square)
        if captured:
            score += piece_value[captured.piece_type]

    # Material Count
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.BLACK:
                material += piece_value[piece.piece_type]
            else:
                material -= piece_value[piece.piece_type]
    score+=material

    # Reward central squares (FOCUS ON PAWNS)
    for csq in central_squares:
        piece = board.piece_at(csq)
        if piece and piece.piece_type == chess.PAWN:
            csq_multiply = board.fullmove_number - 1
            csq_multiply = 11 - csq_multiply
            if csq_multiply > 11:
                csq_multiply = 0

            if piece.color == chess.BLACK:
                score += 10 * csq_multiply
            else:
                score -= 10 * csq_multiply


    # Reward open bishops (FOCUS ON BISHOPS)
    for bsq in board.pieces(chess.BISHOP, chess.BLACK):
        mobility = 0
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        f0, r0 = chess.square_file(bsq), chess.square_rank(bsq)

        for df, dr in directions:
            f, r = f0, r0
            while True:
                f += df
                r += dr
                if not (0 <= f <= 7 and 0 <= r <= 7):
                    break
                sq = chess.square(f, r)
                piece = board.piece_at(sq)
                if piece:
                    if piece.color != chess.BLACK:
                        mobility += 1  # can capture
                    break  # blocked
                mobility += 1  # empty square

        score += mobility * 2

    # Check for any possible gains, look for any defenders, and add to score
    for square in chess.SquareSet(board.occupied_co[chess.WHITE]):
        attackers = board.attackers(chess.BLACK, square)

        if attackers:
            victim = board.piece_at(square)
            victim_value = piece_value[victim.piece_type]

            # get cheapest black attacker
            attacker_values = [
                piece_value[board.piece_at(a).piece_type]
                for a in attackers
                if board.piece_at(a)
            ]

            if attacker_values:
                cheapest_attacker = min(attacker_values)

                net_gain = victim_value - cheapest_attacker

                # only reward if actually winning material
                if net_gain > 0:
                    score += net_gain

    
    # Look for any white attackers
    for atk_square in chess.SquareSet(board.occupied_co[chess.BLACK]):
        attackers = board.attackers(chess.WHITE, atk_square)

        if attackers:
            victim = board.piece_at(atk_square)
            victim_value = piece_value[victim.piece_type]

            # get cheapest white attacker
            attacker_values = [
                piece_value[board.piece_at(a).piece_type]
                for a in attackers
                if board.piece_at(a)
            ]

            if attacker_values:
                cheapest_attacker = min(attacker_values)

                net_gain = victim_value - cheapest_attacker

                # punish black only if white wins material
                if net_gain > 0:
                    score -= net_gain

    # Reward chekmate
    if board.is_checkmate():
        score+=100000000

    return score

def find_best_move():
    # initial candidates: all legal moves
    candidates = []

    for move in board.legal_moves:
        board.push(move)
        score = evaluate(move)
        board.pop()
        candidates.append((score, move))

    # sort and keep top N
    candidates.sort(reverse=True, key=lambda x: x[0])
    candidates = candidates[:number_of_lines]

    # repeat evaluation depth-1 times
    for _ in range(depth - 1):
        new_candidates = []

        for score, move in candidates:
            board.push(move)

            # evaluate replies
            reply_scores = []
            for reply in board.legal_moves:
                board.push(reply)
                reply_scores.append(evaluate(reply))
                board.pop()

            board.pop()

            # assume opponent plays best reply (worst for us)
            if reply_scores:
                new_score = min(reply_scores)
            else:
                new_score = score

            new_candidates.append((new_score, move))

        # sort again and trim
        new_candidates.sort(reverse=True, key=lambda x: x[0])
        candidates = new_candidates[:number_of_lines]

    print(candidates)
    return candidates[0][1]



def computer():
    # Ask for best move and push
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
                    print (board.fen())
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

print (f"{name} {version} is starting...")
print ("San moves are accepted.")
play()
