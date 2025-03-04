import random


board = [" " for _ in range(9)]
human = "X"
computer = "O"

# Check for a win
def check_winner(board, player):
    win_patterns = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                    (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                    (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_patterns)

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_winner(board, computer):
        return 1
    elif check_winner(board, human):
        return -1
    elif " " not in board:
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = computer
                best = max(best, minimax(board, depth + 1, False))
                board[i] = " "
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = human
                best = min(best, minimax(board, depth + 1, True))
                board[i] = " "
        return best

# AI Move
def best_move(board):
     # 30% chance to make a random move instead of perfect move
    if random.random() < 0.3:
        available_moves = [i for i in range(9) if board[i] == " "]
        return random.choice(available_moves)
    
    # Otherwise, use  Minimax to find the best move
    best_val = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = computer
            move_val = minimax(board, 0, False)
            board[i] = " "
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

# Display the board
def print_board(board):
    for i in range(0, 9, 3):
        print("|".join(board[i:i+3]))
        if i < 6:
            print("-" * 5)
def reset_board():
    return [" " for _ in range(9)]

# Main game loop
def play_game():
    print(" 🎮 Welcome to Tic-Tac-Toe! 🎮 ".center(50,"*"))
    print("\nHere are the instructions:")
    print("\n1.You are X, and the computer is O.")
    print("\n2.The game board is numbered 1-9 like this:")
    print("\n     1 | 2 | 3")
    print("     - - - - -")
    print("     4 | 5 | 6")
    print("     - - - - -")
    print("     7 | 8 | 9")
    print("\n💡 Enter a number (1-9) to place your mark (X).")
    print("\n3.Win by getting 3 in a row (horizontally, vertically, or diagonally).")
    print("\n4.If the board is full and no one wins, it's a tie!")
    print("\nCan you outsmart the Computer? Good luck! 🔥")

    while True:
        board = reset_board()
        while " " in board:
            # Human's turn
            print_board(board)
            move = int(input("Enter your move (1-9): "))-1
            if board[move] == " ":
                board[move] = human
            else:
                print("Invalid move! Try again.")
                continue
            
            if check_winner(board, human):
                print_board(board)
                print("You win!🎉")
                return True
            
            # Computer's turn
            if " " in board:
                move = best_move(board)
                board[move] = computer
                if check_winner(board, computer):
                    print_board(board)
                    print("Computer wins! You won't be getting any hints for now.")
                    return False
            
        print_board(board)
        print("It's a tie!")

    # Ask if the player wants to play again
        again = input("Do you want to play again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing! 👋")
            break

