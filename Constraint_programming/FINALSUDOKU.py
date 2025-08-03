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

def findBestChoices(pzl, possibles):
    best_choices = []
    min_positions = float('inf')
    
    for pos, syms in enumerate(possibles):
        if pzl[pos] == '.' and len(syms) == 1:
            return [(pos, list(syms)[0])]
    
    for cs in constraint_sets:
        empty_positions = [pos for pos in cs if pzl[pos] == '.']
        if not empty_positions:
            continue
            
        used_symbols = {pzl[pos] for pos in cs if pzl[pos] != '.'}
        needed_symbols = set(SYMSET) - used_symbols
        
        for sym in needed_symbols:
            valid_positions = [pos for pos in empty_positions if sym in possibles[pos]]
            if len(valid_positions) == 1:
                return [(valid_positions[0], sym)]
            elif len(valid_positions) < min_positions:
                min_positions = len(valid_positions)
                best_choices = [(pos, sym) for pos in valid_positions]
    
    if not best_choices:
        min_possibilities = float('inf')
        best_pos = -1
        for pos, syms in enumerate(possibles):
            if pzl[pos] == '.' and len(syms) < min_possibilities:
                min_possibilities = len(syms)
                best_pos = pos
                if min_possibilities <= 2:
                    break
        best_choices = [(best_pos, sym) for sym in possibles[best_pos]]
    
    return best_choices

def disseminateQ(pzl, possibles, queue):
    while queue:
        pos, sym = queue.pop(0)
        if pzl[pos] != '.':
            continue
            
        pzl = pzl[:pos] + sym + pzl[pos+1:]
        possibles[pos] = set()

        for nbr in NBRPOS[pos]:
            if sym in possibles[nbr]:
                possibles[nbr].remove(sym)
                if pzl[nbr] == '.' and len(possibles[nbr]) == 1:
                    sym_to_use = list(possibles[nbr])[0]
                    queue.append((nbr, sym_to_use))
                elif len(possibles[nbr]) == 0 and pzl[nbr] == '.':
                    return None
        
        for cs_idx in IDXTOCS[pos]:
            cs = constraint_sets[cs_idx]
            empty = [p for p in cs if pzl[p] == '.']
            if not empty:
                continue
            
            used = {pzl[p] for p in cs if pzl[p] != '.'}
            for needed_sym in set(SYMSET) - used:
                valid = [p for p in empty if needed_sym in possibles[p]]
                if len(valid) == 1:
                    queue.append((valid[0], needed_sym))
                elif len(valid) == 0:
                    return None
    
    return pzl

def bruteForce(pzl, possibles):
    if '.' not in pzl:
        return pzl
        
    choices = findBestChoices(pzl, possibles)
    
    for pos, sym in choices:
        pzl_copy = pzl
        possibles_copy = [p.copy() for p in possibles]
        new_pzl = disseminateQ(pzl_copy, possibles_copy, [(pos, sym)])
        
        if new_pzl:
            result = bruteForce(new_pzl, possibles_copy)
            if result:
                return result
    
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
            print(f"   {solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        elif solution and idx < 100:
            print(f"    {solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        elif solution and idx >= 100:
            print(f"     {solution} {checkSum(solution)} {end_time - start_time:.1f}s")
        else:
            print("No solution found")
        
        if len(puzzles) == 1:
            print("\nOriginal puzzle:")
            print_2d_sudoku(puzzle)
            print("\nSolution:")
            print_2d_sudoku(solution)

if __name__ == "__main__":
    main()