import sys; args = sys.argv[1:]
import re

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
    possible_moves = []
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
                        possible_moves.append(i)
                        break
                    x, y = x + dx, y + dy

    return possible_moves

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

def print_snapshot(board, token, possible_moves):
    display_board(board, possible_moves)
    print()
    print(board, board.count('x') + board.count('X'), "/", board.count('o') + board.count('O'))
    if possible_moves:
        print(f"Possible moves for {token}: {', '.join(map(str, sorted(possible_moves)))}")
    else:
        print("No moves possible")
    print()

def get_default_token(board):
    x_moves = get_possible_moves(board, 'x')
    o_moves = get_possible_moves(board, 'o')
    if not x_moves and o_moves:
        return 'o'
    elif not o_moves and x_moves:
        return 'x'
    else:
        return 'x' if board.count('.') % 2 == 0 else 'o'

def parse_move(move_input):
    if move_input.isdigit():
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

    for arg in args:
        if re.match(board_pattern, arg):
            board = arg.lower()
        elif re.match(token_pattern, arg):
            token = arg.lower()
        elif re.match(move_pattern, arg):
            move = parse_move(arg)
            if move is not None:
                moves.append(move)

    return board, token, moves

def main():
    board, token, moves = parse_args(args)

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

if __name__ == "__main__":
    main()