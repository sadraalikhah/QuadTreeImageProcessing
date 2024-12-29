import pygame
import math
from QuadTree import QuadTree
from UtilityFunctions import csv_to_image_array

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)



# Convert CSV to image array
csv_file = 'image3_gray.csv'
test_img = csv_to_image_array(csv_file)

length = int(math.sqrt(len(test_img)))
size = width , height = length, length
screen = pygame.display.set_mode(size)

qt = QuadTree(test_img)
print(qt.getDepth())
print(qt.pixelDepth(1,1))

#Save Image
qt.output_image('img_result.png', False)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
    
    qt.display(screen)
    
    
    pygame.display.flip()