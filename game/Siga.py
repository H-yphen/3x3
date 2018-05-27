__author__ = "Hazem Elmasry @ZyptosKid"


from random import choice as randomChoice



# Globals: (used multiple times across different functions)
# sets of possible y/n answers:
Y = {'Y', 'y', 'yes', 'Yes', 'YES'}
N = {'N', 'n', 'no', 'No', 'NO'}

# the mark of each player as will show on board:
P1 = '^'
P2 = comp = 'v'

# initialized board
Board = {
	1:P2 , 2:P2 , 3:P2 ,
	4:" ", 5:" ", 6:" ",
	7:P1 , 8:P1 , 9:P1 ,
}


def help():

	'''
	Prints a brief manual for the game, no parameters needed
	No parameters, returns None
	'''

	print('''
	Siga v1
	By: Hazem Elmasry

	How to play:

		Two players place three pieces on a 3x3 grid and move one piece at a time each turn.

		The goal is to get your three pieces in a row

		You're allowed to move to the square next to you or the square after it, Horizontally, Vertically, or Diagonally.
		But you're not allowed to jump over the other player's piece.\n\n\n
		
	Good luck!\n\n\n''')


def initialize():
	'''
	Called once. initializes Siga's unchanging options. no parameters.

	Returns a dictionary as follows:

		'Multiplayer': 	(bool) 	Multiplayer T/F depending on user input,
		'P1First': 		(bool) 	Player 1 goes first T/F depending on user input

	THIS FUNCTION CONTAINS INPUT PROMPTS

	'''
	
	# This loop makes sure the user input is correct and understood by the rest of the code
	# The loop won't exit until both multiplayer() and whoFirst() have returned tuples with AT LEAST one True value
	while True:
	
		while True:
			multi = yesno( inp = input('Multiplayer? [Y/N/RESET]:  ')) # def multiplayer is on line 94
			if any(multi) or multi == 'RESET':
				print('Alright, got that.\n')
				break # pass on to whoFirst call loop. multiplayer input should be correct.
			else:
				continue
		if multi == 'RESET':
			continue

		while True:
			P1First = yesno( inp = input('P1, wanna go first? [Y/N/RESET]:  '))
			if any(P1First) or multi == 'RESET':
				print('Alright, got that.\n')
				break # Both inputs are correct, loop breaks.
			else:
				continue
		if P1First == 'RESET':
			continue
		break


	return {
		'Multiplayer':multi[1],
		'P1First':P1First[1],
		}
		# The function's output is Tuple type. Index [0] is predefined to assure that input is correct, while index [1] represents user's choice


def yesno(inp):
	'''
	Decides the mode of the game based on its only parameter.
	Usually the parameter is an input function that prompts the user to answer a simple yes no question.
	
	Returns a tuple that has two items. 
		First item is True if user input was correct, False (along with the second item) otherwise.
		Second item is true if the player answers Yes, False if No
	
	'''

	global Y, N # Gets the Y and N sets from globals

	if multi in Y.union(N): # if the answer is valid

		if multi in Y:
			multi = True
		else:
			multi = False

		return True,multi

	else: # answer is neither Yes nor No

		print('this isn\'t a correct choice!')

		return False,False


def showBoard(Board,Labels=True):

	'''
	Prints the game board, returns None

	Params:
		Board (any linear indexed iterable),
		Labels = default True (bool) : either shows slot label or hides it

	examples:
	
		Board = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i' ]

		Labels = True:
			[1] | [2] | [3]
			 a  |  b  |  c
		   -----------------
			[4] | [5] | [6]
			 d  |  e  |  f
		   -----------------
			[7] | [8] | [9]
			 g  |  h  |  i

		Labels = False:
			 a  |  b  |  c
		   -----------------
			 d  |  e  |  f
		   -----------------
			 g  |  h  |  i

	This function is reusable for all linear iterables. Import it, no problems.

	'''

	if type(Board) == dict:
		PBoard = Board.values()

	else:
		PBoard = Board

	if Labels:
		print('\n [1] | [2] | [3]\n  {}  |  {}  |  {} \n-----------------\n [4] | [5] | [6]\n  {}  |  {}  |  {} \n-----------------\n [7] | [8] | [9]\n  {}  |  {}  |  {} \n'.format(*PBoard))
	
	else:
		print('\n  {}  |  {}  |  {} \n-----------------\n  {}  |  {}  |  {} \n-----------------\n  {}  |  {}  |  {} \n'.format(*PBoard))


