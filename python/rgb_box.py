import pygame

pygame.init()

# set the size of the window
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# set the background color for the window
color = (0, 0, 0)
screen.fill(color)

# create a box at the coordinates 100, 100 with the size 10, 10
# and the color (255, 255, 255)
color = (255, 255, 255)
r = pygame.Rect((100, 100), (10, 10))
pygame.draw.rect(screen, color, r)

# tell Python to draw the screen
pygame.display.flip()

# wait for the user to exit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit()


# color examples:
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
white = (255, 255, 255)