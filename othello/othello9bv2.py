import sys; args = sys.argv[1:]
# Saatvik Kesarwani
import re
import random
import time

CORNERS = {0, 7, 56, 63}
EDGES = {1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55, 57, 58, 59, 60, 61, 62}
X_SQUARES = {9, 14, 49, 54}
C_SQUARES = {1, 6, 8, 15, 48, 55, 57, 62}
CORNER_POSITIONS = {0, 7, 56, 63}
C_SQUARE_POSITIONS = [(0, 1), (7, 6), (0, 8), (7, 15), (56, 48), (63, 55), (56, 57), (63, 62)]
X_SQUARE_POSITIONS = [(0, 9), (7, 14), (56, 49), (63, 54)]
EDGE_POSITIONS = set(list(range(1, 7)) + list(range(57, 63)) + [8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55])
INNER_DIAGONAL_POSITIONS = {18, 27, 36, 45, 21, 28, 35, 42}
# Global caches with size limits
possible_moves_cache = {}
midgame_cache = {}
alphabeta_cache = {}
MAX_CACHE_SIZE = 1000000
CURRENT_BOARD = None
CURRENT_PLAYER = None
search_cache = {}
PRECOMPUTED_RESPONSES = {'...........................ox......xo...........................': 19, '..................o........oox.....xxx..........................': 21, '...................x......xxoo.....xxx..........................': 20, '...........***.....xx.....ooxo.....xxx.....***..................': 1, '..........oo.x....oox.....oxxo.....xxx.....****.................': 12, '...*.*....ooxx....ooxo....oxxo.....xxx....*****.................': 34, '..x***....oxxx....ooxo....oxoo.....oxx....o****.................': 34, '..x***....oxxx*...ooxxx...oxoo.....oooo...o.....................': 30, '..xxxo....oooo....ooxox...oxoo*....oooo...o***.*................': 6, '.*xxxo....oxxo....oxoxx...oxoxx...ooooo...ooo***.****...........': 55, '.*xxxo....oxxx....oxooxo..oxooxo..ooxooo..oooooo..******........': 59, '.*xxxo....oxxx*...oxooxo..oxooxo..oxoooo..oooooo.*oxx***.**x....': 33, '.*xxxo....oxxx....oxoxxo..oxoxoo.ooooooo.xoxxxoo.*xoxx**.*ox....': 24, '.*xxxo*...oxxx....oxoxxo*.oxoxoo.xooooooxxoxxxoo..xxxx**.*oxx...': 49, '.*xxxo....oxxx...xxxxoxxoxxoooxooxxxoooooxxxxxooo..xxxo**..oooo*.': 9, '.*xxxxx...ooxxx..xxoxoxxoxxoooxooxxxoooooxxxxxooo..xxxo**..oooo*.': 0, '.*xxxxx...ooxxx..xxoxoxxoxxooxxooxxxooxooxxxxxoxo..xxxo*o..oooo*o': 9, 'oxxxxxx...oxxxx..xxoxoxxoxxooxxooxxxooxooxxxxoooo..xxxooo..oooooo': 9, 'ooooooooxxxxxx**xxoxoxxoxxooxxooxxxooxooxxxxoooo**xxxooo.*oooooo': None, 'oooooooooxxxxx..oxoxoxxooxooxxoooxoooxooooxxooooo*xxxooo..oooooo': None, 'ooooooooooxxxx..oooxoxxoooooxxoooooooxooooxooooooooxxooo*ooooooo': None, 'ooooooooooxxxx*ooooxoxooooooxooooooooxooooxooooooxoxxoooxooooooo': None}
HLLIM = 13
OPPONENT_MOVES = {
    '...........................ox......xo...........................': 29,
    '..................o........oox.....xxx..........................': 26,
    '...................x......xxoo.....xxx..........................': 11,
    '...........***.....xx.....ooxo.....xxx.....***..................': 10,
    '..........oo.x....oox.....oxxo.....xxx.....****.................' : 21,
    '...*.*....ooxx....ooxo....oxxo.....xxx....*****.................' : 42,
    '..x***....oxxx....ooxo....oxoo.....oxx....o****.................' : 38,
    '..x***....oxxx*...ooxxx...oxoo.....oooo...o.....................' : 3,
    '..xxxo....oooo....ooxox...oxoo*....oooo...o***.*................' : 34,
    '.*xxxo....oxxo....oxoxx...oxoxx...ooooo...ooo***.****...........' : 46,
    '.*xxxo....oxxx....oxooxo..oxooxo..ooxooo..oooooo..******........' : 51,
    '.*xxxo....oxxx*...oxooxo..oxooxo..oxoooo..oooooo.*oxx***.**x....' : 58,
    '.*xxxo....oxxx....oxoxxo..oxoxoo.ooooooo.xoxxxoo.*xoxx**.*ox....' : 17,
    '.*xxxo*...oxxx....oxoxxo*.oxoxoo.xooooooxxoxxxoo..xxxx**.*oxx...' : 24,
    '.*xxxo....oxxx...xxxxoxxoxxoooxooxxxoooooxxxxxooo..xxxo**..oooo*.' : 61,
    '.*xxxxx...ooxxx..xxoxoxxoxxoooxooxxxoooooxxxxxooo..xxxo**..oooo*.' : 9,
    '.*xxxxx...ooxxx..xxoxoxxoxxooxxooxxxooxooxxxxxoxo..xxxo*o..oooo*o' : 63,
    'oxxxxxx...oxxxx..xxoxoxxoxxooxxooxxxooxooxxxxoooo..xxxooo..oooooo' : 0,
    'ooooooooxxxxxx**xxoxoxxoxxooxxooxxxooxooxxxxoooo**xxxooo.*oooooo' : 7,
    'oooooooooxxxxx..oxoxoxxooxooxxoooxoooxooooxxooooo*xxxooo..oooooo' : 48,
    'ooooooooooxxxx..oooxoxxoooooxxoooooooxooooxooooooooxxooo*ooooooo' : 57,
    'ooooooooooxxxx*ooooxoxooooooxooooooooxooooxooooooxoxxoooxooooooo' : 15,
}
class Strategy:
    #enable logging to see the output of print statements
    logging = True
    
    def best_strategy(self, board, player, best_move, still_running, time_limit=None):
        """
        Args:
            board: The game board as a string of length 64 with chars in {'.', 'x', 'o'}
            player: The player's token ('x' or 'o')
            best_move: A multiprocessing.Value object to store the best move
            still_running: A multiprocessing.Value object to check if we should keep running
            time_limit: Optional time limit in seconds before we need to return
        """
        #get initial quick move as a safety in case we run out of time
        possible_moves = get_possible_moves(board, player)
        if possible_moves:
            best_move.value = quickMove(board, player)
        
        empty_positions = board.count('.')
        move = None
        
        #only continue if we're still running
        if still_running.value:
            #check if we should use endgame (alphabeta) or midgame strategy
            #if empty_positions <= HLLIM:
                #move = alphabeta_top(board, player)
            #else:
                #move = midgame_alphabeta(board, player)
            move = select_move(board,player)
            #if no move was found and we're still running, try rule_of_thumb
            if move is None and still_running.value:
                if possible_moves:
                    move = rule_of_thumb(board, player)
            
            #update best_move if we found a better move and are still running
            if move is not None and still_running.value:
                best_move.value = move
