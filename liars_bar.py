# Description: A program that simulates the Liars Bar game

import argparse
import random
import time

class Player:
    """A class that represents a player in the Liars Bar game
    The player has an upper bound on the number of shoots he can make
    """ 
    def __init__(self, name: str, max_shoots: int = 6) -> None:
        """Initialize the player with the maximum number of shoots
        and a number between 1 and max_shoots that represents on which shoot the player dies
        """ 
        self.name = name
        self.max_shoots = max_shoots
        self.fatal_shoot = random.randint(1, max_shoots)
        self.shoots = 0

    def shoot(self) -> bool:
        """The player makes a shoot
        """
        self.shoots += 1
        return self.shoots == self.fatal_shoot
    
    def alive(self) -> bool:
        """Check if the player is alive
        """
        return self.shoots < self.fatal_shoot
    
    def get_status(self) -> str:
        """Get the status of the player
        """
        return f'{self.shoots}/{self.max_shoots}'

def main(num_players: int = 3, sleep_time=1) -> None:
    """The main function that simulates the Liars Bar game
    Steps:
        1. Initialize the game with the number of players
        2. Start the game until the number of players is 1
        3. For each iteration:
            a. Decides a table card among queens, kings, and aces
            sleep for a second
            b. Take as input which player is making the shoot
            c. The player makes a shoot
            d. Check if the player is alive
            e. If the player is dead, remove the player from the game
            f. If the player is alive, continue to next iteration
    """
    print('Welcome to Liars Bar game')
    time.sleep(sleep_time)
    print('The deck consists of 6 queens, 6 kings, 6 aces, and 2 jokers (wild cards)')
    time.sleep(sleep_time)
    names = []
    num_players = int(input('Enter the number of players: '))
    for i in range(num_players):
        name = input(f'Enter player {i+1} name: ')
        names.append(name)
    table_cards = ['Q', 'K', 'A']
    play_again = 'y'
    while play_again == 'y':
        players = [Player(names[i]) for i in range(num_players)]
        num_round = 1
        while len(players) > 1:
            table_card = random.choice(table_cards)
            print(f'==== Round {num_round} ====')
            num_round += 1
            time.sleep(sleep_time)
            # print()
            time.sleep(sleep_time)
            print(f'Table card: {table_card}')
            time.sleep(sleep_time)
            player_status: str = ', '.join([f'{p.name} [{p.get_status()}]' for p in players])
            which_player = str(input(f"Who should make the shoot? ({player_status}) "))
            player = None
            for p in players:
                if p.name == which_player:
                    player = p
                    break
            assert player is not None, 'Player not found'
            is_dead = player.shoot()
            time.sleep(sleep_time)
            print(f'{player.name} made a shoot')
            time.sleep(sleep_time)
            if is_dead:
                print(f'Player {which_player} is dead')
                players.remove(player)
            else:
                print(f'Player {which_player} is alive')
            time.sleep(sleep_time)
        print('==== Game Over ====')
        print(f'Winner is {players[0].name}!!')
        time.sleep(sleep_time)
        play_again = input('Do you want to play again? (y/n) ')



if __name__ == '__main__':
    # argparser = argparse.ArgumentParser(description='Liars Bar game')
    # argparser.add_argument('num_players', type=int, help='Number of players', default=3, required=False)

    # args = argparser.parse_args()
    # main(args.num_players)
    main()