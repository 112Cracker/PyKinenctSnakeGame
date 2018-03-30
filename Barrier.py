import pygame
import random
from GameObject import GameObject

class Barrier(GameObject):
    size = 100
    
    @staticmethod
    def init():
        Barrier.image = pygame.image.load('images/barrier.png').convert_alpha()
    
    def __init__(self,x,y,level=None):

        image = Barrier.image
        w,h = image.get_size()
 #       print(Food.size,max(w,h))
        factor = float(Barrier.size)/max(w,h)
        image = pygame.transform.scale(image, (int(w*factor), int(3*h*factor)))
        super(Barrier,self).__init__(x,y,image,w / 2 * factor)
        vx = 0
        vy = self.downSpeed
        self.velocity  = (vx,vy)
    def update(self,screenWidth,screenHeight):
        super(Barrier,self).update(screenWidth,screenHeight)

    