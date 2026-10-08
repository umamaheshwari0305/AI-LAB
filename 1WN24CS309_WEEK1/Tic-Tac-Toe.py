import math

# Print the board
def print_board(board):
    print()
    for i in range(3):
        print(" | ".join(board[i * 3:(i + 1) * 3]))
        if i < 2:
            print("--+---+--")
    print()


# Check whether a player has won
def check_winner(board, player):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


# Check if board is full
def is_draw(board):
    return all(position != " " for position in board)


# Minimax algorithm
def minimax(board, is_maximizing):
    # Computer wins
    if check_winner(board, "O"):
        return 1

    # Human wins
    if check_winner(board, "X"):
        return -1

    # Draw
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(best_score, score)

        return best_score


# Find the best move for computer
def computer_move(board):
    best_score = -math.inf
    best_move = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# Main game
def play_game():
    board = [" "] * 9

    print("TIC-TAC-TOE")
    print("You are X")
    print("Computer is O")

    print("\nPosition numbers:")
    print("1 | 2 | 3")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("7 | 8 | 9")

    while True:
        print_board(board)

        # Human move
        try:
            move = int(input("Enter your move (1-9): ")) - 1

            if move < 0 or move > 8 or board[move] != " ":
                print("Invalid move! Try again.")
                continue

            board[move] = "X"

        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue

        # Check human win
        if check_winner(board, "X"):
            print_board(board)
            print("You win!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Computer move
        print("Computer is thinking...")
        move = computer_move(board)
        board[move] = "O"

        # Check computer win
        if check_winner(board, "O"):
            print_board(board)
            print("Computer wins!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break


# Start the game
play_game()
