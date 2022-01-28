import pygame
from pygame.locals import *
red = (255,0,0)
blue = (0,0,255)
pygame.init()
display_surf = pygame.display.set_mode((400,400))
surf_1 = pygame.transform.scale(pygame.image.load("../cars/car2.png"),(80,80))#pygame.Surface((80,80))
surf_1_1 = pygame.Surface((80,80))
surf_1_1.fill(red)
rect_1 = (0,0)
mask_1 = pygame.mask.from_surface(surf_1_1)
surf_2 = pygame.transform.scale(pygame.image.load("../cars/car3.png"),(40,40))#pygame.Surface((40,40))
surf_2_2 = pygame.Surface((40,40))
surf_2_2.fill(blue)
rect_2 = (10,10)#surf_2.get_rect()
mask_2 = pygame.mask.from_surface(surf_2_2)
def collide(obj1,obj2,rect1,rect2):
	dx = rect1[0] - rect2[0]
	dy = rect1[1] - rect2[1]
	print(obj1.overlap(obj2,(dx,dy)))
display_surf.blit(surf_1_1,rect_1)
display_surf.blit(surf_2_2,rect_2)
pygame.display.update()
collide(mask_1,mask_2,rect_1,rect_2)
while True:
	for event in pygame.event.get():
		if(event.type == QUIT):
			pygame.quit()
			quit()
