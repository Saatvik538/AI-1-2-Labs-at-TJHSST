import sys; args = sys.argv[1:]
import time

def setGlobals(puzzle):
    global N, SYMSET, constraint_sets, SYMBOL_VALUES, IDXTOCS, NBRPOS
    
    N = int(len(puzzle) ** 0.5)
    h = int(N ** 0.5)
    w = N // h
    
    puzzle_symbols = sorted(set(puzzle) - {'.'})
    SYMSET = puzzle_symbols[:N]
    symnext = '1'
    while len(SYMSET) < N:
        if symnext not in SYMSET:
            SYMSET.append(symnext)
        symnext = str(int(symnext)+1)
    
    SYMBOL_VALUES = {sym: ord(sym) - min(ord(s) for s in SYMSET) for sym in SYMSET}
    
    constraint_sets = []
    
    for i in range(N):
        constraint_sets.append(set(range(i * N, (i + 1) * N)))
    
    for i in range(N):
        constraint_sets.append(set(range(i, N * N, N)))
    
    for i in range(0, N, h):
        for j in range(0, N, w):
            subblock = set()
            for x in range(h):
                for y in range(w):
                    subblock.add(i * N + j + x * N + y)
            constraint_sets.append(subblock)
    IDXTOCS = [[] for _ in range(N*N)]
    for idx, cs in enumerate(constraint_sets):
        for pos in cs:
            IDXTOCS[pos].append(idx)
    
    NBRPOS = [set() for _ in range(N*N)]
    for pos in range(N*N):
        for cs_idx in IDXTOCS[pos]:
            NBRPOS[pos].update(constraint_sets[cs_idx])
        NBRPOS[pos].remove(pos)

def isInvalid(pzl, pos):
    sym = pzl[pos]
    for cs_idx in IDXTOCS[pos]:
        if sym in [pzl[i] for i in constraint_sets[cs_idx] if i != pos and pzl[i] != '.']:
            return True
    return False

def findOptimalSymbol(pzl, possibles):
    best_positions = []
    min_positions = float('inf')
    chosen_symbol = None

    for cs in constraint_sets:
        empty_positions = [pos for pos in cs if pzl[pos] == '.']
        if not empty_positions:
            continue
        used_symbols = {pzl[pos] for pos in cs if pzl[pos] != '.'}
        for sym in SYMSET:
            if sym in used_symbols:
                continue
                
            valid_positions = [pos for pos in empty_positions if sym in possibles[pos]]
            num_positions = len(valid_positions)
            
            if num_positions == 0:
                continue
            
            if num_positions == 1:
                return valid_positions, sym
                
            if num_positions < min_positions:
                min_positions = num_positions
                best_positions = valid_positions
                chosen_symbol = sym

    return best_positions, chosen_symbol

def checkSum(pzl):
    return sum(SYMBOL_VALUES[c] for c in pzl if c != '.')

def initializePossibles(pzl):
    possibles = [set(SYMSET) for _ in range(len(pzl))]
    for i, char in enumerate(pzl):
        if char != '.':
            possibles[i] = set()
            updatePossibles(possibles, i, char)
    return possibles

def updatePossibles(possibles, pos, sym):
    removed = {}
    for nbr in NBRPOS[pos]:
        if sym in possibles[nbr]:
            possibles[nbr].remove(sym)
            if nbr not in removed:
                removed[nbr] = set()
            removed[nbr].add(sym)
    return removed

def restorePossibles(possibles, removed):
    for pos, symbols in removed.items():
        possibles[pos].update(symbols)

def bruteForce(pzl, possibles):
    if '.' not in pzl:
        return pzl

    positions, symbol = findOptimalSymbol(pzl, possibles)
    if symbol:
        for pos in positions:
            new_pzl = pzl[:pos] + symbol + pzl[pos + 1:]
            removed = updatePossibles(possibles, pos, symbol)
            
            if not isInvalid(new_pzl, pos):
                result = bruteForce(new_pzl, possibles)
                if result:
                    return result
            
            restorePossibles(possibles, removed)
            possibles[pos].add(symbol)
        return ""
    min_possibilities = float('inf')
    best_pos = -1
    for i, char in enumerate(pzl):
        if char == '.':
            if len(possibles[i]) < min_possibilities:
                min_possibilities = len(possibles[i])
                best_pos = i
                if min_possibilities == 1:
                    break

    for choice in list(possibles[best_pos]):
        new_pzl = pzl[:best_pos] + choice + pzl[best_pos + 1:]
        removed = updatePossibles(possibles, best_pos, choice)
        
        if not isInvalid(new_pzl, best_pos):
            result = bruteForce(new_pzl, possibles)
            if result:
                return result
        
        restorePossibles(possibles, removed)
        possibles[best_pos].add(choice)

    return ""

def print_2d_sudoku(puzzle):
    N = int(len(puzzle) ** 0.5)
    h = int(N ** 0.5)
    w = N // h
    
    for i in range(N):
        if i > 0 and i % h == 0:
            print('-' * (N + w - 1))
        row = puzzle[i * N : (i + 1) * N]
        print(' '.join(row[j:j+w] for j in range(0, N, w)))

def main():
    if len(args[0]) in [9*9, 12*12, 16*16, 25*25]:
        puzzles = [args[0]]
    else: 
        with open(args[0]) as f:
            puzzles = f.read().strip().split('\n')

    for idx, puzzle in enumerate(puzzles, 1):
        setGlobals(puzzle)
        print(f"{idx}: {puzzle}")
        
        start_time = time.time()
        possibles = initializePossibles(puzzle)
        solution = bruteForce(puzzle, possibles)
        end_time = time.time()
        
        if solution and idx < 10:
            print(f"{solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        elif solution and idx < 100:
            print(f"{solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        elif solution and idx >= 100:
            print(f"{solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        else:
            print("No solution found")
        
        if len(puzzles) == 1:
            print("\nOriginal puzzle:")
            print_2d_sudoku(puzzle)
            print("\nSolution:")
            print_2d_sudoku(solution)

if __name__ == "__main__":
    main()