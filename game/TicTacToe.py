# V1.05_final
from random import choice
from Siga import showBoard


# global list used to insert (1 or more user's) or the computer's input.
slots = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
# demo list to show the user how to use the board.
demo = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def help():
    '''prints game manual'''
    print('''hello! this is TicTacToe made by Adham and supervised by our team '3x3.'
the concept is pretty simple, you choose whether you want to play with the computer or with your friend and based on turns
each player will try to hit his/her letter (X or O) horizontally, vertically, or diagonally in 3 slots.
who ever claims three consecutive of his letter, Wins the game!
''')


def SingleOrMulti():
    '''multiplayer / single player checker
    returning string that is either 'single' or 'multi'''

    gametype = ''
    # loop to keep asking the user for one of the two inputs, y or n.
    while gametype == '':
        mode = input('are you alone? y for yes and n for no please.')
        if mode == 'y':
            gametype += 'single'
            print("alright! you'll play with Ultron :)")
            return gametype
        elif mode == 'n':
            print("oh, you are with a friend. this will be interesting.")
            gametype += 'multi'
            return gametype
        else:
            print('oh-oh. use y for yes and n for no. no capitalization.')


def shwBoard(board):  # function that calls the board, imported.
    '''function that calls showboard function from the siga.py file'''

    # print('' +board[3]+ '  | ' +board[4]+ '  | '+board[5] ) \/\/\/\/\/
    # print('' +board[0]+ '  | ' +board[1]+ '  | '+board[2] ) old board
    # print('' +board[6]+ '  | ' +board[7]+ '  | '+board[8] ) /\/\/\/\/\
    # print('-------------')

    showBoard(board, Labels=False)


def whosfirst():
    '''player1 chooses who goes first, returning whether P1 is playing W comp or P2 as a string'''

    answertype = ''
    while answertype == '':
        # loop to keep asking the user for one of the two inputs, y or n
        answer = input(
            'Player 1, do you wanna go first? y for yes and n for no please.')
        if answer == 'y':
            print('okay! good luck. make your first move player 1.')
            answertype += 'yes'
            return answertype
        elif answer == 'n':
            print('okay! good luck player 1, your opponent is going first.')
            answertype += 'no'
            return answertype
        else:
            print('please stick with y for yes and n for no, no capitalization.')


def emptyspace(plyr_mve):
    '''function that identifies blank spaces in the global list (slot)
    while returning boolean True/False'''
    if slots[plyr_mve] == ' ':
        return True
    else:
        return False


def compmove():
    '''Function that loops random no choices no from range 0 to 8.
        if the choice is not taken,checked by empytyspace,
        the choice is saved in the global list (slots)
        if not the loop starts again.'''

    state = bool
    while state != True:

        x = choice(list(range(8)))
        y = emptyspace(x)
        state = y

    if state == True:
        slots[x] = 'O'
        shwBoard(slots)


def player1move(symb):
    '''function that lets the player choose
    his move and stores it into (slots) list '''

    shwBoard(demo)
    while True:
        loc = input(
            "choose your move's place from 1-9 as stated in the board infront of you")
        if loc.isnumeric():  # checks if input is a number. flo
            possible = (
                float(eval(loc)) == 1.0 or float(eval(loc)) == 2.0 or float(eval(loc)) == 3.0 or
                float(eval(loc)) == 4.0 or float(eval(loc)) == 5.0 or float(eval(loc)) == 6.0 or
                float(eval(loc)) == 7.0 or float(eval(loc)) == 8.0 or float(eval(loc)) == 9.0
            )
            # checks if the input after being filtered is between 1-9 whole numbers.
            if possible == True:
                if emptyspace(eval(loc)-1) == True:
                    slots[eval(loc)-1] = symb
                    shwBoard(slots)

                    break

            else:  # repeats the loop if number exceeds 9 or lower 1
                print('please choose between 1-9 only!!')
        else:  # repeats loop if user inputs anything other than numeric values
            print('dont use complex expression.')


