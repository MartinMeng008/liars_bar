import pygame
from moviepy.editor import VideoFileClip
import sys


def play_video(is_dead: bool) -> None:
    """Play a video of the player making a shoot."""
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
    pygame.event.pump()
    pygame.display.quit()
    pygame.quit()
    clip.close()
    sys.exit(0)