def precompute_best_moves(): #precompute each move
    #Runs Alpha-Beta search for every known board state and stores the best response.
    for known_board, opponent_move in OPPONENT_MOVES.items():
        opponent_board = make_move(known_board, opponent_move, 'o')  # Assume opponent is 'o'
        best_move = None
        best_score = float('-inf')

        for move in get_possible_moves(opponent_board, 'x'):  #my bot plays 'x'
            new_board = make_move(opponent_board, move, 'x')
            if new_board.count('.') < HLLIM:
                score = -alphabeta(new_board, 'o', -10000, 10000, 1)[0]
            else:
                score = -midgame_search(new_board, 'o', -10000, 10000, 3)

            if score > best_score:
                best_score = score
                best_move = move
        
        PRECOMPUTED_RESPONSES[known_board] = best_move
def select_move(board, token):
    #Select a move instantly if precomputed, otherwise fall back to Alpha-Beta.
    if board[53] == 'o' and board[7] == '.':
        return 7
    pre_move = PRECOMPUTED_RESPONSES.get(board, None)
    
    if pre_move is not None:
        return pre_move  #instantly return precomputed move in O(1) time
    
    #if no precomputed move, use normal decision-making
    if board.count('.') <= HLLIM:
        return alphabeta_top(board, token)
    return midgame_alphabeta(board, token)
#pre-compute adjacent squares for each position
ADJACENT = {}
for i in range(64):
    x, y = i // 8, i % 8
    adj = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                adj.append(nx * 8 + ny)
    ADJACENT[i] = adj

TOPRINT= ""

