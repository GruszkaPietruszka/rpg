print('''

    ____            __
   / __ \____ _____/ /___  ____ ___
  / /_/ / __ `/ __  / __ \/ __ `__ \/
 / _, _/ /_/ / /_/ / /_/ / / / / / /
/_/ |_|\__,_/\__,_/\____/_/ /_/ /_/


''')
start = ''
while start not in [1, 2, 3, 'Q']:
    start = input('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X  Type the letter and press ENTER  X
X  to continue:                     X
X                                   X
X  1 - start the game               X
X  2 - view the Hall of Fame        X
X  3 - view info about the game     X
X  Q - quit the game                X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    ''').lower()
    if start == '1':
        print('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X  Poor you! Some local people have X
X  found you nearly dead in Radom.  X
X  They've heard you took some      X
X  strange pills from a black guy   X
X  named Morpheus. Now you have to  X
X  find out what's going on and     X
X  somehow get out of this hell...  X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
        player_name = input('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X    Hey, you! What's your name?    X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
        player_class = ''
        while player_class not in ['1', '2', '3']:
            player_class = input('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X  Ok, cool. You will have to fight X
X  here a lot... What style do you  X
X  prefer?                          X
X                                   X
X  1 - Melee                        X
X  2 - Ranged                       X
X  3 - Magic                        X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
        if player_class == '1':
            player_class = 'Melee'
            capacity = 100
            strength = 10
            dexterity = 5
            energy = 5
            mana = 25
        elif player_class == '2':
            player_class = 'Ranged'
            capacity = 70
            strength = 5
            dexterity = 10
            energy = 5
            mana = 25
        elif player_class == '3':
            player_class = 'Magic'
            capacity = 50
            strength = 5
            dexterity = 5
            energy = 15
            mana = 50
        experience = 0
        player_level = 1
        print('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X  Perfect. Now you can go and see  X
X  what it's like to live in Radom. X
X  Here's how to play:              X
X                                   X
X  W, S, A, D - movement            X
X  I - inventory                    X
X  ...                              X
X                                   X
X          PRESS W to PLAY!         X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
        break
    elif start == '2':
        pass
    elif start == '3':
        print('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X This amazing rouge-like game with X
X ra(n)dom-generated levels is done X
X by Jakub "Sterydziarz" Krutak and X
X   Szymon Wójcik as a project for  X
X             our school.           X
X                                   X
X        Thanks for playing!        X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
    elif start == 'q':
        print('''
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X                                   X
X           Goodbye then!           X
X                                   X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        ''')
        exit()
