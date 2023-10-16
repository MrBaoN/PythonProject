import os
from sys import exit
from time import sleep
import random as rand

Get4_tip = ['You can type \'q\' or \'quit\' anytime to return to menu!',
            'This is totally not similar to Connect 4 at all!',
            'Connect multiple three\'s simultaneously for a better chance to win!',
            'Start in the middle gets you better chances of winning!']
element_tip = ['You can type \'q\' or \'quit\' anytime to return to menu!',
               'Fire beat Ice, Ice beat Water, and Water beat Fire.',
               'This game is inspired by the age-old Rock-Paper-Scissors!',
               'Don\'t ask why fire beat ice...a glimpse of this knowledge will kill you...']
dungeon_tip = ['You can type \'q\' or \'quit\' anytime to return to menu!',
               'You can parry to reflect incoming damage to your opponent!',
               'All action in battle consumes 7 stamina regardless, use them sparingly!',
               'Stamina will be recover after a level up!']
generic_tip = ['You can type \'q\' or \'quit\' anytime to return to menu!', 'Did you know that 1 + 1 = 3? Me neither...',
               'The loading screen is not actually loading anything, you got bamboozle!',
               'Dying is bad for you!']

game_list = ['[1] Get Four', '\n[2] DungeonSpyre', '\n\n[3] Quit']
game_tip = [Get4_tip, dungeon_tip, generic_tip]


################ Cool loading screen #################

def load_oscillate(string, tip_shown='', count=0, finalcount=0):
    if count > 3:
        finalcount += 1
        if finalcount != 3:
            count = 0
            load_oscillate(string, tip_shown, count, finalcount)
        else:
            return True
    else:

        sleep(.5)
        os.system('cls')
        print(string, end='')
        print('.' * count)
        print('\n' + tip_shown)
        count += 1
        load_oscillate(string, tip_shown, count, finalcount)


########################################################

if __name__ == "__main__":
    os.system('cls')

    print('Welcome to our selection of games!')
    sleep(1)
    print('We have:')

    for option in game_list:
        sleep(.5)
        print(option)

    sleep(1)
    user = input('\nWhich one do you want to play?\nPlease choose a number from 1-3: ')

    while True:
        try:
            int(user)
            if int(user) == 1:
                gamename = 'connect_4.py'
                tip = 0
                break
            elif int(user) == 2:
                gamename = 'Dungeon.py'
                tip = 1
                break
            elif int(user) == 3:
                exit()
            else:
                int('urmom')

        except:
            os.system('cls')
            print('Invalid input, try again!')
            sleep(2)
            os.system('cls')
            print('Welcome to our selection of games!')
            print('We have:')
            print('[1] Get Four\n[2] DungeonSpyre\n\n[4] Quit')

            user = input('\nWhich one do you want to play?\nPlease chose a number from 1-3: ')

    print('Great choice!')
    load_oscillate('loading', 'Tip: ' + rand.choice(game_tip[tip]))
    exec(open(gamename).read())

