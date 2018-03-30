import pygame
import math
from GameObject import GameObject
from GameKinnect import GameKinnect

class Snake(GameObject):

	length = 4
	speed = 10

	@staticmethod
	def init():
		Snake.image = pygame.image.load("images/circle.png").convert_alpha()

	def __init__(self,x,y):

		factor = 0.02
		image = Snake.image
		w,h = image.get_size()
#		print(w,h)
		image = pygame.transform.scale(image, (int(factor * w), int(factor * h)))
		super(Snake, self).__init__(x,y,image,30)
		self.test = GameKinnect(800, 500)
		

	def update(self, keysDown, screenWidth, screenHeight,collideBarrier):
		
		print(GameKinnect.cur_right_hand_x)
		if GameKinnect.cur_right_hand_x < 0:
			vx = -Snake.speed
			vy = 0
			self.velocity = (vx,vy)
			super(Snake,self).update(screenWidth,screenHeight)
#			print(self.x)

		if GameKinnect.cur_right_hand_x > 0:
			vx = Snake.speed
			vy = 0 
			self.velocity = (vx ,vy)
			super(Snake,self).update(screenWidth,screenHeight)
#			print(self.x)

	def moveLeft(self,screenWidth,screenHeight,speed):
		self.velocity = (-speed,0)
		super(Snake,self).update(screenWidth,screenHeight)


	def moveRight(self,screenWidth,screenHeight,speed):
		self.velocity = (speed,0)
		super(Snake,self).update(screenWidth,screenHeight)




	
