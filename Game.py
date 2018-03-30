# This is the main game function
try:
	import sys
	import random
	import math
	#import getopt
	import pygame
	from GameObject import GameObject
	from GameKinnect import GameKinnect
	from pygame.locals import *
	#from Snake import Snake 
	from Block import Block
	from Food import Food
	from Barrier import Barrier
	from Border import Border
except ImportError as err:
	print("couldnt load module %s" % (err))
	sys.exit(2)
	
def randBinList(n):
	return [random.randint(0,1) for b in range(1,n+1)]

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
		
		print(GameKinnect.delta)
		if GameKinnect.delta > 0:
			vx = -Snake.speed
			vy = 0
			self.velocity = (vx,vy)
			super(Snake,self).update(screenWidth,screenHeight)
#			print(self.x)

		if GameKinnect.delta < 0:
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

class Game(GameKinnect):
	#try and draw number on block
	#try and randomize position 
	#delete from group when it is at the bottom
	def init(self):
		pygame.mixer.music.load('music/snakeMusic.mp3')
		pygame.mixer.music.play(-1)
		self.bgColor = (255, 255, 255)
		self.gameOver = True
		# Snake
		Snake.init()
		self.snakeGroup = pygame.sprite.Group()
		self.snakeList = []
		# Snake movement
		self.counter = 0 
		self.isMoveRight = True
		self.snakeLength = 4
		self.snakeSize=14
		self.timer = 0
		# Border
		Border.init()
		self.blockGroup = pygame.sprite.Group()
		# Barrier
		Barrier.init()
		self.barrierGroup = pygame.sprite.Group()
		self.collideBarrier = (0, 0)
		self.points = 0
		# Food
		Food.init()
		# Block
		Block.init()
		# Initialize the snakeGroup
		for i in range(self.snakeLength):
			snake = Snake(self.width//2,self.height//2 + self.snakeSize *i )
			self.snakeGroup.add(snake)
			self.snakeList.append(snake)
		# Initialize the foodGroup
		self.foodGroup = pygame.sprite.Group()
		# Initialize the borderGroup
		self.borderGroup = pygame.sprite.Group(Border(self.width//2,self.height+300,self.width,self.height))
		# GameOver Image
		self.GGImage = pygame.image.load('images/gameover.png').convert_alpha()
		self.GGImage = pygame.transform.scale(self.GGImage,(1920,1080))
		self.GGrect = self.GGImage.get_rect()
		
	def keyPressed(self, code, mod):
		if self.gameOver == True:
			if code == ord('r'):
				self.init()
				self.gameOver = False
	def timerFired(self, dt):
		if len(self.snakeList) == 0:
			self.gameOver = True
		if self.gameOver == False:
			# Time counter
			self.timer += 1
			# Update the group
			self.blockGroup.update(self.isKeyPressed,self.width,self.height)
			self.foodGroup.update(self.width,self.height)
			self.barrierGroup.update(self.width,self.height)
			# Create new elements on screen
			# Create blocks
			if self.timer % 100 == 0:
				#TODO: make sure doesnt go off screen, make sure it doesnt overlap with other blocks
				randList = randBinList(10)
				for i in range(len(randList)):
					if randList[i] == 1:
						randomX = i * 192
						for j in range(random.randint(0, 10)):
							self.blockGroup.add(Block(randomX, 0))

			# Create barriers				
			if self.timer % 100 == 0:
				barrierX = random.randint(0, self.width)
				self.barrierGroup.add(Barrier(barrierX, 0))
				pygame.sprite.groupcollide(self.blockGroup, self.barrierGroup,True,False,pygame.sprite.collide_circle)
			# Create fruits
			if self.timer == 200:
				# # Barrier.init()
#				for i in range(1):
				applex = random.randint(0, self.width)
				appley = random.randint(0, self.height//4)
				self.foodGroup.add(Food(applex, 0))
				self.timer = 0
#				pygame.sprite.groupcollide(self.blockGroup, self.foodGroup,False,True,pygame.sprite.collide_circle)
#				pygame.sprite.groupcollide(self.barrierGroup, self.foodGroup,False,True,pygame.sprite.collide_circle)
			#MARK: Snake Movement
			if self.counter >= len(self.snakeList):
				self.counter = 0 
				if self.isMoveRight:
					self.isMoveRight = False
				else:
					self.isMoveRight = True 
			else:
				if self.isMoveRight:
					if self.counter == 0:
						speed = 3
						self.snakeList[self.counter].moveRight(self.width,self.height,speed)
						self.counter +=1 
					else:
						speed = 3
						self.snakeList[self.counter].moveRight(self.width,self.height,speed)
						self.counter += 1 
				else:
					if self.counter == 0:
						speed = 3
						self.snakeList[self.counter].moveLeft(self.width,self.height,speed)
						self.counter +=1 
					else:
						speed = 3
						self.snakeList[self.counter].moveLeft(self.width,self.height,speed)
						self.counter += 1
			if pygame.sprite.groupcollide(self.snakeGroup, self.blockGroup,False,True,pygame.sprite.collide_circle):
				self.snakeLength -= 1
				snakeHead = self.snakeList[0]
				self.snakeList = [ ]
				self.snakeGroup = pygame.sprite.Group()
				for i in range(self.snakeLength):
					snake = Snake(snakeHead.x,snakeHead.y+self.snakeSize*i )
					self.snakeGroup.add(snake)
					self.snakeList.append(snake)
			if pygame.sprite.groupcollide(self.snakeGroup, self.foodGroup,False,True,pygame.sprite.collide_circle):
				self.snakeLength += 1
				self.points += 1
				snakeHead = self.snakeList[0]
				snakeTail = self.snakeList[-1]
				snake = Snake(snakeTail.x, snakeTail.y + self.snakeSize)
				self.snakeList.append(snake)
				self.snakeGroup.add(snake)
			
			if pygame.sprite.groupcollide(self.barrierGroup, self.snakeGroup, False, False):
				sumCollideX =  [ ]	
				for elem in pygame.sprite.groupcollide(self.barrierGroup, self.snakeGroup, False, False):
					sumCollideX.append(elem.x)
				sumSnakeX = 0
				for snakeEle in self.snakeGroup:
					sumSnakeX += snakeEle.x
					
				if sumSnakeX/float(len(self.snakeList)) > sum(sumCollideX)/float(len(sumCollideX)):
						self.collideBarrier = (1,0)
				else:
						self.collideBarrier = (0,1)
					
			self.snakeGroup.update(self.isKeyPressed,self.width,self.height,self.collideBarrier)
			self.collideBarrier = (0,0)

	# from http://thepythongamebook.com/en:pygame:step014	
	@staticmethod
	def write(msg="pygame is cool"):
		myfont = pygame.font.SysFont("None", 32)
		mytext = myfont.render(msg, True, (0,0,0))
		mytext = mytext.convert_alpha()
		return mytext

	def redrawAll(self, screen):
		screen.blit(Game.write("Points: %d"%self.points),(200,30))
		if self.gameOver == True:
			screen.blit(self.GGImage, self.GGrect)
			pygame.display.flip()
		else:
			self.snakeGroup.draw(screen)
			self.blockGroup.draw(screen)
			self.foodGroup.draw(screen)
			self.borderGroup.draw(screen)
			self.barrierGroup.draw(screen)
			
if __name__ == '__main__':
	Game(1920, 1080).run()
