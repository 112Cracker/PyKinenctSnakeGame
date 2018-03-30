import pygame
import random
from GameObject import GameObject

class Border(GameObject):
    
    height = 5
    @staticmethod
    def init():
        Border.image = pygame.image.load('images/Transparant.png').convert_alpha()
    
    def __init__(self,x,y,screenWidth,screenHeight):

        image = Border.image
        w,h = image.get_size()
        factor = screenWidth/float(w)
        print(w*factor,Border.height,factor)
        image = pygame.transform.scale(image, (int(w*factor), Border.height))
        super(Border,self).__init__(x,y,image,w / 2 * factor)
        
    def update(self,screenWidth,screenHeight):
        super(Border,self).update(screenWidth,screenHeight)