def boardfull():
    '''checks if the board is full and
    prints that game has ended and returns a true val.'''

    marker = 0  # initializer
    for i in slots:
        if i == ' ':
            marker += 1
            return False
    if marker == 0:
        print("oh no it's a draw.")
        return True


def checkwin(symb):
    '''checks if the designated player X or O
    has won and returns their status'''
    status = True  # initializing condition

    possible = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    # possible winning combinations.
    for item in possible:
        emp_lst = []
        for i in item:
            # adding correlating items from possible with slots
            emp_lst.append(slots[i])
        if emp_lst[0] != ' ' and emp_lst[0] == emp_lst[1] and emp_lst[1] == emp_lst[2]:
            if emp_lst[0] == symb:  # prints that the designated player won
                print('you won player using letter {}!'.format(symb))
                status = True

            return status


def Gene_checkwin():
    '''Checks if either of players has won.
    similar to checkwin(f) but generalized to be
    used as an initial starting condition'''
    status = False  # initializing condition false since no one wins at the start

    possible = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    for item in possible:
        emp_lst = []
        for i in item:
            emp_lst.append(slots[i])
        if emp_lst[0] != ' ' and emp_lst[0] == emp_lst[1] and emp_lst[1] == emp_lst[2]:

            status = True
        else:
            status = False

        return status
    else:
        status = False
        return status


def runGame():
    ''' the central code that runs the game'''
    help()  # introduces player to the rules and the team
    mode = SingleOrMulti()  # user chooses game mode
    if mode == 'multi':
        if whosfirst() == 'yes':  # if player chooses to go first
            while Gene_checkwin() == False:
                # initial condition
                player1move('X')  # P1 moves
                if checkwin('X') == True:  # if P1 "X" wins game breaks and player wins
                    break
                else:  # ends P1 turn
                    if boardfull() != True:  # checks draw
                        if checkwin('O') != True:
                            # initial condition
                            player1move('O')  # P2 moves
                            # if P2 "O" wins game breaks and player wins
                            if checkwin('O') == True:
                                break
                            else:  # end P2 turn
                                if boardfull() == True:  # checks draw
                                    break
                    else:
                        break

        else:  # if P2 is going to start first
            while Gene_checkwin() == False:
                # initial condition
                player1move('O')  # P2 moves
                if checkwin('O') == True:  # if P2 "O" wins game breaks and player wins
                    break
                else:  # end P2 turn
                    if boardfull() != True:  # checks draw
                        if checkwin('X') != True:
                            # initial condition
                            player1move('X')  # P1 moves
                            
                            if checkwin('X') == True:  # if P1 "X" wins game breaks and player wins
                                break
                            else:
                                if boardfull() == True:  # checks draw
                                    break
                    else:
                        break

    if mode == 'single':  # if player chooses single with comp
        if whosfirst() == 'yes':  # player chooses to go first
            while Gene_checkwin() == False:
                '''^^^ initial condition ^^^'''
                player1move('X')  # P1 moves
                if checkwin('X') == True:  # if P1 "X" wins game breaks and player wins
                    break
                else:  # ends P1 turn
                    if boardfull() != True:  # checks draw
                        if checkwin('O') != True:
                            # initial condition
                            compmove()  # comp moves
                            # if COMP "O" wins game breaks and player wins
                            if checkwin('O') == True:
                                break
                            else:  # end COMP turn
                                if boardfull() == True:  # checks draw
                                    break
                    else:
                        break

        else:  # COMP goes first
            while Gene_checkwin() == False:
                # initial condition
                compmove()  # COMP moves
                if checkwin('O') == True:  # if COMP "O" wins game breaks and player wins
                    break
                else:  # end COMP turn
                    if boardfull() != True:  # checks draw
                        if checkwin('X') != True:
                            # initial condition
                            player1move('X')  # P1 moves
                            # if P1 "X" wins game breaks and player wins
                            if checkwin('X') == True:
                                break
                            else:  # end P1 turn
                                if boardfull() == True:  # checks draw
                                    break
                    else:
                        break