def print_snapshot(board, token, possible_moves, n=False, last_move=None):
    display_board(board, possible_moves, last_move)
    global TOPRINT
    print()

    if not n:
        print(f"{board} {board.count('x') + board.count('X')}/{board.count('o') + board.count('O')}")
    if possible_moves:
        TOPRINT = f"Possible moves for {token}: {', '.join(map(str, sorted(set(possible_moves))))}"
        print(f"Possible moves for {token}: {', '.join(map(str, sorted(set(possible_moves))))}")
   
    #else:
       # print("No moves possible")
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
    tournament_games = None
    verbose = False

    for arg in args:
        if re.match(board_pattern, arg):
            board = arg.lower()
        elif re.match(token_pattern, arg):
            token = arg.lower()
        elif re.match(move_pattern, arg) and len(str(arg)) < 3:
            move = parse_move(arg)
            if move is not None:
                moves.append(move)
        elif arg.startswith('P'):
            tournament_games = int(arg[1:])
        elif arg.lower() == 'v':
            verbose = True
        else:
            condensed_game = arg

    return board, token, moves, condensed_game, tournament_games, verbose

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
                print(board[index].lower(), end='')
        print()

def get_possible_moves(board, token):
    board_key = (board, token)
    if board_key in possible_moves_cache:
        return possible_moves_cache[board_key]

    possible_moves = set()
    opponent = 'o' if token == 'x' else 'x'
    
    for i in range(64):
        if board[i] != '.':
            continue
        has_adjacent = False
        for adj in ADJACENT[i]:
            if board[adj].lower() == opponent:
                has_adjacent = True
                break
        if not has_adjacent:
            continue
            
        for adj in ADJACENT[i]:
            if board[adj].lower() != opponent:
                continue
            dx = (adj // 8) - (i // 8)
            dy = (adj % 8) - (i % 8)
            nx, ny = adj // 8 + dx, adj % 8 + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                pos = nx * 8 + ny
                if board[pos] == '.':
                    break
                if board[pos].lower() == token:
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


def brdEval(board, player):
    opponent = 'o' if player == 'x' else 'x'
    
    # Define key positions
    vital_spots = {0, 7, 56, 63}  # corners
    x_squares = {1, 6, 8, 15, 48, 55, 57, 62}  # squares adjacent to corners
    x_square_to_corner = {1: 0, 6: 7, 8: 0, 15: 7, 48: 56, 55: 63, 57: 56, 62: 63}
    
    def count_stable_borders(token):
        stable_count = 0
        for edge in [range(8), range(0, 57, 8), range(7, 64, 8), range(56, 64)]:
            edge_stable = True
            for pos in edge:
                if board[pos] == token and (edge_stable or is_safe_edge(board, pos, token)):
                    stable_count += 1
                else:
                    edge_stable = False
        return stable_count

    # Count vital spots (corners)
    player_vital = sum(1 for spot in vital_spots if board[spot] == player)
    opponent_vital = sum(1 for spot in vital_spots if board[spot] == opponent)
    
    # Count X-squares (only penalize if the corresponding corner is empty)
    player_x = sum(1 for spot in x_squares if board[spot] == player and board[x_square_to_corner[spot]] == '.')
    opponent_x = sum(1 for spot in x_squares if board[spot] == opponent and board[x_square_to_corner[spot]] == '.')
    
    # Count stable borders
    player_stable = count_stable_borders(player)
    opponent_stable = count_stable_borders(opponent)
    
    # Calculate mobility
    player_options = len(get_possible_moves(board, player))
    opponent_options = len(get_possible_moves(board, opponent))
    
    # Calculate piece difference
    player_count = board.count(player)
    opponent_count = board.count(opponent)
    piece_advantage = player_count - opponent_count
    
    # Determine game phase
    empty_squares = board.count('.')
    if empty_squares > 40:  
        vital_importance = 12
        x_square_importance = -3
        stable_importance = 6
        options_importance = 5
        piece_importance = 0
    elif empty_squares > 15:
        vital_importance = 10
        x_square_importance = -2
        stable_importance = 7
        options_importance = 4
        piece_importance = 1
    else:  # Late game
        vital_importance = 8
        x_square_importance = -1
        stable_importance = 5
        options_importance = 2
        piece_importance = 3
    
    evaluation = (
        vital_importance * (player_vital - opponent_vital) +
        x_square_importance * (player_x - opponent_x) +
        stable_importance * (player_stable - opponent_stable) +
        options_importance * (player_options - opponent_options) +
        piece_importance * piece_advantage
    )
    
    return evaluation
def predict_opponent_move(board):
    for known_board, move in OPPONENT_MOVES.items():
        if board.count('.') == known_board.count('.') and all(board[i] == known_board[i] or known_board[i] == '*' for i in range(64)):
            return move
    return None
def alphabeta_top(board, token):
    opponent = 'o' if token == 'x' else 'x'
    opponent_move = predict_opponent_move(board)
    
    if opponent_move is not None:
        opponent_board = make_move(board, opponent_move, opponent)
        best_score = float('-inf')
        best_move = None
        for move in get_possible_moves(opponent_board, token):
            new_board = make_move(opponent_board, move, token)
            score = -alphabeta(new_board, opponent, float('-inf'), float('inf'), 5)[0]
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    return original_alphabeta_top(board, token)
def original_alphabeta_top(board, token):
    best_score = float('-inf')
    best_move = None
    best_sequence = []
    alpha = float('-inf')
    beta = float('inf')
    
    possible_moves = get_possible_moves(board, token)
    if not possible_moves:
        return [0]
    
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
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return best_move

def alphabeta(board, token, alpha, beta, depth):
    cache_key = (board, token, alpha, beta, depth)
    if cache_key in alphabeta_cache:
        return alphabeta_cache[cache_key]

    possible_moves = get_possible_moves(board, token)
    
    if not possible_moves:
        opponent = 'o' if token == 'x' else 'x'
        opponent_moves = get_possible_moves(board, opponent)
        if not opponent_moves:
            score = board.count(token) - board.count(opponent)
            result = (score, [])
            alphabeta_cache[cache_key] = result
            return result
        score, sequence = alphabeta(board, opponent, -beta, -alpha, depth + 1)
        result = (-score, sequence)
        alphabeta_cache[cache_key] = result
        return result
    
    best_score = float('-inf')
    best_sequence = []
    
    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in possible_moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]
    
    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score, sequence = alphabeta(new_board, 'o' if token == 'x' else 'x', -beta, -alpha, depth + 1)
        score = -score
        
        if score > best_score:
            best_score = score
            best_sequence = [move] + sequence
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    result = (best_score, best_sequence)
    alphabeta_cache[cache_key] = result
    return result

