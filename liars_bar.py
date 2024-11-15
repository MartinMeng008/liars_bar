# Description: A program that simulates the Liars Bar game
# Author: Qian Meng
# Email: martinmq99@gmail.com
# Date: 2024-11-02
# Version: 1.0
# Usage: python liars_bar.py
# Dependencies: moviepy, pygame, ffmpeg

# Todo:
# 1. Add final leaderboard (done)
# 2. Add option to play video or not (done)
# 2. Handle invalid names by prompting again instead of exception

import random
import time
import pygame
from moviepy.editor import VideoFileClip
import argparse

DEBUG = False


class Player:
    """A class that represents a player in the Liars Bar game
    The player has an upper bound on the number of shoots he can make
    """

    def __init__(self, name: str, max_shoots: int = 6, do_video: bool = False) -> None:
        """Initialize the player with the maximum number of shoots
        and a number between 1 and max_shoots that represents on which shoot the player dies
        """
        self.name = name
        self.max_shoots = max_shoots
        self.do_video = do_video
        self.fatal_shoot = random.randint(1, max_shoots)
        self.shoots = 0

    def shoot(self) -> bool:
        """The player makes a shoot
        """
        self.shoots += 1
        if self.do_video:
            self.play_video(self.shoots == self.fatal_shoot)
        return self.shoots == self.fatal_shoot

    def play_video(self, is_dead: bool) -> None:
        """Play a video of the player making a shoot
        """
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Video Player')

        # Load the video using moviepy
        if is_dead:
            clip = VideoFileClip('videos/shooting_dead.mp4')
        else:
            clip = VideoFileClip('videos/shooting_alive.mp4')
        clip = clip.resize((640, 480))

        # Convert video frames to a format Pygame can use
        frames = []
        for frame in clip.iter_frames():
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frames.append(frame_surface)

        clock = pygame.time.Clock()
        frame_count = len(frames)
        frame_rate = clip.fps
        current_frame = 0

        # Main loop to play the video
        running = True
        while running and current_frame < frame_count:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(frames[current_frame], (0, 0))
            pygame.display.update()
            current_frame += 1
            clock.tick(frame_rate)

        # Clean up
        clip.close()
        pygame.quit()

    def alive(self) -> bool:
        """Check if the player is alive
        """
        return self.shoots < self.fatal_shoot

    def get_status(self) -> str:
        """Get the status of the player
        """
        return f'{self.shoots}/{self.max_shoots}'


def main(num_players: int = 3, sleep_time: int = 1, do_video: bool = True) -> None:
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
    # print('If you call a liar on a single true ghost card, everyone on the table makes a shoot')
    # ghost_mode = input('Do you want to play with ghost card? (y/n) ')
    names = []
    num_players = int(input('Enter the number of players: '))
    Leaderboard = {}
    for i in range(num_players):
        name = input(f'Enter player {i+1} name: ')
        names.append(name)
        Leaderboard[name] = 0
    table_cards = ['Q', 'K', 'A']
    play_again = 'y'
    while play_again == 'y':
        players = [Player(name=names[i], do_video=do_video)
                   for i in range(num_players)]
        num_round = 1
        while len(players) > 1:
            if DEBUG:
                sleep_time = 0
                print('==== Players ====')
                for player in players:
                    print(f'{player.name} fatal shot: {player.fatal_shoot}')
            table_card = random.choice(table_cards)
            print(f'==== Round {num_round} ====')
            num_round += 1
            time.sleep(sleep_time)
            # print()
            time.sleep(sleep_time)
            print(f'Table card: {table_card}')
            time.sleep(sleep_time)
            player_status: str = ', '.join(
                [f'{p.name} [{p.get_status()}]' for p in players])
            which_player = str(
                input(f"Who should make the shoot? ({player_status}) "))
            which_players = which_player.split(',')
            # remove any leading or trailing whitespaces
            which_players = [p.strip() for p in which_players]
            for shoot_player in which_players:
                player = None
                for p in players:
                    if p.name == shoot_player:
                        player = p
                        break
                assert player is not None, f'Player {shoot_player} is invalid'
                is_dead = player.shoot()
                time.sleep(sleep_time)
                print(f'{player.name} made a shoot')
                time.sleep(sleep_time)
                if is_dead:
                    print(f'Player {player.name} is dead')
                    players.remove(player)
                else:
                    print(f'Player {player.name} is alive')
            time.sleep(sleep_time)
        print('==== Game Over ====')
        print(f'Winner is {players[0].name}!!')
        Leaderboard[players[0].name] += 1
        time.sleep(sleep_time)
        play_again = input('Do you want to play again? (y/n) ')
    print('==== Final Leaderboard ====')
    # Sort the leaderboard by score
    Leaderboard = dict(
        sorted(Leaderboard.items(), key=lambda x: x[1], reverse=True))
    for name, score in Leaderboard.items():
        print(f'{name}: {score}')
    time.sleep(sleep_time)
    print('================================')
    winners = [name for name, score in Leaderboard.items() if score ==
               list(Leaderboard.values())[0]]
    if len(winners) == 1:
        print(f'Congrats to the winner {winners[0]}!!')
    else:
        print(f"Congrats to the winners {', '.join(winners)}!!")
    print('================================')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Liars Bar game')
    # argparser.add_argument('num_players', type=int, help='Number of players', default=3, required=False)
    argparser.add_argument("-v", "--video", help="Play video",
                           action="store_true", default=False)

    args = argparser.parse_args()
    main(do_video=args.video)
    # main()
