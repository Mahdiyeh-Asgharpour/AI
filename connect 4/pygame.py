import numpy as np
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))
    print("-----------------------------")


def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def get_valid_moves(board):
    valid_moves = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_moves.append(col)
    return valid_moves

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

def evaluate_window(window, piece):
    score = 0
    opponent_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def is_terminal_node(board):
    return winning_move(board, b_piece) or winning_move(board, p_piece) or len(get_valid_moves(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_moves = get_valid_moves(board)
    terminal = is_terminal_node(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board,b_piece):  # AI wins
                return (None, 10000000000000)
            elif winning_move(board, p_piece):  # Player wins
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)

        else:  # Depth is 0
            return (None, score_position(board, b_piece))
    if maximizingPlayer:
        value = float("-inf")
        best_column = random.choice(valid_moves)

        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, b_piece)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                best_column = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return best_column, value
    else:
        value = float("inf")
        best_column = random.choice(valid_moves)

        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, p_piece)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                best_column = col

            beta = min(beta, value)

            if alpha >= beta:
                break

        return best_column, value

board = create_board()
print_board(board)
game_over = False
turn = 0
x=input("choose 1 or 2?")
if int(x)==2:
    p_piece = 2
    b_piece = 1
else:
    p_piece = 1
    b_piece = 2
while not game_over:
    # print(str(turn))
    if turn == 0:  # Player's turn
        col = int(input("Player, make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, p_piece)

            if winning_move(board,  p_piece):
                print("Player %d wins!", p_piece)
                print("score:"+str(score_position(board, p_piece)))
                game_over = True

    else:  # AI's turn
        
        col, _ = minimax(board, 4, float("-inf"), float("inf"), True)
        print("AI :"+str(col))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, b_piece)

            if winning_move(board,  b_piece):
                print("score:"+str(score_position(board, b_piece)))
                print("AI wins!")
                game_over = True

    print_board(board)
    turn += 1
    turn %= 2