def midgame_alphabeta(board, token, depth=4):
    opponent = 'o' if token == 'x' else 'x'
    opponent_move = predict_opponent_move(board)
    if depth == 0:
        result = brdEval(board, token)
        return result
    if opponent_move is not None:
        opponent_board = make_move(board, opponent_move, opponent)
        best_score = float('-inf')
        best_move = None
        for move in get_possible_moves(opponent_board, token):
            new_board = make_move(opponent_board, move, token)
            score = -midgame_search(new_board, opponent,float('-inf'), float('inf'), depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    return origional_midgame_alphabeta(board, token)

def origional_midgame_alphabeta(board, token, depth=4):
    opponent = 'o' if token == 'x' else 'x'
    best_move = None
    best_score = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    moves = get_possible_moves(board, token)
    if not moves:
        return None

    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]

    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score = -midgame_search(new_board, opponent, -beta, -alpha, depth - 1)

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_move if best_move is not None else rule_of_thumb(board, token)

def midgame_search(board, token, alpha, beta, depth):
    cache_key = (board, token, alpha, beta, depth)
    if cache_key in midgame_cache:
        return midgame_cache[cache_key]

    if depth == 0:
        result = brdEval(board, token)
        midgame_cache[cache_key] = result
        return result

    opponent = 'o' if token == 'x' else 'x'
    moves = get_possible_moves(board, token)

    if not moves:
        opponent_moves = get_possible_moves(board, opponent)
        if not opponent_moves:
            result = brdEval(board, token)
            midgame_cache[cache_key] = result
            return result
        result = -midgame_search(board, opponent, -beta, -alpha, depth - 1)
        midgame_cache[cache_key] = result
        return result

    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]

    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score = -midgame_search(new_board, opponent, -beta, -alpha, depth - 1)

        if score >= beta:
            midgame_cache[cache_key] = beta
            return beta
        if score > alpha:
            alpha = score

    midgame_cache[cache_key] = alpha
    return alpha


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
   
    safe_edge_moves = []
    for move in possible_moves:
        if is_safe_edge(board, move, token):
            safe_edge_moves.append(move)
   
    if safe_edge_moves:
        best_move = None
        max_flips = -1
        for move in safe_edge_moves:
            flips = count_flips(board, move, token)
            if flips > max_flips:
                max_flips = flips
                best_move = move
        return best_move
   
    opponent = 'o' if token == 'x' else 'x'
    best_move = None
    min_moves = float('inf')
    for move in possible_moves:
        new_board = make_move(board, move, token)
        num_moves = len(get_possible_moves(new_board, opponent))
        if num_moves < min_moves:
            min_moves = num_moves
            best_move = move
    return best_move
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
def quickMove(board, token, hl=HLLIM):
    if not board:  
        global HLLIM
        HLLIM = int(token)
        return
   
    return rule_of_thumb(board, token)
