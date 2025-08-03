import sys; args = sys.argv[1:]
import re

CORNERS = {0, 7, 56, 63}
EDGES = {1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55, 57, 58, 59, 60, 61, 62}

# Global caches
possible_moves_cache = {}
alphabeta_cache = {}

def print_snapshot(board, token, possible_moves, last_move=None):
    display_board(board, possible_moves, last_move)
    print()
    print(board, board.count('x') + board.count('X'), "/", board.count('o') + board.count('O'))
    if possible_moves:
        print(f"Possible moves for {token}: {', '.join(map(str, sorted(set(possible_moves))))}")
    else:
        print("No moves possible")
    print()

def parse_move(move_input):
    if isinstance(move_input, int):
        return move_input
    if isinstance(move_input, str):
        if move_input.isdigit():
            return int(move_input)
        elif len(move_input) == 2:
            col = ord(move_input[0].lower()) - ord('a')
            row = int(move_input[1]) - 1
            if 0 <= col < 8 and 0 <= row < 8:
                return row * 8 + col
    return None

def parse_args(args):
    board_pattern = r'^[.xoXO]{64}$'
    token_pattern = r'^[xoXO]$'
    move_pattern = r'^([a-hA-H][1-8]|-?\d+)$'
    board = '.' * 27 + 'ox......xo' + '.' * 27
    token = None
    moves = []
    condensed_game = None

    for arg in args:
        if re.match(board_pattern, arg):
            board = arg.lower()
        elif re.match(token_pattern, arg):
            token = arg.lower()
        elif re.match(move_pattern, arg) and len(str(arg)) < 3:
            move = parse_move(arg)
            if move is not None:
                moves.append(move)
        else:
            condensed_game = arg

    return board, token, moves, condensed_game

def get_default_token(board):
    x_moves = get_possible_moves(board, 'x')
    o_moves = get_possible_moves(board, 'o')
    if not x_moves and o_moves:
        return 'o'
    elif not o_moves and x_moves:
        return 'x'
    else:
        return 'x' if board.count('.') % 2 == 0 else 'o'

def display_board(board, possible_moves=None, last_move=None):
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if possible_moves and index in possible_moves:
                print('*', end='')
            elif last_move is not None and index == last_move:
                print(board[index].upper(), end='')
            else:
                print(board[index].upper(), end='')
        print()

def get_possible_moves(board, token):
    board_key = (board, token)
    if board_key in possible_moves_cache:
        return possible_moves_cache[board_key]

    possible_moves = set()
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    opponent = 'o' if token == 'x' else 'x'

    for i in range(64):
        if board[i] != '.':
            continue
        for dx, dy in directions:
            x, y = i // 8, i % 8
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and board[nx*8 + ny].lower() == opponent:
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if board[nx*8 + ny] == '.':
                        break
                    if board[nx*8 + ny].lower() == token:
                        possible_moves.add(i)
                        break
                    nx, ny = nx + dx, ny + dy

    result = list(possible_moves)
    possible_moves_cache[board_key] = result
    return result

def make_move(board, move, token):
    board = list(board.lower())
    board[move] = token
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    opponent = 'o' if token == 'x' else 'x'

    for dx, dy in directions:
        x, y = move // 8, move % 8
        nx, ny = x + dx, y + dy
        to_flip = []
        while 0 <= nx < 8 and 0 <= ny < 8 and board[nx*8 + ny] == opponent:
            to_flip.append(nx*8 + ny)
            nx, ny = nx + dx, ny + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[nx*8 + ny] == token:
            for flip_pos in to_flip:
                board[flip_pos] = token
    return ''.join(board)

def evaluate_position(board, move, token):
    score = 0
    if move in CORNERS:
        score += 100
    elif move in EDGES:
        score += 50
    
    new_board = make_move(board, move, token)
    opponent = 'o' if token == 'x' else 'x'
    opponent_moves = len(get_possible_moves(new_board, opponent))
    score -= opponent_moves * 2
    
    return score

def alphabeta_top(board, token):
    best_score = float('-inf')
    best_move = None
    best_sequence = []
    alpha = float('-inf')
    beta = float('inf')
    
    possible_moves = get_possible_moves(board, token)
    if not possible_moves:
        return [0]
    
    # Sort moves by initial evaluation
    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in possible_moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]
    
    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score, sequence = alphabeta(new_board, 'o' if token == 'x' else 'x', -beta, -alpha, 1)
        score = -score
        
        if score > best_score:
            best_score = score
            best_move = move
            best_sequence = [move] + sequence
            print(f"Score: {best_score}; Move: {best_move}")
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return [best_score] + best_sequence

def alphabeta(board, token, alpha, beta, depth):
    possible_moves = get_possible_moves(board, token)
    
    if not possible_moves:
        opponent = 'o' if token == 'x' else 'x'
        opponent_moves = get_possible_moves(board, opponent)
        if not opponent_moves:
            # Game is over, count pieces
            score = board.count(token) - board.count(opponent)
            return score, []
        # Must pass
        score, sequence = alphabeta(board, opponent, -beta, -alpha, depth - 1)
        return -score, sequence
    
    best_score = float('-inf')
    best_sequence = []
    
    # Sort moves by evaluation
    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in possible_moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]
    
    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score, sequence = alphabeta(new_board, 'o' if token == 'x' else 'x', -beta, -alpha, depth - 1)
        score = -score
        
        if score > best_score:
            best_score = score
            best_sequence = [move] + sequence
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return best_score, best_sequence

