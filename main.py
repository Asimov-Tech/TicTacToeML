import numpy as np
import random
import pickle  # For saving/loading Q-table

# Initialize game state
turns = 0
board = np.zeros((3, 3), dtype=int)
current_player = 1  # Player 1 starts

def display_board(board):
    print("\nCurrent board:")
    for row in board:
        display_row = []
        for cell in row:
            if cell == 0:
                display_row.append(".")
            elif cell == 1:
                display_row.append("X")
            elif cell == 2:
                display_row.append("O")
        print(" ".join(display_row))
    print()

def check_legal_move(move) -> bool:
    if 0 <= move < 3:
        return True
    else:
        print("Invalid input. Please enter a number between 0 and 2.")
        return False

def check_if_occupied(row, col, board) -> bool:
    if board[row][col] != 0:
        print("This spot is already occupied. Try again.")
        return True  # Spot is occupied
    else:
        return False  # Spot is free

def check_win(board):
    # Check horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return True

    # Check vertical
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != 0:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return True
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return True

    return False  # No win yet

def get_player_move(player):
    while True:
        try:
            row = int(input(f"Player {player} ({'X' if player ==1 else 'O'}), enter row (0, 1, or 2): "))
            if not check_legal_move(row):
                continue
            col = int(input(f"Player {player} ({'X' if player ==1 else 'O'}), enter column (0, 1, or 2): "))
            if not check_legal_move(col):
                continue
            return row, col
        except ValueError:
            print("Invalid input. Please enter integers between 0 and 2.")

class QLearningAgent:
    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.2):
        self.Q = {}  # Q-table as a dictionary
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_Q(self, state, action):
        return self.Q.get((state, action), 0.0)

    def choose_action(self, state, available_actions):
        if random.uniform(0,1) < self.epsilon:
            # Explore: choose a random action
            action = random.choice(available_actions)
        else:
            # Exploit: choose the best action based on current Q-values
            Q_values = [self.get_Q(state, a) for a in available_actions]
            max_Q = max(Q_values)
            # In case multiple actions have the same max Q-value
            actions_with_max_Q = [a for a, q in zip(available_actions, Q_values) if q == max_Q]
            action = random.choice(actions_with_max_Q)
        return action

    def learn(self, state, action, reward, next_state, next_available_actions, done):
        old_Q = self.get_Q(state, action)
        if done:
            target = reward
        else:
            future_Q = [self.get_Q(next_state, a) for a in next_available_actions]
            target = reward + self.gamma * max(future_Q, default=0)
        self.Q[(state, action)] = old_Q + self.alpha * (target - old_Q)

    def save_Q(self, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self.Q, f)

    def load_Q(self, filename="q_table.pkl"):
        try:
            with open(filename, 'rb') as f:
                self.Q = pickle.load(f)
        except FileNotFoundError:
            print("Q-table file not found. Starting with an empty Q-table.")

def train_agent(agent, episodes=50000):
    for episode in range(episodes):
        # Initialize the game
        board = np.zeros((3, 3), dtype=int)
        turns = 0
        done = False
        current_player = 1  # Agent starts first

        while not done:
            state = tuple(board.flatten())
            available_actions = [i for i in range(9) if board.flatten()[i] == 0]

            if current_player == 1:
                # Agent's turn
                action = agent.choose_action(state, available_actions)
                row, col = divmod(action, 3)
                board[row][col] = current_player
                turns += 1

                if check_win(board):
                    reward = 1  # Agent wins
                    agent.learn(state, action, reward, None, [], True)
                    done = True
                elif turns == 9:
                    reward = 0  # Draw
                    agent.learn(state, action, reward, None, [], True)
                    done = True
                else:
                    # Opponent's turn next
                    next_available_actions = [i for i in range(9) if board.flatten()[i] == 0]
                    agent.learn(state, action, 0, tuple(board.flatten()), next_available_actions, False)
                    current_player = 2
            else:
                # Opponent's turn (Random)
                opp_action = random.choice(available_actions)
                board[opp_action // 3][opp_action % 3] = current_player
                turns += 1

                if check_win(board):
                    reward = -1  # Agent loses
                    agent.learn(state, action, reward, None, [], True)
                    done = True
                elif turns == 9:
                    reward = 0  # Draw
                    agent.learn(state, action, reward, None, [], True)
                    done = True
                else:
                    current_player = 1  # Agent's turn

        # Optional: Print progress
        if (episode+1) % 10000 == 0:
            print(f"Episode {episode+1}/{episodes} completed.")

    # Save the trained Q-table
    agent.save_Q()
    print("Training completed and Q-table saved.")

def play_against_agent(agent):
    board = np.zeros((3, 3), dtype=int)
    turns = 0
    current_player = 1  # Agent starts first

    while True:
        display_board(board)
        state = tuple(board.flatten())
        available_actions = [i for i in range(9) if board.flatten()[i] == 0]

        if current_player == 1:
            # Agent's turn
            action = agent.choose_action(state, available_actions)
            row, col = divmod(action, 3)
            board[row][col] = current_player
            turns += 1

            if check_win(board):
                display_board(board)
                print(f"Agent (X) wins!")
                break
            elif turns == 9:
                display_board(board)
                print("It's a draw!")
                break
            else:
                current_player = 2
        else:
            # Human player's turn
            row, col = get_player_move(current_player)
            action = row * 3 + col
            if board[row][col] != 0:
                print("Spot occupied! Choose another move.")
                continue
            board[row][col] = current_player
            turns += 1

            if check_win(board):
                display_board(board)
                print(f"Player {current_player} ({'O'}) wins!")
                break
            elif turns == 9:
                display_board(board)
                print("It's a draw!")
                break
            else:
                current_player = 1

if __name__ == "__main__":
    agent = QLearningAgent()
    # Attempt to load existing Q-table
    agent.load_Q()

    while True:
        print("\n--- Tic-Tac-Toe with Q-Learning Agent ---")
        print("1. Train Agent")
        print("2. Play Against Agent")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                episodes = int(input("Enter number of training episodes (e.g., 50000): "))
            except ValueError:
                print("Invalid input. Using default 50000 episodes.")
                episodes = 50000
            train_agent(agent, episodes=episodes)
        elif choice == '2':
            # Set epsilon to 0 for exploitation (use learned policy)
            original_epsilon = agent.epsilon
            agent.epsilon = 0
            play_against_agent(agent)
            agent.epsilon = original_epsilon
        elif choice == '3':
            print("Exiting the game.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
