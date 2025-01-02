from Node import Node
import math
import pygame
from PIL import Image, ImageDraw


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
            
    def getDepth(self):
        if self.is_leaf:
            return 1
        else:
            depth = [self.top_left.getDepth(), self.top_right.getDepth(), self.bottom_left.getDepth(), self.bottom_right.getDepth()]
            return max(depth) + 1
        
    def pixelDepth(self, x, y, depth = 1):
        if (self.is_leaf):
            if (self.x1 <= x and x < self.x2 and self.y1 <= y and y < self.y2):
                return depth
        else:
            if (self.top_left.x1 <= x and x < self.top_left.x2 and self.top_left.y1 <= y and y < self.top_left.y2):
                return self.top_left.pixelDepth(x, y, depth + 1)
            elif (self.top_right.x1 <= x and x < self.top_right.x2 and self.top_right.y1 <= y and y < self.top_right.y2):
                return self.top_right.pixelDepth(x, y, depth + 1)
            elif (self.bottom_left.x1 <= x and x < self.bottom_left.x2 and self.bottom_left.y1 <= y and y < self.bottom_left.y2):
                return self.bottom_left.pixelDepth(x, y, depth + 1)
            elif (self.bottom_right.x1 <= x and x < self.bottom_right.x2 and self.bottom_right.y1 <= y and y < self.bottom_right.y2):
                return self.bottom_right.pixelDepth(x, y, depth + 1)
    
    #graphics
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
            # pygame.draw.rect(screen, (255,0,0), (self.x1 * scale_factor, self.y1 * scale_factor, (self.x2-self.x1) * scale_factor, (self.y2-self.y1) * scale_factor), 1)
    
    def draw_QT_rectangle(self, img, scale_factor, show_borders):
        if (self.is_leaf == False):
            self.top_left.draw_QT_rectangle(img, scale_factor, show_borders)
            self.top_right.draw_QT_rectangle(img, scale_factor, show_borders)
            self.bottom_left.draw_QT_rectangle(img, scale_factor, show_borders)
            self.bottom_right.draw_QT_rectangle(img, scale_factor, show_borders)
        else:
            if isinstance(self.Node.value, int):
                color = [self.Node.value] * 3  # Grayscale
            else:
                color = self.Node.value  # RGB
            
            ImageDraw.Draw(img).rectangle(
                (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                fill=tuple(color)
            )
            if(show_borders):
                ImageDraw.Draw(img).rectangle(
                    (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                    outline=(255, 0, 0), width=1
                )
    
    def output_image(self, filename, show_borders=False):
        scale_factor = 5

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (int((self.x2-self.x1) * scale_factor), int((self.y2-self.y1) * scale_factor)),
            "green"
        )
        
        self.draw_QT_rectangle(img, scale_factor, show_borders)
        

        img.save(filename)
        
    
    def is_overlapped(self, x1, y1, x2, y2):
    # Check if there is no overlap
        if (self.x2 <= x1 or  # Self is to the left of the other
            self.x1 >= x2 or  # Self is to the right of the other
            self.y2 <= y1 or  # Self is above the other
            self.y1 >= y2):  # Self is below the other
            return False
        return True
    
    def findCanvasRange(self, canvas, x1, y1, x2, y2):
        
        if (self.is_leaf == False):
            self.top_left.findCanvasRange(canvas, x1, y1, x2, y2)
            self.top_right.findCanvasRange(canvas, x1, y1, x2, y2)
            self.bottom_left.findCanvasRange(canvas, x1, y1, x2, y2)
            self.bottom_right.findCanvasRange(canvas, x1, y1, x2, y2)
        else:
            if self.is_overlapped(x1, y1, x2, y2):
                canvas['x1'] = min(canvas['x1'], self.x1)
                canvas['y1'] = min(canvas['y1'], self.y1)
                canvas['x2'] = max(canvas['x2'], self.x2)
                canvas['y2'] = max(canvas['y2'], self.y2)
                
    def drawSubspace(self, img, scale_factor, show_borders, x1, y1, x2, y2):
        if (self.is_leaf == False):
            self.top_left.drawSubspace(img, scale_factor, show_borders, x1, y1, x2, y2)
            self.top_right.drawSubspace(img, scale_factor, show_borders, x1, y1, x2, y2)
            self.bottom_left.drawSubspace(img, scale_factor, show_borders, x1, y1, x2, y2)
            self.bottom_right.drawSubspace(img, scale_factor, show_borders, x1, y1, x2, y2)
        elif (self.is_overlapped(x1, y1, x2, y2)):
            if isinstance(self.Node.value, int):
                
                color = [self.Node.value] * 3  # Grayscale
            else:
                color = self.Node.value  # RGB
            
            ImageDraw.Draw(img).rectangle(
                (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                fill=tuple(color)
            )
            if(show_borders):
                ImageDraw.Draw(img).rectangle(
                    (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                    outline=(255, 0, 0), width=1
                )
    
    
    def searchSubspacesWithRange(self, filename , x1, y1, x2, y2, show_borders=False):
        scale_factor = 5

        canvas = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

        self.findCanvasRange(canvas, x1, y1, x2, y2)
        
        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (int((canvas['x2']-canvas['x1']) * scale_factor), int((canvas['y2']-canvas['y1']) * scale_factor)),
            "white"
        )
        
        self.drawSubspace(img, scale_factor, show_borders, x1, y1, x2, y2)
        
        img.save(filename)

    def mask(self, original_img, filename, x1, y1, x2, y2):
        scale_factor = 5
        img_with_mask = original_img.copy()

        canvas = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self.findCanvasRange(canvas, x1, y1, x2, y2)

        mask_img = Image.new(
            "RGBA",
            (int((canvas['x2'] - canvas['x1']) * scale_factor), int((canvas['y2'] - canvas['y1']) * scale_factor)),
            "black"
        )

        self.maskSubspace(img_with_mask, mask_img, scale_factor, x1, y1, x2, y2)
        img_with_mask.save(filename)
        # img_with_mask.show()

    def maskSubspace(self, img_with_mask, mask_img, scale_factor, x1, y1, x2, y2):
        if not self.is_leaf:
            self.top_left.maskSubspace(img_with_mask, mask_img, scale_factor, x1, y1, x2, y2)
            self.top_right.maskSubspace(img_with_mask, mask_img, scale_factor, x1, y1, x2, y2)
            self.bottom_left.maskSubspace(img_with_mask, mask_img, scale_factor, x1, y1, x2, y2)
            self.bottom_right.maskSubspace(img_with_mask, mask_img, scale_factor, x1, y1, x2, y2)
        elif self.is_overlapped(x1, y1, x2, y2):
            ImageDraw.Draw(mask_img).rectangle(
                (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                fill="white"
            )
            ImageDraw.Draw(mask_img).rectangle(
                (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                outline=(255, 0, 0), width=1
            )
            ImageDraw.Draw(img_with_mask).rectangle(
                (self.x1 * scale_factor, self.y1 * scale_factor, self.x2 * scale_factor, self.y2 * scale_factor),
                fill="white"
            )

    def compress(self, target_size):

        scale_factor = int((self.x2 - self.x1) / target_size)
        compressed_image = []

        for i in range(target_size):
            row = []
            for j in range(target_size):
                start_x = int(self.x1 + j * scale_factor)
                start_y = int(self.y1 + i * scale_factor)
                end_x = int(start_x + scale_factor)
                end_y = int(start_y + scale_factor)

                total_value = [0, 0, 0] if isinstance(self.get_pixel_value(start_x, start_y), tuple) else 0
                pixel_count = 0

                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                        pixel = self.get_pixel_value(x, y)
                        if isinstance(total_value, list):
                            total_value[0] += pixel[0]
                            total_value[1] += pixel[1]
                            total_value[2] += pixel[2]
                        else:
                            total_value += pixel
                        pixel_count += 1

                if isinstance(total_value, list):
                    row.append(tuple(total // pixel_count for total in total_value))
                else:
                    row.append(total_value // pixel_count)

            compressed_image.append(row)

        compressed_img = Image.new(
            "RGB" if isinstance(self.get_pixel_value(self.x1, self.y1), tuple) else "L",
            (target_size, target_size)
        )

        for i in range(target_size):
            for j in range(target_size):
                compressed_img.putpixel((j, i), compressed_image[i][j])

        return compressed_img

    def get_pixel_value(self, x, y):

        if self.is_leaf:
            if self.x1 <= x < self.x2 and self.y1 <= y < self.y2:
                return self.Node.value
        else:
            if self.top_left.x1 <= x < self.top_left.x2 and self.top_left.y1 <= y < self.top_left.y2:
                return self.top_left.get_pixel_value(x, y)
            elif self.top_right.x1 <= x < self.top_right.x2 and self.top_right.y1 <= y < self.top_right.y2:
                return self.top_right.get_pixel_value(x, y)
            elif self.bottom_left.x1 <= x < self.bottom_left.x2 and self.bottom_left.y1 <= y < self.bottom_left.y2:
                return self.bottom_left.get_pixel_value(x, y)
            elif self.bottom_right.x1 <= x < self.bottom_right.x2 and self.bottom_right.y1 <= y < self.bottom_right.y2:
                return self.bottom_right.get_pixel_value(x, y)

