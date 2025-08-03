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
#global caches with size limits
possible_moves_cache = {}
alphabeta_cache = {}
MAX_CACHE_SIZE = 1000000
CURRENT_BOARD = None
CURRENT_PLAYER = None
search_cache = {}
#global hole limit
HLLIM = 11
MYTKN = ""

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
       #print("No moves possible")
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
    if board.count('.') > 50:
        possible_moves_cache.clear()
    board_key = (board, token)
    if board_key in possible_moves_cache:
        return possible_moves_cache[board_key]

    possible_moves = set()
    opponent = 'o' if token == 'x' else 'x'
    
    #only check empty squares that are adjacent to opponent pieces
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
    """
    Evaluates the Othello board position from the given player's perspective.
    Returns a numeric score where higher values favor the player.
    
    The evaluation combines four key strategic elements with different weights:
    1. Control of vital spots (corners) - Weight: 20
    2. Stable border pieces - Weight: 15
    3. Mobility (number of legal moves) - Weight: 10
    4. Raw piece advantage - Weight: 1
    
    Args:
        board (str): The 64-character string representing the board state
        player (str): The player token ('x' or 'o') to evaluate for
        
    Returns:
        int: The weighted sum of all strategic elements, where higher is better for player
    
    Strategic Elements Explained:
    - Vital Spots: Corners (positions 0,7,56,63) are most valuable as they can never be flipped
    - Stable Borders: Edge pieces that cannot be flipped due to their position
    - Mobility: Difference in number of legal moves between player and opponent
    - Piece Advantage: Raw difference in piece count between player and opponent
    
    The final score is calculated as:
    score = 20 * (player_corners - opponent_corners) +
            15 * (player_stable_edges - opponent_stable_edges) +
            10 * (player_moves - opponent_moves) +
            1 * (player_pieces - opponent_pieces)
    """
    opponent = 'o' if player == 'x' else 'x'
    
    #define key positions
    vital_spots = {0, 7, 56, 63}  #corners
    
    def count_stable_borders(token):
        stable_count = 0
        for edge in [range(8), range(0, 57, 8), range(7, 64, 8), range(56, 64)]:
            for pos in edge:
                if board[pos] == token and is_safe_edge(board, pos, token):
                    stable_count += 1
        return stable_count

    #count vital spots
    player_vital = sum(1 for spot in vital_spots if board[spot] == player)
    opponent_vital = sum(1 for spot in vital_spots if board[spot] == opponent)
    
    #count stable borders
    player_stable = count_stable_borders(player)
    opponent_stable = count_stable_borders(opponent)
    
    #calculate mobility
    player_options = len(get_possible_moves(board, player))
    opponent_options = len(get_possible_moves(board, opponent))
    
    #calculate piece difference
    playercount = board.count(player)
    oppcount = board.count(opponent)
    piece_advantage = playercount - oppcount
    
    #importance factors
    vital_importance = 20
    stable_importance = 15
    options_importance = 10
    piece_importance = 1
    
    #calculate final score
    evaluation = (
        vital_importance * (player_vital - opponent_vital) +
        stable_importance * (player_stable - opponent_stable) +
        options_importance * (player_options - opponent_options) +
        piece_importance * piece_advantage
    )
    
    return evaluation

def alphabeta_top(board, token):
    best_score = float('-inf')
    best_move = None
    best_sequence = []
    alpha = float('-inf')
    beta = float('inf')
    
    possible_moves = get_possible_moves(board, token)
    if not possible_moves:
        return [0]
    
    #sort moves by initial evaluation
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
            #print(f"Score: {best_score}; Move: {best_move}")
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return best_move

def alphabeta(board, token, alpha, beta, depth):
    possible_moves = get_possible_moves(board, token)
    
    if not possible_moves:
        opponent = 'o' if token == 'x' else 'x'
        opponent_moves = get_possible_moves(board, opponent)
        if not opponent_moves:
            #game is over, count pieces
            score = board.count(token) - board.count(opponent)
            return score, []
        #must pass
        score, sequence = alphabeta(board, opponent, -beta, -alpha, depth + 1)
        return -score, sequence
    
    best_score = float('-inf')
    best_sequence = []
    
    #sort moves by evaluation
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
    
    return best_score, best_sequence



def midgame_alphabeta(board, token, depth=4):
    #depth of 4 in reality because you subtract 1
    opponent = 'o' if token == 'x' else 'x'
    best_move = None
    best_score = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    
    moves = get_possible_moves(board, token)
    if not moves:
        return None

    for move in moves:
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
    if depth == 0:
        return brdEval(board, token)

    possible_moves = get_possible_moves(board, token)
    
    if not possible_moves:
        opponent = 'o' if token == 'x' else 'x'
        opponent_moves = get_possible_moves(board, opponent)
        if not opponent_moves:
            #game is over, count pieces
            score = board.count(token) - board.count(opponent)
            return score
        #must pass
        score = midgame_search(board, opponent, -beta, -alpha, depth - 1)
        return -score
    
    best_score = float('-inf')    
    #sort moves by evaluation
    moves_with_scores = [(move, evaluate_position(board, move, token)) for move in possible_moves]
    sorted_moves = [move for move, _ in sorted(moves_with_scores, key=lambda x: x[1], reverse=True)]
    
    for move in sorted_moves:
        new_board = make_move(board, move, token)
        score = midgame_search(new_board, 'o' if token == 'x' else 'x', -beta, -alpha, depth - 1)
        score = -score
        
        if score > best_score:
            best_score = score
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    
    return best_score




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
    if not board:  #set hole limit
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
            mv = midgame_alphabeta(brd, tkn) # Use depth=4
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
        '''
        print(f"Adding {score} to My score")
        print(f"Adding {enemyScore} to My enemy score")
        print(enemyTokens)
        print(myTokens)
        '''
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
        if move == '_1':
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
    board, token, moves, condensed_game, tournament_games, verbose = parse_args(args)
    hl = HLLIM

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
        quick_move = quickMove(board, token, hl)
        print(f"My move: {quick_move}")
        empty_positions = board.count('.')
        if empty_positions <= HLLIM:
            start = time.time()
            result = alphabeta_top(board, token)
            end = time.time()
            print(f"Alphabeta move: {result}")
            print(f"Time taken {end-start}")
        else:
            start = time.time()
            result = midgame_alphabeta(board, token)
            end = time.time()
            print(f"Midgame Alpha-Beta move: {result}")
            print(f"Time taken {end-start}")

if __name__ == "__main__":
    main()

#saatvik kesarwani, pd 1, 2026