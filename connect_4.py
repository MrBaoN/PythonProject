from sys import exit
from time import sleep
import os
import random as rand
from menu import load_oscillate, generic_tip

quiti = ['q', 'quiti']

####################     Prior game preparation     #########################

row_identifier = ['  A  ', '  B  ', '  C  ', '  D  ', '  E  ', '  F  ', '  G  ']
row_1 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']
row_2 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']
row_3 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']
row_4 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']
row_5 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']
row_6 = ['|___|', '|___|', '|___|', '|___|', '|___|', '|___|', '|___|']

rows = [row_identifier, row_1, row_2, row_3, row_4, row_5, row_6]
column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}

another = ['another', 'friend', 'friends', 'players', '2', 'two', 'someone', 'with']

# Player profile for easy reference
player1 = ['Player 1', 'marking', 'column', 'another']
player2 = ['Player 2', 'marking', 'column', 'another']


################    Def command    #######################

def check_q(user_input):
    """Check for quit command"""
    user_input = user_input.split()
    for word in user_input:
        if word.lower() in quiti:
            load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
            with open('menu.py') as newgame:
                exec(newgame.read())


###########################
def yesno(x):
    """
    Check each word to for keywords to see if yes or no and return true or false.
    """
    yes = ['yes', 'y', 'sure', 'yea', 'ye']
    no = ['no', 'n', 'nope', 'nah', 'not']

    while True:
        x = x.split()
        for each_word in x:

            if each_word.lower() in yes:
                return True

            elif each_word.lower() in no:
                return False

        x = input('Invalid answer, please retype: ')


############################
def valid(x):
    """Check if column inputted is even a column at all. Also check if user want to quit"""

    while True:
        try:
            int(column.get(x.lower()))
            return column.get(x.lower())
        except:
            cls()
            for eachrow in rows:
                eachrow = ''.join(eachrow)
                print(eachrow)
            x = input('Invalid column, try again: ')


##############################
def player_piece(y):
    """Determine player 2 marking after player 1 choose"""
    y = y.lower()
    if y == 'x':
        return 'O'
    elif y == 'o':
        return 'X'


###############################
def winning():
    """
    Check for the same piece 4 times consecutively in horizontal, vertical, diagonals formulation to determine if winning
    or not. If there is someone winning, check for which player's marking it was to determine who won.
    """
    height = 7
    width = 7

    # check horizontal spaces
    for eachrow in range(1, height):
        for eachcol in range(width - 3):
            if rows[eachrow][eachcol] == rows[eachrow][eachcol + 1] == rows[eachrow][eachcol + 2] == rows[eachrow][
                eachcol + 3] \
                    and rows[eachrow][eachcol] != '|___|':
                if rows[eachrow][eachcol] in player1:
                    return True, player1, eachrow, eachcol, '-', rows[eachrow][eachcol]
                elif rows[eachrow][eachcol] in player2:
                    return True, player2, eachrow, eachcol, '-', rows[eachrow][eachcol]

    # check vertical spaces
    for eachcol in range(width):
        for eachrow in range(1, height - 3):
            if rows[eachrow][eachcol] == rows[eachrow + 1][eachcol] == rows[eachrow + 2][eachcol] == rows[eachrow + 3][
                eachcol] \
                    and rows[eachrow][eachcol] != '|___|':
                if rows[eachrow][eachcol] in player1:
                    return True, player1, eachrow, eachcol, '|', rows[eachrow][eachcol]
                elif rows[eachrow][eachcol] in player2:
                    return True, player2, eachrow, eachcol, '|', rows[eachrow][eachcol]

    # check / diagonal spaces
    for eachrow in range(1, height - 3):
        for eachcol in range(3, width):
            if rows[eachrow][eachcol] == rows[eachrow + 1][eachcol - 1] == rows[eachrow + 2][eachcol - 2] == \
                    rows[eachrow + 3] \
                        [eachcol - 3] and rows[eachrow][eachcol] != '|___|':

                if rows[eachrow][eachcol] in player1:
                    return True, player1, eachrow, eachcol, '/', rows[eachrow][eachcol]
                elif rows[eachrow][eachcol] in player2:
                    return True, player2, eachrow, eachcol, '/', rows[eachrow][eachcol]

    # check \ diagonal spaces
    for eachrow in range(width - 3):
        for eachcol in range(1, height - 3):
            if rows[eachrow][eachcol] == rows[eachrow + 1][eachcol + 1] == rows[eachrow + 2][eachcol + 2] == \
                    rows[eachrow + 3][
                        eachcol + 3] and rows[eachrow][eachcol] != '|___|':

                if rows[eachrow][eachcol] in player1:
                    return True, player1, eachrow, eachcol, '\\', rows[eachrow][eachcol]
                elif rows[eachrow][eachcol] in player2:
                    return True, player2, eachrow, eachcol, '\\', rows[eachrow][eachcol]
    return False, ''


