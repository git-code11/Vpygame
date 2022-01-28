import pygame 
from pygame.locals import *
import sys
import math
import random
BLACK  = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ANCOLOR = (125,125,125)
WHITE = (255,255,255)

pygame.init()

display_surf = pygame.display.set_mode((600,400))
pygame.display.set_caption("Hello world")

display_surf.fill(WHITE)
pygame.draw.lines(display_surf,GREEN,True,(
	(146+30,0+10),(291+30,106+10),(236+30,277+10),(56+30,277+10),(0+30,106+10)
	),2)
pygame.draw.line(display_surf,BLUE,(60,60),(360,120),5)
pygame.draw.circle(display_surf,RED,(300,50),20,1)
pygame.draw.ellipse(display_surf,RED,(200,150,100,50))
pygame.draw.arc(display_surf,BLACK,(200,150,100,50),0,math.pi*2,2)
pygame.draw.rect(display_surf,BLUE,(200,150,100,50),1)

my_car = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("../cars/car4.png"),(50,200)),270)
my_bus = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("../cars/car1.png"),(50,200)),90)
bus_rect = my_bus.get_rect()
bus_rect.topleft = (600,20)
my_rect = my_car.get_rect()
my_rect.topleft = (10,20)
speed = 10
clock = pygame.time.Clock()
def failed():
	fontobj = pygame.font.SysFont("arial",50,True,True)
	surf = fontobj.render("GameOver",True,GREEN,BLUE)
	surf_rect = surf.get_rect()
	surf_rect.topleft = ((600-surf_rect.width)/2,(400-surf_rect.height)/2)
	display_surf.blit(surf,surf_rect)
	pygame.display.update()
def _act():
	key = pygame.key.get_pressed()
	if key[K_RIGHT]:
		my_rect.left += speed
	elif key[K_LEFT] and my_rect.left > 0:
		my_rect.left -= speed
	elif key[K_UP]  and my_rect.top > 0:
		my_rect.top -= speed
	elif key[K_DOWN]:
		my_rect.top += speed
	else:
		pass
pygame.mixer.music.load("./music1.mid")
pygame.mixer.music.queue("./music2.mid")
music_cnt = 0
pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
pygame.mixer.music.play()
sound1 = pygame.mixer.Sound("./match1.wav")
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == (pygame.USEREVENT +1):
			print(music_cnt)
			if(music_cnt%2 == 0):
				pygame.mixer.music.queue("./music1.mid")
			else:
				pygame.mixer.music.queue("./music2.mid")
			#pygame.mixer.music.play()
			music_cnt += 1

	_act()
	bus_rect.move_ip((-speed,0))
	if(bus_rect.right <0):
		bus_rect.left = 600
		bus_rect.top = random.randrange(10,390)

	if(my_rect.colliderect(bus_rect)):
		#print("collision occured")
		sound1.play()
		failed()
		pygame.mixer.music.stop()
		pygame.time.delay(1024)
		pygame.mixer.music.play()
		bus_rect.left = 600
		bus_rect.top = random.randrange(10,390)
		my_rect.left = 10
	else:
		display_surf.fill(ANCOLOR)
		display_surf.blit(my_car,my_rect)
		display_surf.blit(my_bus,bus_rect)
		pygame.display.update()
	clock.tick(30)
