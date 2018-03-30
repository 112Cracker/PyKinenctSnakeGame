import pygame
import random
from GameObject import GameObject

class Food(GameObject):
    size = 40
    @staticmethod
    def init():
        Food.image = pygame.image.load('images/apple.png').convert_alpha()
    
    def __init__(self,x,y,level=None):

        image = Food.image
        w,h = image.get_size()
 #       print(Food.size,max(w,h))
        factor = float(Food.size)/max(w,h)
        image = pygame.transform.scale(image, (int(w*factor), int(h * factor)))
        super(Food,self).__init__(x,y,image,w / 2 * factor)
        vx = 0
        vy = self.downSpeed
        self.velocity  = (vx,vy)
        
    def update(self,screenWidth,screenHeight):
        super(Food,self).update(screenWidth,screenHeight)