def playermoved(Board,currentPMark,otherPMark):

	'''
	Processes the player's movement and checks its validity specifically based on the Siga rules.

	Params:
		Board (dict)
		currentPMark (str): Current turn player's mark. used for conditions and comparisons
		otherPMark (str): The other player's mark. also used as the one above
		
	returns the movement origin of the player for using it to check if all the player's pieces moved or not
	'''
	# list of possible corner movement combinations
	corners = [
		{1,9},
		{3,7}
	]

	# list of possible 2-block jump movement combinations
	jumps = [
		{1,3},
		{1,7},
		{1,9},
		{2,8},
		{3,7},
		{3,9},
		{4,6}
	]

	# list of possible out-of-range movement combinations
	ambition = [
		{1,8},
		{1,6},
		{2,9},
		{2,7},
		{3,4},
		{3,8},
		{4,9},
		{6,7}
	]

	# I used to try a mathematical approach instead off possible combinations approach but it was never consistent across all possible movements. For example: moving from square 4 to square 3 should mathematically mean a 1-block movement, but it actually is an out-of-range movement.

	# This loop is for RESET fallbacks
	while True:
		
		# This loop won't exit until move origin is a valid choice
		while True:

			try:

				moveOrigin = int(input('Type in a slot number where you have one of your pieces:  '))

				if moveOrigin not in Board:

					print('you chose something that isn\'t on the Board to begin with.')
					continue

				elif Board[moveOrigin] != currentPMark:

					print('please choose one of your pieces')
					continue

				break

			except Exception as a: # usually an error with the int() casting or a keyboard interrupt (ctrl+c)

				# To allow a ctrl+c exit
				if a == KeyboardInterrupt:
					break

				else:
					print('your input was invalid')
					continue

		# This loop won't exit until move destination is a valid choice and all game movement rules are satisfied (or user returns to the previous loop)
		while True:

			try:

				moveDest = input('Choose a slot number where you want it to go [or RETURN]:  ')
				
				if moveDest == 'RETURN':
					break # get out of this loop, continue the mother loop
					
				moveDest = int(moveDest)

				if moveDest not in Board:

					print('you chose something that isn\'t on the Board to begin with.')
					continue

				elif Board[moveDest] != " ":

					print('you can\'t move there!')
					continue

				cornerJumps = {moveOrigin,moveDest} in corners
				normalJumps = {moveOrigin,moveDest} in jumps
				ambitious = {moveOrigin,moveDest} in ambition


				if ambitious:

					print('can\'t move this far!')
					continue

				elif (normalJumps or cornerJumps) and Board[(moveDest + moveOrigin)/2] == otherPMark: # If there is a jump, and the slot in between has a player's piece on it; a forbidden move in Siga.

					print('can\'t jump over the other player\'s piece!')
					continue

				else:

					# if there was no problem with the player choices
					Board[moveDest] = currentPMark
					Board[moveOrigin] = " "
					# one successful move done
					break

			except Exception as a:
			# reason why I have one exception block of those for each loop is because I don't want an error to repeat the whole procedure, but rather continue with the current input prompt.
			
				if a == KeyboardInterrupt:
					break

				else:
					print('your input was invalid')
					continue
		
		if moveDest == 'RETURN':
			continue
		break


	del(corners,jumps,ambition) # no need to keep those around
	return moveOrigin # I use the move origin to make sure later that the player moved all the three pieces before winning, another rule of Sega. 
	# The condition is checked on both wincheck() and runGame()


