from hashlib import new
from ipaddress import collapse_addresses
import gym
import random
import requests
import numpy as np
import argparse
import sys
from gym_connect_four import ConnectFourEnv
import copy

env: ConnectFourEnv = gym.make("ConnectFour-v0")
#GameOver = False
isGameOver = False
#SERVER_ADRESS = "http://localhost:8000/"
SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
# TODO: fill this list with your stil-id's
STIL_ID = ["da20example-s1", "da22test-s2"]


# --------------variables---------------------
# array([0, 1, 2, 3, 4, 5, 6]) all possible positions to put markers
notFull = np.arange(7)
# default state
#state = np.zeros((6, 7), dtype=int)

# --------------------------------------------


def call_server(move):
    res = requests.post(SERVER_ADRESS + "move",
                        data={
                            "stil_id": STIL_ID,
                            "move": move,  # -1 signals the system to start a new game. any running game is counted as a loss
                            "api_key": API_KEY,
                        })
    # For safety some respose checking is done here
    if res.status_code != 200:
        print("Server gave a bad response, error code={}".format(res.status_code))
        exit()
    if not res.json()['status']:
        print("Server returned a bad status. Return message: ")
        print(res.json()['msg'])
        exit()
    return res


def check_stats():
    res = requests.post(SERVER_ADRESS + "stats",
                        data={
                            "stil_id": STIL_ID,
                            "api_key": API_KEY,
                        })

    stats = res.json()
    return stats


"""
You can make your code work against this simple random agent
before playing against the server.
It returns a move 0-6 or -1 if it could not make a move.
To check your code for better performance, change this code to
use your own algorithm for selecting actions too
"""


def opponents_move(env):
    env.change_player()  # change to oppoent
    avmoves = env.available_moves()
    if not avmoves:
        env.change_player()  # change back to student before returning
        return -1

    # TODO: Optional? change this to select actions with your policy too
    # that way you get way more interesting games, and you can see if starting
    # is enough to guarrantee a win
    action = random.choice(list(avmoves))

    state, reward, done, _ = env.step(action)
    if done:
        if reward == 1:  # reward is always in current players view
            reward = -1
    env.change_player()  # change back to student before returning
    return state, reward, done


def student_move(currentState):

    col, score = MiniMax(currentState, 4, True, -np.Inf, np.Inf)

    print("MINMAX HAR VALT COLUMN  " + str(col) + "  med score  " + str(score))
    #state = layMarker(currentState, nextOpenRow(currentState, col), col, 1)
    # call_server(col)
    """
    TODO: Implement your min-max alpha-beta pruning algorithm here.
    Give it whatever input arguments you think are necessary
    (and change where it is called).
    The function should return a move from 0-6
    """
    # return random.choice([0, 1, 2, 3, 4, 5, 6])
    return col


# def nextOpenRow(matrix, col):
#     Colum = matrix[:, col]
#     print(Colum)
#     for r in range(6, -1):
#         if Colum[r] == 0:
#             return r
#     return -1


def nextOpenRow(matrix, col):
   # print("nexOpenRow har blivit callad")
    Colum = matrix[:, col]
  #  print(Colum)
    for r in range(0, 6):
        if Colum[5-r] == 0:
            return 5-r
    return -1


def OpenCols(matrix):
    topRow = matrix[0, :]
    openCols = []
    for c in range(0, 7):
        if topRow[c] == 0:
            openCols.append(c)
    return openCols


def layMarker(Matrix, row, col, player):
    # print("the col in laymarker is " + str(col))
    # print("  the row  in laymarker is " + str(row))
    # print("columnen")
    # print(col)
    # print("columnen")
   # column = int(str(col))
    #rows = int(str(row))

    NewMatrix = copy.deepcopy(Matrix)
    NewMatrix[row][col] = player
    return NewMatrix


