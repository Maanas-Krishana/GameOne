import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

     
def display_board(board):
    print(Fore.CYAN + "\nCurrent Board:")
    for i in range(3):
        print(Fore.YELLOW + " | ".join(board[i * 3:(i + 1) * 3]))
        if i < 2:
            print(Fore.CYAN + "---+---+---")
    time.sleep(0.5)  # Small pause will enhance visibility

def save_game_state(board, player_turn):
    with open("game_state.txt", "w") as file:
        for i in range(3):
            file.write(",".join(board[i * 3:(i + 1) * 3]) + "\n")
        file.write(f"Player Turn: {player_turn}\n")
    print(Fore.GREEN + "Game state saved!")

def save_stats(winner):
    with open("game_stats.txt", "a") as file:
        if winner == "Draw":
            file.write("Game ended in a draw\n")
        else:
            file.write(f"Player {winner} wins\n")
    print(Fore.GREEN + "Stats saved!")

def load_game_state():
    if not os.path.exists("game_state.txt"):
        return None, None

    with open("game_state.txt", "r") as file:
        lines = file.readlines()
        board = []
        for line in lines[:3]:
            board.extend(line.strip().split(","))
        player_turn = int(lines[3].strip().split(": ")[1])
    return board, player_turn

def check_winner(board):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  #3 Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  #3 Columns
        [0, 4, 8], [2, 4, 6]              #2 Diagonals
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] and board[pattern[0]] != "-":
            return board[pattern[0]]
    if all(cell in ["X", "O"] for cell in board):
        return "Draw"
    return None

# Feature to View the Game Statistics
def view_stats():
    if os.path.exists("game_stats.txt"):
        with open("game_stats.txt", "r") as file:
            stats = file.readlines()
            print(Fore.MAGENTA + "\nGame Statistics:")
            for stat in stats:
                print(Fore.YELLOW + stat.strip())
    else:
        print(Fore.RED + "No game stats available.")

# Feature to Restart the Game
def restart_game():
    print(Fore.CYAN + "Restarting game...")
    os.remove("game_state.txt") if os.path.exists("game_state.txt") else None
    tic_tac_toe()
# Game starts from here
def tic_tac_toe():
    print(Fore.MAGENTA + "Welcome to Tic Tac Toe!\n" + Fore.BLUE + "Player 1: X\nPlayer 2: O")

    while True:
        choice = input(Fore.YELLOW + "Do you want to load the previous game state? (yes/ no/ stats/ restart): ").strip().lower()
        if choice == "yes":
            board, player_turn = load_game_state()
            if not board:
                print(Fore.RED + "Game not saved. Starting a new game.")
                board = [str(i) for i in range(1, 10)]
                player_turn = 1
            break
        elif choice == "no":
            board = [str(i) for i in range(1, 10)]
            player_turn = 1
            break
        elif choice == "stats":
            view_stats()
        elif choice == "restart":
            restart_game()
            return
        else:
            print(Fore.RED + "Invalid option. Please choose again.")

    display_board(board)

    while True:
        print(Fore.CYAN + f"Player {player_turn}, it's your turn!")
        try:
            move = int(input(Fore.YELLOW + "Enter your move (1-9): ")) - 1
            if board[move] not in ["X", "O"]:
                board[move] = "X" if player_turn == 1 else "O"
                winner = check_winner(board)
                display_board(board)

                if winner:
                    if winner == "Draw":
                        print(Fore.MAGENTA + "The game is a draw!")
                    else:
                        print(Fore.GREEN + f"Player {player_turn} ({winner}) wins!")
                    save_stats(winner)
                    break

                player_turn = 3 - player_turn  # Switch between first and second player

                save_game_state(board, player_turn)
            else:
                print(Fore.RED + "Invalid. That spot is already taken.")
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid input. Please enter between 1 and 9.")

if __name__ == "__main__":
    tic_tac_toe()
