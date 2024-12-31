import pygame
import math
from QuadTree import QuadTree
from UtilityFunctions import csv_to_image_array
from PIL import Image

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

#tree construction
qt = QuadTree(test_img)

#method test
print(qt.getDepth())
print(qt.pixelDepth(1,1))

qt.searchSubspacesWithRange('img_subspace.png', 10,10, 200, 300, True)

#Save Image
qt.output_image('img_result.png', False)

original_img = Image.open("img_result.png")
qt.mask(original_img,'img_mask.png', 10,10, 200, 300)

compressed_img = qt.compress(target_size=128)
compressed_img.save("compressed_image.png")





#set running to false if you don't want live view
running = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
    
    qt.display(screen)
    
    
    pygame.display.flip()