import matplotlib.pyplot as plt
import numpy as np

# 八皇后问题的解决方案
def solve_n_queens(n):
    solutions = []
    board = [-1] * n
    place_queens(board, 0, n, solutions)
    return solutions

def place_queens(board, row, n, solutions):
    if row == n:
        solutions.append(board.copy())
    else:
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                place_queens(board, row + 1, n, solutions)
                board[row] = -1

def is_safe(board, row, col):
    for r in range(row):
        if board[r] == col or \
           board[r] - r == col - row or \
           board[r] + r == col + row:
            return False
    return True

# 可视化解决方案
def visualize_solution(solution):
    n = len(solution)
    board = np.zeros((n, n))

    for row, col in enumerate(solution):
        board[row, col] = 1

    fig, ax = plt.subplots()
    ax.matshow(board, cmap=plt.cm.Blues)

    for i in range(n):
        for j in range(n):
            if board[i, j] == 1:
                ax.text(j, i, 'Q', va='center', ha='center', color='black', fontsize=20)

    plt.xticks([])
    plt.yticks([])
    plt.show()

# 主程序
n = 8
solutions = solve_n_queens(n)

print(f"找到 {len(solutions)} 种解决方案。")

# 可视化第一种解决方案
visualize_solution(solutions[0])
