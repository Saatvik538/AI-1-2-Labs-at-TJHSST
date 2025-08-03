import sys; args = sys.argv[1:]
import re

CORNERS = {0, 7, 56, 63}
EDGES = {1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55, 57, 58, 59, 60, 61, 62}

# Global cache table for negamax
cache = {}

def print_snapshot(board, token, possible_moves):
    display_board(board, possible_moves)
    print()
    print(board, board.count('x') + board.count('X'), "/", board.count('o') + board.count('O'))
    if possible_moves:
        print(f"Possible moves for {token}: {', '.join(map(str, sorted(set(possible_moves))))}")
    else:
        print("No moves possible")
    print()

def parse_move(move_input):
    #converts move input to board index
    if isinstance(move_input, str) and move_input.isdigit():
        return int(move_input)
    elif isinstance(move_input, str) and len(move_input) == 2:
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
    #determines the default token to play based on the current board state
    x_moves = get_possible_moves(board, 'x')
    o_moves = get_possible_moves(board, 'o')
    if not x_moves and o_moves:
        return 'o'
    elif not o_moves and x_moves:
        return 'x'
    else:
        return 'x' if board.count('.') % 2 == 0 else 'o'

def display_board(board, possible_moves=None):
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if possible_moves and index in possible_moves:
                print('*', end='')
            else:
                print(board[index].upper(), end='')
        print()

def get_possible_moves(board, token):
    possible_moves = set()
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    opponent = 'o' if token == 'x' else 'x'

    for i in range(64):
        if board[i] != '.':
            continue
        for dx, dy in directions:
            x, y = i // 8, i % 8
            x, y = x + dx, y + dy
            if 0 <= x < 8 and 0 <= y < 8 and board[x*8 + y].lower() == opponent:
                while 0 <= x < 8 and 0 <= y < 8:
                    if board[x*8 + y] == '.':
                        break
                    if board[x*8 + y].lower() == token:
                        possible_moves.add(i)
                        break
                    x, y = x + dx, y + dy

    return list(possible_moves)

def make_move(board, move, token):
    board = list(board.lower())
    board[move] = token
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    opponent = 'o' if token == 'x' else 'x'

    for dx, dy in directions:
        x, y = move // 8, move % 8
        x, y = x + dx, y + dy
        to_flip = []
        while 0 <= x < 8 and 0 <= y < 8 and board[x*8 + y] == opponent:
            to_flip.append(x*8 + y)
            x, y = x + dx, y + dy
        if 0 <= x < 8 and 0 <= y < 8 and board[x*8 + y] == token:
            for flip_pos in to_flip:
                board[flip_pos] = token
    return ''.join(board)

def negamax(brd, tkn):
    #check if the current board state and token combination is already cached
    board_key = (tuple(brd), tkn)  
    if board_key in cache:
        return cache[board_key]

    #get possible moves
    possible_moves = get_possible_moves(brd, tkn)

    #base case: game is over
    if not possible_moves:
        opponent_moves = get_possible_moves(brd, 'o' if tkn == 'x' else 'x')
        if not opponent_moves:  #game is truly over
            score = brd.count(tkn) - brd.count('o' if tkn == 'x' else 'x')
            result = (score, [])
            cache[board_key] = result  #store the result in the cache
            return result

        #must pass
        neg_score, move_seq = negamax(brd, 'o' if tkn == 'x' else 'x')
        result = (-neg_score, [-1] + move_seq)
        cache[board_key] = result  #store the result in the cache
        return result

    #initialize best score and sequence
    best_score = float('-inf')
    best_sequence = []

    #explore all possible moves
    for move in possible_moves:
        new_board = make_move(brd, move, tkn)
        neg_score, move_seq = negamax(new_board, 'o' if tkn == 'x' else 'x')
        score = -neg_score

        if score > best_score:
            best_score = score
            best_sequence = [move] + move_seq

    #store the result in the cache
    result = (best_score, best_sequence)
    cache[board_key] = result
    return result

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

def quickMove(brd, tkn):
    open_positions = brd.count('.')
    
    if open_positions < 11:
        score, move_sequence = negamax(brd, tkn)
        best_move = move_sequence[-1]
        print(f"My move is {best_move}") #get the last move in the sequence
        #print score and move sequence in the required format
        print(f"Min score: {score}; Move sequence: {move_sequence[::-1]}")
        return best_move

    #Otherwise use the original strategy
    corneravoid = {0:{1, 8, 9}, 7:{6, 14, 15}, 56:{48, 49, 57}, 63:{54, 55, 62}}
    possible_moves = get_possible_moves(brd, tkn)
    if not possible_moves:
        return None
    
    #strat 1: play to a corner, avoid playing next to an opponent's corner
    for corner in CORNERS:
        if corner in possible_moves:
            return corner
        if brd[corner] != tkn:
            for adjacent in corneravoid[corner]:
                if len(possible_moves) > 1 and adjacent in possible_moves:
                    possible_moves.remove(adjacent)
        else:
            for adjacent in corneravoid[corner]:
                if adjacent in possible_moves:
                    return adjacent

    #strat 2: play to a safe edge
    safe_edge_moves = []
    for move in possible_moves:
        if is_safe_edge(brd, move, tkn):
            safe_edge_moves.append(move)
    
    if safe_edge_moves:
        best_safe_move = None
        max_flips = -1
        for move in safe_edge_moves:
            flips = count_flips(brd, move, tkn)
            if flips > max_flips:
                max_flips = flips
                best_safe_move = move
        return best_safe_move

    #strat 3: minimize opponent's mobility
    min_opponent_moves = float('inf')
    best_move = None
    opponent = 'o' if tkn == 'x' else 'x'
    for move in possible_moves:
        new_board = make_move(brd, move, tkn)
        opponent_moves = len(get_possible_moves(new_board, opponent))
        if opponent_moves < min_opponent_moves:
            min_opponent_moves = opponent_moves
            best_move = move
    
    if best_move is not None:
        return best_move

    #strat 4: choose move that flips the most pieces
    max_flips = -1
    for move in possible_moves:
        flips = count_flips(brd, move, tkn)
        if flips > max_flips:
            max_flips = flips
            best_move = move

    return best_move if best_move is not None else possible_moves[0]
def process_condensed_game(condensed_game, board, token):
    #processes a condensed game notation
    moves = [condensed_game[i:i+2] for i in range(0, len(condensed_game), 2)]
    for i, move in enumerate(moves):
        if "_" in move:
            move = move[1:]
            moves[i] = move
    for i, move in enumerate(moves):
        move = int(move)
        moves[i] = move
def main():
    #main game logic
    board, token, moves, condensed_game = parse_args(args)
    if condensed_game:
        if token is None:
            token = get_default_token(board)
        board, token = process_condensed_game(condensed_game, board, token)
    if moves:
        if token is None:
            token = get_default_token(board)

        possible_moves = get_possible_moves(board, token)
        print_snapshot(board, token, possible_moves)

        for move in moves:
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
        mvPref = quickMove(board, token)
        print(f"The preferred move is: {mvPref}")

if __name__ == "__main__":
    main()

#saatvik kesarwani, pd 1, 2026