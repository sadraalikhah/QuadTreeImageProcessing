import pygame
from QuadTree import QuadTree

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)


test_img = [
    0, 0, 0, 0,
    255, 255, 255, 255,
    0, 255, 0, 255,
    255, 0, 0, 255
]

qt = QuadTree(test_img)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
    
    qt.display(screen)
    
    pygame.display.flip()