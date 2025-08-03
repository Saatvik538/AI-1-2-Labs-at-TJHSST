import sys; args = sys.argv[1:]

def display_board(board, possible_moves=None):
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if possible_moves and index in possible_moves:
                print('*', end='')
            else:
                print(board[index], end='')
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

    return possible_moves

def main():
    board = '.' * 27 + 'ox......xo' + '.' * 27
    tokenToMove = ''
    if args and args[0] and len(args[0]) == 64:
        board = args[0].lower() 

    if len(args) < 2:
        num_tokens = 64 - board.count('.')
        if num_tokens % 2 == 0:
            tokenToMove = 'x'
        else:
            tokenToMove = 'o'
    else:
        tokenToMove = args[1].lower()

    possible_moves = get_possible_moves(board, tokenToMove)
    print (possible_moves if possible_moves else "No moves possible")
    display_board(board, possible_moves)
    if possible_moves:
        print(f"Possible moves for {tokenToMove}: {', '.join(map(str, sorted(possible_moves)))}")
    else:
        print("No moves possible")

if __name__ == "__main__":
    main()