##############################
def num_player(some_input):
    """Check for keywords that indicate if user is playing against AI or another player."""

    some_input = some_input.split()

    for i in some_input:
        if i in another:
            return True
        elif i == some_input[-1] and i not in another:
            return False


##############################
def restart():
    """Reset the board to empty"""
    for eachrow in range(6, 0, -1):
        for block in range(7):
            rows[row][block] = '|___|'


##############################
def people(multiplayer):
    """
    Determine moves of bots or ask real player 2 for their move depending on if they play against
    AI or against another player
    """
    if multiplayer:
        player_2 = input(f'\nPlayer 2, you are {player2[1]}. Choose your column (A to G): ')
        check_q(player_2)
        while True:
            num = valid(player_2)
            if row_1[num] != '|___|':
                cls()
                for eachrow in rows:
                    eachrow = ''.join(eachrow)
                    print(eachrow)
                player_2 = input('\nThe column is occuppied, choose a different column Player 2: ')
            else:
                return num

    elif not multiplayer:
        sleep(1.5)
        choices = list(column.keys())
        computer = rand.choice(choices)
        num = valid(computer)
        while row_1[num] != '|___|':
            choices.remove(computer)
            computer = rand.choice(choices)
            num = valid(computer)
        return num


#####################################
def place_piece(piece, num):
    """Quick command that places player pieces to shorten command."""
    for i in range(6, 0, -1):
        if rows[i][num] == '|___|':
            rows[i][num] = '|_' + piece + '_|'
            break


####################################
def cls():
    """Clear screen"""
    os.system('cls')


def coolanima(row, element, position, save, new, quote, count=0, finalcount=0):
    """Animation that plays when winning, highlighting where 4 consecutive mark are"""
    if count == 1:
        finalcount += 1
        if finalcount != 6:
            count = 0
            coolanima(row, element, position, new, save, quote, count, finalcount)
        else:
            return True
    else:
        rows[row][element] = new
        if position == '/':
            rows[row + 1][element - 1] = new
            rows[row + 2][element - 2] = new
            rows[row + 3][element - 3] = new
        elif position == '\\':
            rows[row + 1][element + 1] = new
            rows[row + 2][element + 2] = new
            rows[row + 3][element + 3] = new
        elif position == '-':
            rows[row][element + 1] = new
            rows[row][element + 2] = new
            rows[row][element + 3] = new
        elif position == '|':
            rows[row + 1][element] = new
            rows[row + 2][element] = new
            rows[row + 3][element] = new
        cls()
        for i in rows:
            i = ''.join(i)
            print(i)
        print('\n' + quote)
        sleep(.5)
        count += 1
        coolanima(row, element, position, save, new, quote, count, finalcount)


####################      The game starts here      ##########################