def is_safe_edge(board, move, token):
    if move not in EDGES:
        return False
    
    row, col = divmod(move, 8)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if 0 <= x < 8 and 0 <= y < 8:
            if board[x*8 + y] == '.':
                return False
    
    for dx, dy in directions:
        x, y = row + dx, col + dy
        while 0 <= x < 8 and 0 <= y < 8:
            if board[x*8 + y] != token:
                break
            x, y = x + dx, y + dy
        if 0 <= x < 8 and 0 <= y < 8 and board[x*8 + y] == '.':
            return False
    
    return True

def quickMove(board, token, hl=0):
    if not board:  # Set hole limit
        global HLLIM
        HLLIM = token
        return
    
    open_positions = board.count('.')
    if open_positions <= hl:
        ab_result = alphabeta_top(board, token)
        print(f"Min score: {ab_result[0]}; Move sequence: {ab_result[1:][::-1]}")
        return ab_result[1]
    
    return rule_of_thumb(board, token)

def rule_of_thumb(board, token):
    corneravoid = {0:{1, 8, 9}, 7:{6, 14, 15}, 56:{48, 49, 57}, 63:{54, 55, 62}}
    possible_moves = get_possible_moves(board, token)
    if not possible_moves:
        return None
    
    for corner in CORNERS:
        if corner in possible_moves:
            return corner
        if board[corner] != token:
            for adjacent in corneravoid[corner]:
                if len(possible_moves) > 1 and adjacent in possible_moves:
                    possible_moves.remove(adjacent)
        else:
            for adjacent in corneravoid[corner]:
                if adjacent in possible_moves:
                    return adjacent
    
    safe_edge_moves = [move for move in possible_moves if is_safe_edge(board, move, token)]
    
    if safe_edge_moves:
        return max(safe_edge_moves, key=lambda m: count_flips(board, m, token))
    
    opponent = 'o' if token == 'x' else 'x'
    return min(possible_moves, key=lambda m: len(get_possible_moves(make_move(board, m, token), opponent)))

def count_flips(board, move, token):
    flips = 0
    opponent = 'o' if token == 'x' else 'x'
    directions = [-1, 1, -8, 8, -9, 9, -7, 7]
    
    for direction in directions:
        current = move + direction
        flip_count = 0
        while 0 <= current < 64 and board[current] == opponent:
            flip_count += 1
            current += direction
        if 0 <= current < 64 and board[current] == token:
            flips += flip_count
    
    return flips

def process_condensed_game(condensed_game, board, token):
    hl = 0
    if condensed_game.startswith('HL'):
        hl_match = re.match(r'HL(\d+)', condensed_game)
        if hl_match:
            hl = int(hl_match.group(1))
            condensed_game = condensed_game[len(hl_match.group(0)):].strip()
    moves = [condensed_game[i:i+2] for i in range(0, len(condensed_game), 2)]
    verbose = 'v' in condensed_game.lower()
    
    if verbose:
        moves = [move for move in moves if move.lower() != 'v']
    
    print_snapshot(board, token, get_possible_moves(board, token))
    
    for i, move in enumerate(moves):
        if move == '_1':
            token = 'o' if token == 'x' else 'x'
            continue
        if '_' in move:
            move = move[1:]
        move = int(move)
        board = make_move(board, move, token)
        token = 'o' if token == 'x' else 'x'
        possible_moves = get_possible_moves(board, token)
        print(f"{'x' if token == 'o' else 'o'} plays to {move}")
        if verbose or i == len(moves) - 1:
            print_snapshot(board, token, possible_moves)
    
    return board, token, hl

def main():
    board, token, moves, condensed_game = parse_args(args)
    hl = 0
    verbose = False

    if condensed_game:
        if token is None:
            token = get_default_token(board)
        board, token, hl = process_condensed_game(condensed_game, board, token)
        verbose = 'v' in condensed_game.lower()
   
    if moves:
        if token is None:
            token = get_default_token(board)

        possible_moves = get_possible_moves(board, token)
        print_snapshot(board, token, possible_moves)

        for i, move in enumerate(moves):
            if move < 0:
                continue
            if move in possible_moves:
                print(f"{token} plays to {move}")
                board = make_move(board, move, token)
                token = 'o' if token == 'x' else 'x'
                possible_moves = get_possible_moves(board, token)
               
                if not possible_moves:
                    token = 'o' if token == 'x' else 'x'
                    possible_moves = get_possible_moves(board, token)
                    if not possible_moves:
                        print_snapshot(board, token, possible_moves)
                        break
               
                if verbose or i == len(moves) - 1:
                    print_snapshot(board, token, possible_moves)
            else:
                print(f"Invalid move: {move}")
                break
    else:
        if token is None:
            token = get_default_token(board)
        possible_moves = get_possible_moves(board, token)
        print_snapshot(board, token, possible_moves)
   
    possible_moves = get_possible_moves(board, token)
    if possible_moves:
        mvPref = quickMove(board, token, hl)
        if mvPref:
            print(f"The preferred move is: {mvPref}")

if __name__ == "__main__":
    main()

#saatvik kesarwani, pd 1, 2026