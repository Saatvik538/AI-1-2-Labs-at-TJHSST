import sys; args = sys.argv[1:]
import time

def setGlobals(puzzle):
    global HEIGHT, WIDTH, BLOCKS, TOTAL_AREA
    parts = puzzle.replace('X', 'x').split()
   
    if 'x' in parts[0]:
        HEIGHT, WIDTH = map(int, parts[0].split('x'))
    else:
        HEIGHT, WIDTH = int(parts[0]), int(parts[1])
        parts = parts[1:]

    BLOCKS = []
    i = 1
    while i < len(parts):
        if 'x' in parts[i]:
            h, w = map(int, parts[i].split('x'))
            BLOCKS.append((h, w))
            i += 1
        else:
            h, w = int(parts[i]), int(parts[i + 1])
            BLOCKS.append((h, w))
            i += 2
   
    TOTAL_AREA = sum(h * w for h, w in BLOCKS)

def isInvalid():
    if TOTAL_AREA > HEIGHT * WIDTH:
        return True
   
    for h, w in BLOCKS:
        if h > HEIGHT and w > HEIGHT:
            return True
        if w > WIDTH and h > WIDTH:
            return True
    return False

def can_place_block(grid, y, x, h, w):
    if y + h > HEIGHT or x + w > WIDTH:
        return False
       
    for i in range(h):
        for j in range(w):
            if grid[y + i][x + j] != 0:
                return False
    return True

def place_block(grid, y, x, h, w, value):
    for i in range(h):
        for j in range(w):
            grid[y + i][x + j] = value

def find_empty_cell(grid):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == 0:
                return y, x
    return None

def get_block_area(block_idx):
    h, w = BLOCKS[block_idx]
    return h * w

def calculate_min_area_needed(remaining_blocks):
    return sum(h * w for idx, (h, w) in enumerate(BLOCKS) if idx in remaining_blocks)

def bruteForce(grid, used_blocks, remaining_blocks):
    if len(remaining_blocks) == 0:
        return True
    
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return False

    y, x = empty_cell
    
    empty_area = sum(row.count(0) for row in grid)
    if calculate_min_area_needed(remaining_blocks) > empty_area:
        return False
    
    sorted_blocks = sorted(remaining_blocks, 
                         key=get_block_area,
                         reverse=True)
    
    for block_idx in sorted_blocks:
        h, w = BLOCKS[block_idx]
        for curr_h, curr_w in [(h, w), (w, h)]:
            if can_place_block(grid, y, x, curr_h, curr_w):
                place_block(grid, y, x, curr_h, curr_w, block_idx + 1)
                new_remaining = remaining_blocks - {block_idx}
                used_blocks.add(block_idx + 1)
                if bruteForce(grid, used_blocks, new_remaining):
                    return True
                
                place_block(grid, y, x, curr_h, curr_w, 0)
    
    if can_place_block(grid, y, x, 1, 1):
        place_block(grid, y, x, 1, 1, -1)
        if bruteForce(grid, used_blocks, remaining_blocks):
            return True
        place_block(grid, y, x, 1, 1, 0)
    
    return False

def get_block_dimensions(grid, y, x):
    value = grid[y][x]
    if value == -1:
        return 1, 1
        
    h, w = 1, 1
    while y + h < HEIGHT and grid[y + h][x] == value:
        h += 1
    while x + w < WIDTH and grid[y][x + w] == value:
        w += 1
    return h, w

def main():
    puzzle = " ".join(args)
    print(f"Puzzle: {puzzle}")
   
    start_time = time.time()
    setGlobals(puzzle)
   
    if isInvalid():
        print("No solution")
        return
   
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    used_blocks = set()
    remaining_blocks = set(range(len(BLOCKS)))
   
    if bruteForce(grid, used_blocks, remaining_blocks):
        print("Decomposition:", end=" ")
        solution = []
        seen_positions = set()
        
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (y, x) not in seen_positions:
                    h, w = get_block_dimensions(grid, y, x)
                    solution.append((h, w))
                    
                    for i in range(h):
                        for j in range(w):
                            seen_positions.add((y + i, x + j))
        
        print(" ".join(f"{h}x{w}" for h, w in solution))
        print(f"Time: {time.time() - start_time:.1f}s")
    else:
        print("No solution")

if __name__ == "__main__":
    main()