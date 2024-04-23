from time import sleep
import os
import random as rand
from math import ceil
from menu import load_oscillate, generic_tip
from connect_4 import yesno

# player: name, lv, exp, hp, mhp, atk,stmu,stm, mstm, round
player = ['name', 1, 0, 150, 150, 10, 7, 168, 168, 1]


def savenew(userstat):
    # clear file
    fileclear = open('saved_game.txt', 'w')
    fileclear.close()
    # save progress
    fileclear = open('saved_game.txt', 'w')
    fileclear.write('Name,level,exp,cur_health,max_health,atk,stamina_usage,curr_stam,max_stam,round\n')
    for stats in userstat:
        fileclear.write(str(stats) + ' ')
    fileclear.close()


def valid(userInput, x, y):
    """Check if user input will be in range of option x and y for it to be valid, also check if input is quitting"""
    while True:
        if userInput == 'q' or userInput == 'quit':
            savenew(player)
            load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
            with open('menu.py') as menu:
                exec(menu.read())

        try:
            userInput = int(userInput)
            if x <= userInput <= y:
                return int(userInput)
            int('invalid input')
        except:
            userInput = input('Invalid input, please try again: ')


def monster_hp(lv_int=1):
    """ Determine monster's hp based on level"""
    return (lv_int + 2) * (lv_int + 3)