def is_win_state1(Matrix):
    # Test rows
    for i in range(6):
        for j in range(7 - 3):
            value = sum(Matrix[i][j:j + 4])
            #value = Matrix[i][j]
            if abs(value) == 4:
                #        print("du har 4 horisontellt!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return True

    # Test columns on transpose array
    reversed_board = [list(i) for i in zip(*Matrix)]
    for i in range(7):
        for j in range(6 - 3):
            value = sum(reversed_board[i][j:j + 4])
            if abs(value) == 4:
                return True

    # Test diagonal
    for i in range(6 - 3):
        for j in range(7 - 3):
            value = 0
            for k in range(4):
                value += Matrix[i + k][j + k]
                if abs(value) == 4:
                    return True

    reversed_board = np.fliplr(Matrix)
    # Test reverse diagonal
    for i in range(6 - 3):
        for j in range(7 - 3):
            value = 0
            for k in range(4):
                value += reversed_board[i + k][j + k]
                if abs(value) == 4:
                    return True

    return False


def MiniMax(Matrix, depth, maximizer, alpha, beta):
   # isGameOver = is_win_state1(Matrix)
    #isGameOver = IsGameOver(Matrix)
    column = -1
    if depth == 0:
        #print("NU HAR VI NÅTT HIT 1")
     #   if isGameOver:
        #print("Game over!!!!!!!!!!")
        #        return 1, 100
      #  else:
        # print("NU HAR VI NÅTT HIT 3")
        # return score(None, Matrix)
        return None, score(Matrix)

    openCols = OpenCols(Matrix)
    if maximizer:
        maxScore = -np.Inf
        for col in openCols:

            row = nextOpenRow(Matrix, col)
            # print("the col is " + str(col))
            # print("  the row is " + str(row))
            newMatrix = layMarker(Matrix, row, col, 1)
            # print("djup = " + str(depth))
            # print("matris = " + str(newMatrix))
            # print("aplha är = " + str(alpha))
            # print("beta är = " + str(beta))
            newScore = MiniMax(newMatrix, depth-1, False, alpha, beta)[1]
            # if(newScore > 0):
            #     print("points i max är = " + str(newScore))
            # print("new score är " + str(newScore))
            # print("för matris:__________________ ")
            # print(newMatrix)
            # print("________________________")
            #maxScore = max(maxScore, newScore)
            if newScore > maxScore:
                maxScore = newScore
                column = col
                # print("favorable column på djup " +
                #       str(depth) + " är column " + str(column) + "där scoren är " +
                #       str(newScore))

            alpha = max(alpha, newScore)
            if beta <= alpha:
                break
        return column, maxScore

    else:
        minScore = np.Inf
        for col in openCols:
            row = nextOpenRow(Matrix, col)
            newMatrix = layMarker(Matrix, row, col, -1)
            # print("djup = " + str(depth))
            # print("matris = " + str(newMatrix))
            # print("aplha är = " + str(alpha))
            # print("beta är = " + str(beta))

            newScore = MiniMax(newMatrix, depth-1, True, alpha, beta)[1]
            # if(newScore < 0):
            #     print("points i min är = " + str(newScore))
            #minScore = min(minScore, newScore)
            if newScore < minScore:
                minScore = newScore
                column = col
            beta = min(beta, newScore)
            if beta <= alpha:
                break
        return column, minScore


def scoreOfSublist(list):  # player är 1 om det är jag eller 2 om de motståndare
    points = 0

    # if list.count(player) == 4:
    if sum(list[0:4]) == 4:
        points += 100
    # elif list.count(player) == 3 and list.count(0) == 1:
    if sum(list[0:4]) == 2:
        points += 4
    if sum(list[0:4]) == -2:
        points -= 4
    if sum(list[0:4]) == 3:
        points += 6
    if sum(list[0:4]) == -3:
        points += -6
    if sum(list[0:4]) == -4:
        points += -100
    # elif list.count(player) == 2 and list.count(0) == 2:
    #    points += 3
    # if(player == 1):
    #     otherPlayer = -1
    # else:
    #     otherPlayer = 1
    # # if list.count(otherPlayer) == 3 and list.count(0) == 1:
    #     points -= 6
    # # if list.count(otherPlayer) == 4:
    #     points -= 100
   # if(points != 0):
    #    print("points är = " + str(points))

    return points