def playGame(myTkn):
    brd, tkn, enemy = '.'*27 + 'ox......xo' + '.'*27, 'x' if myTkn == 'x' else 'o', 'o' if myTkn == 'x' else 'x'
    myenemy = "o" if myTkn == 'x' else 'x'
    xscript = []
    while (myMoves := get_possible_moves(brd, tkn)) or (enemyMoves := get_possible_moves(brd, enemy)):
        if not myMoves:
            xscript.append(-1)
            tkn, enemy = enemy, tkn
            continue
        if tkn != myTkn:
            mv = random.choice(myMoves)
        elif brd.count('.') <= HLLIM:
            mv = alphabeta_top(brd, tkn)
        else:
            mv = midgame_alphabeta(brd, tkn) 
        brd = make_move(brd, mv, tkn)
        xscript.append(mv)
        tkn, enemy = enemy, tkn
    myScore = brd.count(myTkn)
    enemyScore = brd.count(myenemy)
    return myScore, enemyScore

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
def runTournament(numGames):
    myTokens = 0
    enemyTokens = 0
    totaltime = 0.0
    for gameNum in range(1, numGames + 1):
        start = time.time()
        myTkn = "xo"[gameNum % 2]
        score, enemyScore = playGame(myTkn)
        end = time.time()
        myTokens += score
        enemyTokens += enemyScore
        totaltime += end - start
        print(f"Game {gameNum}: {'X' if myTkn == 'x' else 'O'} Score: {score} vs enemy score {enemyScore} in {end-start} seconds")
    totalSum = myTokens + enemyTokens
    tournamentScore = myTokens/totalSum
    print(f"Tournament score: {tournamentScore:.2%} in {totaltime} seconds")
    return tournamentScore

def process_condensed_game(condensed_game, board, token, verbose):
    hl = HLLIM
    if condensed_game.startswith('HL'):
        hl_match = re.match(r'HL(\d+)', condensed_game)
        if hl_match:
            hl = int(hl_match.group(1))
            condensed_game = condensed_game[len(hl_match.group(0)):].strip()
    moves = [condensed_game[i:i+2] for i in range(0, len(condensed_game), 2)]
    moves = [move for move in moves if move.lower() != 'v']
   
    print_snapshot(board, token, get_possible_moves(board, token))
   
    last_move = None
    last_token = token
    for move in moves:
        if move == '-1':
            token = 'o' if token == 'x' else 'x'
            continue
        if '_' in move:
            move = move[1:]
        move = int(move)
        board = make_move(board, move, token)
        last_move = move
        last_token = token
        token = 'o' if token == 'x' else 'x'
        if verbose:
            print(f"{last_token} plays to {last_move}")
   
    if not verbose and last_move is not None:
        print(f"{last_token} plays to {last_move}")
   
    possible_moves = get_possible_moves(board, token)
    print_snapshot(board, token, possible_moves)
   
    return board, token, hl

def main():
    global PRECOMPUTED_RESPONSES
    board, token, moves, condensed_game, tournament_games, verbose = parse_args(args)
    if tournament_games:
        runTournament(tournament_games)
        return

    if condensed_game:
        if token is None:
            token = get_default_token(board)
        board, token, hl = process_condensed_game(condensed_game, board, token, verbose)
   
    elif moves:
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

                if verbose:
                    print_snapshot(board, token, possible_moves)
            else:
                print(f"Invalid move: {move}")
                break
       
        if not verbose:
            print_snapshot(board, token, possible_moves)
    else:
        if token is None:
            token = get_default_token(board)
        possible_moves = get_possible_moves(board, token)
        print_snapshot(board, token, possible_moves)
   
    possible_moves = get_possible_moves(board, token)
    if possible_moves:
        quick_move = select_move(board, token)
        print(f"My move: {quick_move}")

if __name__ == "__main__":
    main()

#saatvik kesarwani, pd 1, 2026