def exp(player_lv, monst_lv):
    """
    Check for player level vs monster level and determine exp.
    If monster's level is higher, player gain more exp.
    """
    if monst_lv - player_lv >= 0:
        print("You have gained", str(((1 + abs(monst_lv - player_lv)) * 10) // 1), 'exp.')
        return int((1 + abs(monst_lv - player_lv)) * 10)
    else:
        print("You have gained", str((1 / int(player_lv - monst_lv) * 10) // 1), "exp.")
        return int(1 / abs(player_lv - monst_lv)) * 10


def option(lis):
    """Quickly print options"""
    print()
    for options in lis:
        sleep(.5)
        print(options)


def checkFileEmpty():
    """Check if saved file is empty"""
    if os.stat("saved_game.txt").st_size == 0:
        return True
    return False


def monster_spawn(lv=1, num=1):
    """Spawn monster based on level of player and round they are currently on."""
    if not num % 10:
        num += 1
        if num != 60:

            mons_lv = lv + 3
            return [mini_boss[num // 10 - 1], mons_lv, monster_hp(3 * mons_lv), ceil(4 * mons_lv), num]
        elif num == 60:
            mons_lv = lv + 10
            return ['DEMON KING', mons_lv, monster_hp(5 * mons_lv), ceil(5 * mons_lv), num]

    else:
        num += 1
        mons_lv = rand.randrange(lv - 1, lv + 3)
        return [rand.choice(monster), mons_lv, monster_hp(mons_lv), ceil(4 / 3 * mons_lv), num]


def battle(userstat, monster_id):
    """
    Battle phase, find player and monster dmg, health, etc. and establish
    interaction based on chosen option and monster chosen action.

    If monster is boss, then extra action (eg. charge) is added

    Return false if died, else return user remaining health
    """
    charging = 0
    name = monster_id[0]
    monster_lv = monster_id[1]
    dmg = userstat[5]
    stm_cons = userstat[6]
    hp = monster_id[2]

    mons_dmg = monster_id[3]
    while hp > 0:
        # die from no hp
        if userstat[3] <= 0:
            os.system('cls')
            print("You toppled down into a pool of blood, wondering if you have done enough...")
            sleep(2)
            return 0
        # die from no stamina
        elif userstat[7] <= 0:
            os.system('cls')
            userstat[3] -= userstat[3]
            print("Exhausted, your eyes struggle to focus... maybe a little nap? Just a little...")
            sleep(2)
            return 0
        os.system('cls')
        print(f'{userstat[0]} Lv{userstat[1]}{name: >50} Lv{monster_lv}')
        print(f'HP : {str(userstat[3])}/{str(userstat[4])}{"HP": >40} : {hp}/{monster_id[2]}')
        print(f'Stamina : {str(userstat[7])}/{str(userstat[8])}')

        if 0 < charging < 4:
            print('\n', name, 'seems to be charging up...')

        elif charging == 4:
            print('\n', name, 'is about to unleash its power in the next turn...')

        option(['[1] Attack', '[2] Parry: Reflect damage to dealer'])
        choice = input('\nChoose an action above: ')
        choice = valid(choice, 1, 2)
        while True:
            try:
                int(choice)
                if int(choice) == 1:
                    choice = 'attack'
                    break
                elif int(choice) == 2:
                    choice = 'parry'
                    break
                int('invalid choice')
            except ValueError:
                choice = input('Invalid input, try again: ')

        if name not in mini_boss and name != "DEMON KING":
            action = rand.choice(monst_action)

        elif name in mini_boss:
            if charging == 0:
                action = rand.choice(mini_action)
            else:
                action = 'charge'

        else:
            if charging == 0:
                action = rand.choice(king_action)
            else:
                action = 'charge'

        if action == 'attack':
            if choice == 'attack':
                print(f'You have dealt {dmg} dmg to {name}!')
                hp -= dmg
                sleep(.5)
                print(f'\n{name} dealt {mons_dmg} dmg!')
                userstat[3] -= mons_dmg
                sleep(2)

            elif choice == 'parry':
                print('Successful parry!')
                hp -= mons_dmg
                sleep(.5)
                print(f'\n{name} have taken {mons_dmg} dmg!')
                sleep(2)

        elif action == 'evade':
            print(f'{name} had used evasion!')
            if choice == 'parry':
                sleep(.5)
                print("\nYou have wasted a parry...")
            sleep(2)

        elif action == 'charge' and charging < 5:
            if charging == 0:
                print(f'{name} have started charging...')
                sleep(.5)
            charging += 1
            if choice == 'attack':
                print(f'You have dealt {dmg} dmg to {name}!')
                hp -= dmg
                if hp > 0:
                    print(name, 'seems unphased and continued charging')

            elif choice == 'parry':
                print('\nYou have wasted a parry...')
            sleep(2)

        elif charging >= 5:
            charging = 0
            if choice == 'attack':
                print(name, 'is immune to your attack.\n')
                sleep(.5)
                userstat[3] -= 10 * mons_dmg
            print('THE WRAITH OF', name, 'HAS BEEN UNLEASHED!!!')
            sleep(2)
            if choice == 'parry':
                print(f'You have successfully parry {name}\'s strongest attack!')
                sleep(1)
                hp -= 10 * mons_dmg
        player[7] -= stm_cons

    os.system('cls')
    print("You have defeated", monster_id[0] + '!')

    return userstat[3]


monst_action = ['attack', 'attack', 'attack', 'evade']

mini_action = ['attack', 'attack', 'attack', 'charge', 'evade']

king_action = ['attack', 'evade', 'evade', 'charge', 'evade', 'attack']
direction = ['Foward', 'Left', 'Right']

monster = ['Long Limbs Humanoid', 'Large-mouth Monster',
           'Glass-eye Skeleton', 'Floating Head', 'Crimson Humanoid', 'Unwaving Hand', 'Legless Longlegs']

mini_boss = ['UNDEAD BISHOP', 'HEADLESS KNIGHT', 'NAMELESS-QUEEN', 'UNDEAD PALADIN']

encouter_surprise = ['A figure emerges from the shadow.', 'Instinctively, you turned around.',
                     'You slowly approach a figure from behind, BANG! A loud noise have expose your position.',
                     'A figure slowly approaches you.', 'You felt eyes watching you, following your movement.']
encouter_right = ['Something jumped out of the corner!', 'You felt liquid dripping from above.',
                  'Your keen sense spotted a figure in the distance.', 'A sharp sound echoed ahead.']
encouter_left = ['A plank flies from your left, almost hitting you.', 'The floor is drenched in blood.',
                 'Something smelled awful ahead.', 'A figure charged at you.']

intersection = ['You reached an intersection, dampened in blood and fluid.', 'There are 3 directions you can go.',
                'The path forward reeks of blood...That leave 2 options..',
                'The intersection full of skid mark, all lead to the left path.',
                'A figure disappeared to the right path.']

##########################################################

if __name__ == "__main__":
    os.system('cls')

    if checkFileEmpty():
        optList = ['[1] New Game', '[3] Quit']
    else:
        optList = ['[1] New Game', '[2] Continue', '[3] Quit']
    print('Dungeon Spyre')
    sleep(.5)
    print('Please select one of the following:')
    sleep(.5)
    option(optList)
    sleep(.5)
    user = input('\nWhat is your choice? (Select a number):\n')

    # Check if user chose valid option
    user = valid(user, 1, 3)

    while checkFileEmpty() and user == 2:
        print("There are no saved file...")
        os.system('cls')
        print('Dungeon Spyre')
        sleep(.5)
        print('Please select one of the following:')
        sleep(.5)
        option(optList)
        sleep(.5)
        user = input('\nWhat is your choice? (Select a number):\n')
        user = valid(user, 1, 3)

    # overwrite files and start new game
    if user == 1:
        os.system('cls')
        print('"Welcome to Dungeon Spyre!"')
        sleep(1)
        input('(Press enter to continue...)')
        os.system('cls')
        print(
            'Tilith: "My name is Tilith, and I presume you\'re here to banish the monster laying dormant in the dungeon?"')
        sleep(1)
        input('\nYou nodded lightly...(Press enter to continue...)')
        os.system('cls')
        print('Tilith: "It\'s an honor to meet you! Mighty knight, may I know your name?"')
        sleep(1)
        player[0] = input('\nMy name is: ')

        while player[0] == '' or any(not x.isalpha() for x in player[0]):
            os.system('cls')
            print('Invalid name')
            sleep(.5)
            player[0] = input('\nMy name is: ')

        savenew(player)

        os.system('cls')
        print(f'Tilith: "Well then Knight {player[0]}, I wish you luck on your journey!"')
        print('Tilith: "I will awaits your good news!"')
        input('\n(Press enter to continue...)')

    # loading saved file onto profile
    elif user == 2 and not checkFileEmpty():
        file = open('saved_game.txt')
        content = file.read()
        content = content.split('\n')
        content.pop(0)
        player = []
        profile = content[0].split()

        for element in profile:
            try:
                int(element)
                player.append(int(element))
            except ValueError:
                player.append(element)
        file.close()
    else:
        load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
        with open('menu.py') as menu:
            exec(menu.read())

    #################### Battle ########################

    while True:
        os.system('cls')
        print('Slowly, you wander deep in the dungeon, knowing that it will be the last time you see an open sky.')
        input('\n(Press enter to continue...)')
        while player[3] > 0:

            os.system('cls')
            monst = monster_spawn(player[1], player[9])
            player[9] = monst[4]
            print(rand.choice(intersection), '\nPlease chose a direction to go')
            option(['[1] Forward', '[2] Right', '[3] Left'])
            user = input('What direction would you like to go? ')
            user = valid(user, 1, 3)
            if user == 1:
                x = encouter_surprise
            elif user == 2:
                x = encouter_right
            else:
                x = encouter_left
            os.system('cls')
            print(rand.choice(x), 'You have encountered', monst[0])
            input('(Press enter to continue...)')
            player[3] = battle(player, monst)

            if player[3] > 0:

                player[2] += exp(player[1], monst[1])
                sleep(2)
                if player[2] >= 100:
                    os.system('cls')
                    player[1] += 1
                    player[2] %= 100
                    player[3] = player[4]
                    player[7] = player[8]
                    print('You have leveled up!', end=' ')
                    sleep(.2)
                    print('Your Health and Stamina have been recovered!')
                    input('(Press enter to continue...)')
                    print('You have 1 skill point, where would you like to spend them?')
                    option(['[1] Max Health increase (40 pts)', '[2] Max Stamina increase (28 pts)',
                            '[3] Damage increase (5 pts)'])

                    user = input('\nPlease choose number 1-3: ')
                    user = valid(user, 1, 3)
                    if user == 1:
                        player[4] += 40
                        player[3] = player[4]
                    elif user == 2:
                        player[8] += 28
                        player[7] = player[8]
                    else:
                        player[5] += 5
                    savenew(player)
                savenew(player)

        input('\n(Press enter to continue...)')
        os.system('cls')

        print('You have died!')
        sleep(.5)
        print(f'You have strengthen yourself to lv {player[1]}, before succumbing to the cycle of life...')
        sleep(.5)

        # clear file since lost game
        emptyfile = open('saved_game.txt', 'w')
        emptyfile.close()
        user = yesno(input('Would you like to play again? (Y/N) '))
        if not user:
            load_oscillate('returning', 'Tip: ' + rand.choice(generic_tip))
            with open('menu.py') as menu:
                exec(menu.read())
        elif user:
            with open('Dungeon.py') as newgame:
                exec(newgame.read())