def compumoved(Board,currentPMark,otherPMark,allmoved):
	
	### AI ALGORITHM ###
	# all must move first
		# make a set of all the possible move dests and origins combinations as lists and pass them through all the forbidden movements as sets, popping/deleting any match
		# make another list of all the move origins that are still False [list(dict.keys(False))?] (from runGame) [another param needed]
		# you end up with a set of all the possible movement lists [origin,dist] and another of unmoved origins
		# copy the possibilities set for a fallback into random choice in case all moved
		# loop through the movement lists set with index[0] aka origin and see if it's in unmoved origins
		# again if yes pass if no pop/delete that list
		# no choice available:
			# check for winning moves
		# one choice or more:
			# randomChoice it
		
	# check for winning moves
		# get the filtered set of lists from above
		# loop every set item (as set) on winning moves and see if the len of your intersection is 2
			# if yes difference the intersection with the win move to find the required dist
				# if [origin,dist] in possible dists, keep it, else pass
		# no choice available:
			# fallback to regular random choice
		# one choice or more:
			# randomChoice it vs filtered for 67/33 chance to win/pass

	'''
	Processes the computer's movement and checks its validity specifically based on the Siga rules.
	This function is derived from playermoved() but with automated choosing system.

	Params:
		Board (dict)
		currentPMark (str): Current turn computer's mark. used for conditions and comparisons
		otherPMark (str): The player's mark. also used as the one above
		
	returns the movement origin of the player for using it to check if all the player's pieces moved or not
	'''

	moveOrigins = [] # all the possible move origins (computer's pieces placement on Board)
	moveDests = [] # all the possible free destinations


	# get a list of all the possible piece choices (3 choices only) and all the possible destination choices (3 choices only) proior to choosing
	# to reduce the number of random choices that could go wrong ( from 9 choices on board twice to three choices twice), and for condition checking

	for square in Board:
		if Board[square] == ' ': # If the square is empty
			moveDests.append(square) # Make it a possible destination
		elif Board[square] == currentPMark: # else if the square has a piece that belongs to computer
			moveOrigins.append(square) # Make it a possible origin
		else:
			pass


	corners = [
		{1,9},
		{3,7}
	]

	jumps = [
		{1,3},
		{1,7},
		{1,9},
		{2,8},
		{3,7},
		{3,9},
		{4,6}
	]

	ambition = [
		{1,8},
		{1,6},
		{2,9},
		{2,7},
		{3,4},
		{3,8},
		{4,9},
		{6,7}
	]

	win = [
		{1,2,3},
		{4,5,6},
		{7,8,9},
		{1,4,7},
		{2,5,8},
		{3,6,9},
		{1,5,9},
		{3,5,7}
	]

	AIlist = []
	for origin in moveOrigins:
		for destination in moveDests:

			cornerJumps = {origin,destination} in corners
			normalJumps = {origin,destination} in jumps
			ambitious = {origin,destination} in ambition
			
			if ambitious:
				continue

			elif (normalJumps or cornerJumps) and Board[(origin+destination)/2] == otherPMark:
				continue

			else:
				AIlist.append([origin,destination])


	if all(allmoved.values()):

		options = AIlist


	else:

		unmovedset = set()
		for origin in allmoved:
			if allmoved[origin] == False:
				unmovedset.add(origin)

		options = []
		for option in AIlist:
			if option[0] in unmovedset:
				options.append(option)


	winoptions = []

	for winset in win:

		if len(set(moveOrigins).intersection(winset)) == 2:

			for option in options:
				if option[1] == winset.difference(set(moveOrigins)).pop() and option[0] not in winset:
					winoptions.append(option)



	movechoice = randomChoice([1,2,3])
	if movechoice%3 != 0 and winoptions:
		winmove = randomChoice(winoptions)
		[moveOrigin,moveDest] = winmove
		Board[moveOrigin] = ' '
		Board[moveDest] = currentPMark
	else:
		move = randomChoice(options)
		[moveOrigin,moveDest] = move
		Board[moveOrigin] = ' '
		Board[moveDest] = currentPMark


	return moveOrigin


