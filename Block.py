import pygame
import math
import random 
from GameObject import GameObject


class Block(GameObject):

	@staticmethod
	def init():
		Block.image = pygame.image.load("images/gold-block.png").convert_alpha()

	def __init__(self,x,y):
		factor = 0.8
		image = Block.image
		w,h = image.get_size()
		#print(w * factor)
		image = pygame.transform.scale(image, (int(factor * w), int(factor * h)))
		super(Block, self).__init__(x,y,image,30)
		self.number = random.randint(0,20)
		self.font = pygame.font.SysFont('Arial', 25)
		pygame.display.set_caption('Box Test')
		self.font.render('Hello!', True, (255,0,0)), (200, 100)
		pygame.display.update()
#		print(self.number)

	def update(self, keysDown, screenWidth, screenHeight):
		vx = 0
		vy = self.downSpeed
		self.velocity = (vx,vy)
		super(Block,self).update(screenWidth,screenHeight)







	