def score(currentM):
    total = 0
    # horisontellt
    for row in range(6):  # 0 to 5
        #list= currentM[row,:]
        RowList = [int(i) for i in list(currentM[row, :])]
        for col in range(7-3):  # 0 to 6-3 = 3
            sublist = RowList[col:col+4]
            total += scoreOfSublist(sublist)

    # vertikalt
    for col in range(7):  # 0 to 5
        #list= currentM[row,:]
        ColList = [int(i) for i in list(currentM[:, col])]
        for row in range(6-3):
            sublist = ColList[row:row+4]
            total += scoreOfSublist(sublist)

  #  ColList = [int(i) for i in list(currentM[i+3:, i])]
    # diagonal ned
    # for col in range(7): #0 to 5
    #     #list= currentM[row,:]
    #     ColList = [int(i) for i in list(currentM[:,col])]
    #     for row in range(6-3):
    #         sublist = ColList[row:row+3]
    #         total += scoreOfSublist(player,sublist)
 # if(total != 0):
  ##      print("points i score är = " + str(total))

    return total


def play_game(vs_server=False):
    """
    The reward for a game is as follows. You get a
    botaction = random.choice(list(avmoves)) reward from the
    server after each move, but it is 0 while the game is running
    loss = -1
    win = +1
    draw = +0.5
    error = -10 (you get this if you try to play in a full column)
    Currently the player always makes the first move
    """
    state = np.zeros((6, 7), dtype=int)
    # setup new game
    if vs_server:
        # Start a new game
        # -1 signals the system to start a new game. any running game is counted as a loss
        res = call_server(-1)

        # This should tell you if you or the bot starts
        print(res.json()['msg'])
        botmove = res.json()['botmove']
        state = np.array(res.json()['state'])
    else:
        # reset game to starting state
        env.reset(board=None)
        # determine first player
        student_gets_move = random.choice([True, False])
        if student_gets_move:
            print('You start!')
            print()
        else:
            print('Bot starts!')
            print()

    # Print current gamestate
    print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
    print(state)
    print()

    done = False
    while not done:
        if(isGameOver == False):
            # Select your move

            stmove = student_move(state)  # TODO: change input here

            # make both student and bot/server moves
            if vs_server:
                # Send your move to server and get response
                res = call_server(stmove)
                print(res.json()['msg'])

                # Extract response values
                result = res.json()['result']
                botmove = res.json()['botmove']
                state = np.array(res.json()['state'])
            else:
                if student_gets_move:
                    # Execute your move
                    avmoves = env.available_moves()

                    if stmove not in avmoves:
                        print(
                            "You tied to make an illegal move! You have lost the game.")
                        print("Your move was " + str(stmove))
                        break
                    state, result, done, _ = env.step(stmove)
                    if(done):
                        print("nu är den DONE_______________")

                student_gets_move = True  # student only skips move first turn if bot starts

                # print or render state here if you like

                # select and make a move for the opponent, returned reward from students view
                if not done:
                    state, result, done = opponents_move(env)

            # Check if the game is over
            if result != 0:
                done = True
                if not vs_server:
                    print("Game over. ", end="")
                if result == 1:
                    print("You won!")
                elif result == 0.5:
                    print("It's a draw!")
                elif result == -1:
                    print("You lost!")
                elif result == -10:
                    print("You made an illegal move and have lost!")
                else:
                    print("Unexpected result result={}".format(result))
                if not vs_server:
                    print(
                        "Final state (1 are student discs, -1 are servers, 0 is empty): ")
            else:
                print(
                    "Current state (1 are student discs, -1 are servers, 0 is empty): ")

            # Print current gamestate
            print(state)
            print()


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--local", help="Play locally",
                       action="store_true")
    group.add_argument(
        "-o", "--online", help="Play online vs server", action="store_true")
    parser.add_argument(
        "-s", "--stats", help="Show your current online stats", action="store_true")
    args = parser.parse_args()

    # Print usage info if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
       # sys.exit(1)

    if args.local:
        play_game(vs_server=False)
    elif args.online:
        play_game(vs_server=True)

    if args.stats:
        stats = check_stats()
        print(stats)

    # TODO: Run program with "--online" when you are ready to play against the server
    # the results of your games there will be logged
    # you can check your stats bu running the program with "--stats"


if __name__ == "__main__":
    main()