def wincheck(Board,player,allmoved=False):

	'''
	Checks if a player won based on the given params and specifically for Siga's rules.

	Params:
		Board (dict)
		player (str): the checked player's mark
		allmoved = default False (bool): True means that all the player's pieces moved.

	returns True for a win, False for not
	'''

	# the possible win cases
	win = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]
	
	# this set is later compared to the win cases to see if it's part of that list
	PlayerComb = set()

	# looping on the board squares and looking for the player pieces' position to add to the set
	for square in Board:
		if Board[square] == player:
			PlayerComb.add(square)

	if allmoved: # If all the player-in-question's pieces moved, check if he won. Because you have to move all your pieces in Siga before a line of pieces is considered a win.

		if PlayerComb in win: # if P is a winning combination
			return True

	else:
		return False
		

def runGame():
	'''
	Main game runner, called on mainframe. No parameters, returns None.
	'''

	help()

	info = initialize() # info is a dict
	global Board, P1, P2, comp, Y, N

	while True:		

		if info['Multiplayer']: # if multiplayer is true

			# turn this move checker into a function
			P1moved = {7:False,8:False,9:False} # all pieces didn't move: False False False
			P2moved = {1:False,2:False,3:False}

			print()
			print('P1\'s piece is "{}"'.format(P1))
			print('P2\'s is "{}"'.format(P2))

			if info['P1First']: # if player 1 goes first is True

				while True:

					print('P1\'s Turn:')
					showBoard(Board)
					P1moved[playermoved(Board,P1,P2)] = True # playermoved returns the move origin which is used here to say that the original piece's place has been abandoned at least once, even if it's filled again.

					if wincheck(Board,P1,all(P1moved.values())): # all(P1moved.values()) means that all the pieces have at least moved once, if so the value would be True.
						showBoard(Board)
						print('P1 Won!')
						break
					
					print('P2\'s Turn:')
					showBoard(Board)
					P2moved[playermoved(Board,P2,P1)] = True

					if wincheck(Board,P2,all(P2moved.values())):
						showBoard(Board)
						print('P2 Won!')
						break
				break

			# Those are repititions of the above block of code with different conditions, function calls, and order. No new syntax..
			
			elif not info['P1First']:

				while True:

					print('P2\'s Turn:')
					showBoard(Board)
					P2moved[playermoved(Board,P2,P1)] = True

					if wincheck(Board,P2,all(P2moved.values())):
						showBoard(Board)
						print('P2 Won!')
						break
					
					print('P1\'s Turn:')
					showBoard(Board)
					P1moved[playermoved(Board,P1,P2)] = True

					if wincheck(Board,P1,all(P1moved.values())):
						showBoard(Board)
						print('P1 Won!')
						break
				break

		elif not info['Multiplayer']:

			P1moved = {7:False,8:False,9:False}
			compmoved = {1:False,2:False,3:False}

			print()
			print('Computer\'s piece is "{}"'.format(comp))

			if info['P1First']:

				while True:
					
					showBoard(Board)
					P1moved[playermoved(Board,P1,comp)] = True
					
					if wincheck(Board,P1,all(P1moved.values())):
						showBoard(Board)
						print('P1 Won!')
						break

					compmoved[compumoved(Board,comp,P1)] = True
					
					if wincheck(Board,comp,all(compmoved.values())):
						showBoard(Board)
						print('You lost to Ultron!')
						break
				break
			
			elif not info['P1First']:

				while True:

					compmoved[compumoved(Board,comp,P1)] = True
					
					if wincheck(Board,comp,all(compmoved.values())):
						showBoard(Board)
						print('You lost to Ultron!')
						break
					
					showBoard(Board)
					P1moved[playermoved(Board,P1,comp)] = True
					
					if wincheck(Board,P1,all(P1moved.values())):
						showBoard(Board)
						print('P1 Won!')
						break
				break