if __name__ == "__main__":
    cls()
    print('Welcome to Get Four!')
    sleep(2)
    user_input = input(
        'Are you playing with another person or would you like to try our AI?\n(Press 1 for one player, 2 for two player): ')

    # Check for quit
    check_q(user_input)

    # Finding keyword that signify there are 2 players
    two_player = num_player(user_input)

    # Explaining the rule
    user_input = input('Would you like to go over the rules of Get Four? (Y/N) ')
    check_q(user_input)
    if yesno(user_input):
        sleep(1)
        print("\nHere are the rules:\n1. There are two players taking turn placing a mark, one at a time."
              "(X or O depending on the player's preference)")
        sleep(.5)
        print("2. Players can only chose what column (from A to G) they want their marking in, and once chose, the"
              "mark will be place in the lowest available space (either bottom or on top of another marking."
              "As implied, the mark do not replace other marks.)")
        sleep(.5)
        print("3. The objective of the game is to get 4 in a row with your own marking, either horizontally,"
              "vertically, or diagonally before your opponent.")
        sleep(.5)
        print('4. If the board get filled up completely and no one wins, the game is considered drawn.\n')
        user_input = False

        # Ask if finish reading with a little easter egg
        sleep_time = 5
        while not user_input:
            sleep(sleep_time)
            user_input = input("Have you read the rules? (Y/N) ")
            check_q(user_input)
            user_input = yesno(user_input)
            if sleep_time < 10:
                print('Take your time.')
                sleep_time += 5
            elif sleep_time < 20:
                print('Hurry up please!')
                sleep_time += 10
            else:
                cls()
                print('Awmygawd u taek 4ever!!!')
                sleep(3)
                exit()

    cls()
    print("Alrighty, let's move onto the main stage.\n")
    sleep(2.5)
    while True:
        # Asking and determining who use what marking
        user_input = input('Please choose your marking, player 1 (X or O): ')
        check_q(user_input)
        user_input = user_input.lower()

        # Check invalid input and quit
        while user_input != 'x' and user_input != 'o':
            user_input = input('Invalid selection, please chose X or O: ')
            check_q(user_input)
            user_input = user_input.lower()

        player1[1] = (user_input.upper())
        player1[-1] = '|_' + user_input.upper() + '_|'

        # determine player 2 piece
        player2[1] = player_piece(player1[1])
        player2[-1] = '|_' + player_piece(player1[1]) + '_|'
        sleep(.5)
        print(f'Player 2 is {player2[1]} then.')
        sleep(2)

        ############ Game Begin ############

        while not winning()[0]:
            cls()
            for row in rows:
                row = ''.join(row)
                print(row)
            # player 1
            player1[2] = input(f'\nPlayer 1, you are {player1[1]}. Choose your column (A to G): ')

            # Checking if column chosen is not full
            while True:
                check_q(player1[2])
                colum = valid(player1[2])
                if row_1[colum] != '|___|':
                    cls()
                    for row in rows:
                        row = ''.join(row)
                        print(row)
                    player1[2] = input('\nThe column is occuppied, choose a different column Player 1: ')
                else:
                    place_piece(player1[1], colum)
                    break
            cls()

            # Print board
            for row in rows:
                row = ''.join(row)
                print(row)

            # Check winning after each player move.
            if winning()[0]:
                sleep(.5)
                coolanima(winning()[2], winning()[3], winning()[4], winning()[5], '|___|', winning()[1][0] + ' won!')
                user_input = input('Play again? (Y/N): ')
                check_q(user_input)

                # if yes then ask user if they want another game. Also check if quitting
                if yesno(user_input):
                    restart()
                    user_input = input(
                        'Are you playing with another person or would you like to try our AI?\n'
                        '(Press 1 for one player, 2 for two player): '
                    )
                    check_q(user_input)
                    two_player = num_player(user_input)

                    cls()
                    break
                else:
                    cls()
                    load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
                    with open('menu.py') as newgame:
                        exec(newgame.read())

            elif not winning()[0]:
                full = 0
                for element in row_1:
                    if element != '|___|':
                        full += 1
                if full == len(row_1):
                    print('That\'s a draw!!!')
                    user_input = input('Play again? (Y/N): ')
                    check_q(user_input)

                    # if yes then restart board
                    if yesno(user_input):
                        restart()
                        user_input = input(
                            'Are you playing with another person or would you like to try our AI?\n'
                            '(Press 1 for one player, 2 for two player): ')
                        check_q(user_input)
                        two_player = num_player(user_input)
                        break
                    else:
                        cls()
                        load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
                        with open('menu.py') as newgame:
                            exec(newgame.read())

            # Player 2
            place_piece(player2[1], people(two_player))
            cls()

            # Print board
            for i in rows:
                i = ''.join(i)
                print(i)

            # Check winning after each player move
            if winning()[0]:
                sleep(.5)
                coolanima(winning()[2], winning()[3], winning()[4], winning()[5], '|___|', winning()[1][0] + ' won!')
                user_input = input('Play again? (Y/N): ')
                check_q(user_input)

                # if yes then ask player if they want another game, also check for quitting
                if yesno(user_input):
                    restart()
                    user_input = input(
                        'Are you playing with another person or would you like to try our AI?\n'
                        '(Press 1 for one player, 2 for two player): ')
                    check_q(user_input)
                    two_player = num_player(user_input)
                    cls()
                    break
                else:
                    cls()
                    load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
                    with open('menu.py') as newgame:
                        exec(newgame.read())

            elif not winning()[0]:
                full = 0
                for element in row_1:
                    if element != '|___|':
                        full += 1
                if full == len(row_1):
                    sleep(.2)
                    print('\nThat\'s a draw!!!')
                    sleep(.5)
                    user_input = input('Play again? (Y/N): ')
                    check_q(user_input)

                    # if yes then restart board
                    if yesno(user_input):
                        restart()
                        user_input = input(
                            'Are you playing with another person or would you like to try our AI?\n'
                            '(Press 1 for one player, 2 for two player): ')
                        check_q(user_input)
                        two_player = num_player(user_input)
                        break
                    else:
                        cls()
                        load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
                        with open('menu.py') as newgame:
                            exec(newgame.read())
