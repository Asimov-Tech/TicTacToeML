import numpy as np

state = 0
turns = 0
board = np.zeros((3, 3))

def input_move(row, col, player):
    board[row][col] = player
    
    print(board)


# TODO Make it so that it takes 1 and 3
def check_legal_move(move)->(bool):
    if move < 3 or move < 0:
        
        return True
    else:
        print("Invalid Move")
        return False
    
def check_if_occupied(row, col, board)-> bool:
    if board[row,col] == 0:
         return True
    else:
         return False
     




def check_win(board):
    # Check horizontal 
    for i in range (3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
                if board[i][2] != 0:
                    return True 
        
    # Check vertical 
    for j in range (3):
            if board[0][j] == board[1][j] == board[2][j]  != 0:
                if board[i][2] != 0:
                    return True  
            

    # Check diagonal
    if board[0][0] == board[1][1] == board[2][2]  != 0:
        if board[i][2] != 0:
                    return True 
    
    if board[0][2] == board[1][1] == board[2][0]  != 0: 
            if board[i][2] != 0:
                    return True 
    

    








while True:

    if state == 0:
        row = int(input("Enter row: "))
        if check_legal_move(row) == False:
            state = 0
        else :
            state = 1
    
    if state == 1:
        col = int(input("Enter col: "))
        if check_legal_move(col) == False:
            state = 1
        else :
            state = 2

    if state == 2:
        player = int(input("Enter player: "))
        if check_legal_move(player) == False:
            state = 2
        else :
            state = 3

    if state == 3:
        input_move(row, col, player)
        state = 0
        turns += 1

        if check_win(board) == True:
            print("Player " + str(player) +" wins")
            break


        if turns == 9:
            print("Game stopped")
