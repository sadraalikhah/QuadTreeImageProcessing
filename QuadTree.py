from Node import Node
import math
import pygame

def subdivide(img):
    length = int(math.sqrt(len(img)))
    span = ((0, length//2), (length//2, length))
    return [
        [img[length*i+j] for i in range(*rowRange) for j in range(*colRange)]
        for rowRange in span
        for colRange in span
    ]

class QuadTree:
    def __init__(self, img, level = 0, x1 = 0, y1 = 0):
        self.level = level
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+math.sqrt(len(img))
        self.y2 = y1+math.sqrt(len(img))
        self.is_leaf = False
        divide = False
        for pixel in img:
            if pixel != img[0]:
                divide = True
        if divide == True:
            image_quads = subdivide(img)
            mid_x = (self.x1 + self.x2) // 2
            mid_y = (self.y1 + self.y2) // 2
            self.top_left = QuadTree(image_quads[0], level + 1, self.x1, self.y1)
            self.top_right = QuadTree(image_quads[1], level + 1, mid_x, self.y1)
            self.bottom_left = QuadTree(image_quads[2], level + 1, self.x1, mid_y)
            self.bottom_right = QuadTree(image_quads[3], level + 1, mid_x, mid_y)
        else:
            self.Node = Node(img[0])
            self.is_leaf = True
            
    def display(self, screen):
        if (self.is_leaf == False):
            self.top_left.display(screen)
            self.top_right.display(screen)
            self.bottom_left.display(screen)
            self.bottom_right.display(screen)
        else:
            scale_factor = 1
            if isinstance(self.Node.value, int):
                color = [self.Node.value] * 3  # Grayscale
            else:
                color = self.Node.value  # RGB
            pygame.draw.rect(screen, color, (self.x1 * scale_factor, self.y1 * scale_factor, (self.x2-self.x1) * scale_factor, (self.y2-self.y1) * scale_factor))