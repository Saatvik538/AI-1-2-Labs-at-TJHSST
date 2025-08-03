import sys; arg = sys.argv[1]

def create_constraint_sets(n):
    constrained_sets = []

    for i in range(n):
        row = [i*n + j for j in range(n)]
        constrained_sets.append(row)

    for i in range(n):
        column = [j*n + i for j in range(n)]
        constrained_sets.append(column)

    for i in range(2*n - 1):
        diag = [j*n + (i-j) for j in range(max(0, i-n+1), min(i+1, n))]
        if diag:
            constrained_sets.append(diag)

    for i in range(2*n - 1):
        diag = [j*n + (n-1-(i-j)) for j in range(max(0, i-n+1), min(i+1, n))]
        if diag:
            constrained_sets.append(diag)

    return constrained_sets

def isInvalid(pzl, queen, constraint_sets):
    for constraint in constraint_sets:
        if sum(1 for i in constraint if pzl[i] == queen) > 1:
            return True
    return False

def isSolved(pzl, N, queen):
    return pzl.count(queen) == N
    

def bruteForce(pzl, N, queen, constraint_sets):
    if isInvalid(pzl, queen, constraint_sets):
        return ""
    if isSolved(pzl, N, queen):
        return pzl

    i = pzl.find('.')
    if i == -1:
        return "" 

    for choice in (queen, 'X'):
        subPzl = pzl[:i] + choice + pzl[i + 1:]
        bF = bruteForce(subPzl, N, queen, constraint_sets)
        if bF:
            return bF

    return ""

def print_solution(solution, N):
    solution = solution.replace('X', '.')
    print(f"Solution: {solution}")
    for i in range(N):
        print(solution[i*N:(i+1)*N])

def main():
    if arg.isdigit():
        N = int(arg)
        initial_board = '.' * (N * N)
        queen = 'Q'
    else:
        N = int(len(arg) ** 0.5)
        initial_board = arg
        queen = next((c for c in arg if c != '.'), 'Q')

    constraint_sets = create_constraint_sets(N)

    if isInvalid(initial_board, queen, constraint_sets):
        print("No solution possible")
        return

    solution = bruteForce(initial_board, N, queen, constraint_sets)

    if solution:
        print_solution(solution, N)
    else:
        print("No solution possible")

if __name__ == "__main__":
    main()