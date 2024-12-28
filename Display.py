import pygame
from QuadTree import QuadTree

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)



test_img = [
    0, 0, 0, 0,
    255, 255, 255, 255,
    0, 255, 0, 255,
    255, 0, 0, 255
]

size = width, height = 400, 400
screen = pygame.display.set_mode(size)

qt = QuadTree(test_img)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
    
    qt.display(screen)
    
    pygame.display.flip()