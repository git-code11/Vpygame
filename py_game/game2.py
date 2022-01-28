import pygame 
from pygame.locals import *
import sys
import math
import random
import glob
import os
#my colors
BLACK  = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ANCOLOR = (125,125,125)
WHITE = (255,255,255)
FPS = 30
WIDTH,HEIGHT = (500,600) 
pygame.init()
display_surf = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("my_first_game")
clock = pygame.time.Clock()

def collide_mask(obj1,obj2):
	dx = obj1.rect.left - obj2.rect.left
	dy = obj1.rect.top - obj2.rect.top
	#print("ass")
	return obj1.mask.overlap(obj2.mask,(dx,dy)) != None

def get_cars():
	bigger_car = ["car1","car2","car12"]
	big_car = ["car10","car11"]
	CARS = []
	player=0
	#print(glob.glob("../cars/car*.png"))
	for file_name in glob.glob("../cars/car*.png"):
		fname = os.path.basename(file_name).split('.')[0]
		if(fname =="car7"):
			player = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(file_name),360),(60,140))
			continue
		if(fname in bigger_car):
			CARS.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(file_name),180),(70,220)))
		elif(fname in big_car):
			CARS.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(file_name),180),(65,180)))
		else:
			CARS.append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(file_name),180),(60,150)))
	return (CARS,player)

ALL_CARS,player_car = get_cars()
CARS_LEN = len(ALL_CARS)

class background:
	def __init__(self):
		self.board = pygame.Surface((WIDTH,HEIGHT))
		self.rect = self.board.get_rect()
		self.rect.topleft = (0,0)
		self.screen = []

	def add(self,_screen):
		self.screen.append(_screen)

	def _img_screen(self,img):
		self.add(pygame.transform.scale(pygame.image.load(img),self.rect.size))

	def put_screen(self,_no=0,_surf=0):
		if(not _surf):
			_surf = self.board
		_surf.blit(self.screen[_no],(0,0))

	def draw(self,surf):
		surf.blit(self.board,self.rect)

class road(background):
	def __init__(self):
		super().__init__()

	def custom(self,_screen_no,_color=[WHITE,BLACK]):
		_screen = self.screen[_screen_no]
		mnt = 0
		for i in range(0,HEIGHT,int(HEIGHT/10)):
			for j in range(0,3):
				if(mnt%2==0):
					pygame.draw.rect(_screen,_color[0],(int((j*WIDTH/4)+WIDTH/4-15),i,15,50))
				else:
					pygame.draw.rect(_screen,_color[1],(int((j*WIDTH/4)+WIDTH/4-15),i,15,50))
				mnt +=1

class GameObject:
	def __init__(self):
		self.image = 0
		self.rect = 0
		self.can_draw = True

	def move(self,x,y):
		self.rect.move_ip(x,y)

	def draw(self,surf):
		if(self.can_draw):
			surf.blit(self.image,self.rect)

	def add(self,img):
		self.image = img
		self.rect = img.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

	def collide_one(self,obj,use_rect=False):
		if(use_rect):
			return self.collide_one_rect(obj)
		else:
			return self.collide_one_mask(obj)

	def collide_one_mask(self,obj):
		if(self == obj):
			raise Exception("Same Value Included")
		return collide_mask(self,obj)
	def collide_one_rect(self,obj):
		if(self == obj):
			raise Exception("Same Value Included")
		return self.rect.colliderect(obj.rect)

	def collide_many(self,obj_list,use_rect=False):
		for obj in obj_list:
			if(self == obj):
				continue
			if(self.collide_one(obj,use_rect=use_rect)):
				return (True,obj)
		return False


class Odd_Car(GameObject):
	def __init__(self):
		super().__init__()
		self._cur_pos = 0

	def reset(self,_list=[]):
		global col
		self.add(ALL_CARS[random.randrange(0,CARS_LEN)])
		random.seed(random.randrange(32252,472640248850))
		self.rect.bottom = random.randrange(-250,0) 
		self._cur_pos = random.randrange(0,4)
		self.rect.left = int(self._cur_pos*WIDTH/4+25)
		cond = self.collide_many(_list)
		if(cond):
			self.rect.bottom = cond[1].rect.top + random.randrange(-200,-150) -4

	def move(self,speed_y,_m_list):
		super().move(0,speed_y)
		if(self.rect.top >= HEIGHT):
			add_score()
			self.reset(_m_list)

WALL_GAP = 5

class Player_Car(GameObject):
	def __init__(self):
		super().__init__()
		self.add(player_car)
		self.fly_no = 1
		self.fly_power = 0

	def move(self,speed):
		key = pygame.key.get_pressed()
		if key[K_RIGHT] and (self.rect.right+12)<(WIDTH+WALL_GAP):
			super().move(speed,0)
		elif key[K_LEFT] and self.rect.left > (0+WALL_GAP):
			super().move(-speed,0)
		elif key[K_UP]  and self.rect.top > 0:
			super().move(0,-speed)
		elif key[K_DOWN] and self.rect.bottom<HEIGHT:
			super().move(0,speed)
		else:
			pass
			
	def activate_fly(self):
		self.fly_power = 100
		self.fly_no -= 1
		update_score()
	def move_xy(self,x,y):
		if ( (self.rect.right+12)<(WIDTH+WALL_GAP) and self.rect.left> (0+WALL_GAP) and 
				self.rect.top > 0 and self.rect.bottom<HEIGHT):
			super().move(x,y)
	def move_fly_xy(self,x,y):
		if (self.rect.top > 0):
			super().move(x,y)
	def start(self):
		self.rect.bottom = HEIGHT - 10
		self.rect.left = int(random.randrange(0,4)*(WIDTH/4)+25)

def grow_cars(_num):
	global bad_cars
	bad_cars = []
	for i in range(_num):
		kst = Odd_Car()
		kst.reset(bad_cars)
		bad_cars.append(kst)

def move_cars():
	for _car in bad_cars:
		_car.move(bad_car_speed,bad_cars)

def draw_cars(_surf):
	for _car in bad_cars:
		_car.draw(_surf)

bad_car_event = pygame.USEREVENT + 6
pygame.time.set_timer(bad_car_event,int(2000))



font_obj = pygame.font.SysFont("arial",30,True,True)

def add_score():
	global Score_board,Score_rect,my_score,fly_board
	my_score += 1
	if(my_score and my_score%10==0):
		my_car.fly_no += 1
	Score_board = font_obj.render(f"Score: {my_score}",True,RED)
	fly_board = font_obj.render(f"Fly: {my_car.fly_no}",True,BLUE)
	Score_rect = Score_board.get_rect()
	Score_rect.topright = (WIDTH-5,0+5)

def update_score():
	global Score_board,Score_rect,my_score,fly_board
	Score_board = font_obj.render(f"Score: {my_score}",True,RED)
	fly_board = font_obj.render(f"Fly: {my_car.fly_no}",True,BLUE)
	Score_rect = Score_board.get_rect()
	Score_rect.topright = (WIDTH-5,0+5)

#managing road
my_road = road()
my_road._img_screen("../cars/back_car.jpg")
my_road.custom(0)
my_road._img_screen("../cars/back_car.jpg")
my_road.custom(1,[BLACK,WHITE])
d_count = 0
def move_road():
	global d_count
	if(d_count%2 == 0):
		my_road.put_screen(0,display_surf)
		d_count = 0
	else:
		my_road.put_screen(1,display_surf)

Road_event = pygame.USEREVENT + 5
pygame.time.set_timer(Road_event,int(1000/4))

#This is game_over
gm_obj = pygame.font.SysFont("arial",50,True,True)
gm_score_obj = pygame.font.SysFont("arial",70,True,True)
gm_surf = pygame.Surface((250,150))
def game_over(_surf):
	gm_surf.fill(WHITE)
	_board = gm_obj.render(f"Game Over",True,RED)
	gm_surf.blit(_board,(int((250-_board.get_rect().width)/2),5))
	_board = gm_score_obj.render(f"{my_score}",True,BLACK)
	gm_surf.blit(_board,(int((250-_board.get_rect().width)/2),50))
	_surf.blit(gm_surf,(int((WIDTH-250)/2),200))
	pygame.display.update()
	pygame.time.delay(500)


pygame.mixer.music.load("./music1.mid")
pygame.mixer.music.queue("./music2.mid")
music_cnt = 0
music_event = pygame.USEREVENT+8
pygame.mixer.music.set_endevent(music_event)
sound1 = pygame.mixer.Sound("./match1.wav")

def initalize():
	global bad_cars,bad_car_speed,max_bad_speed
	global my_speed,my_car,my_score
	#manage The bad_cars
	bad_cars = []
	bad_car_speed = 4
	max_bad_speed = 20
	grow_cars(4)
	#This is me
	my_speed = 10
	my_car = Player_Car()
	my_car.start()
	#managing Score_board
	my_score = -1
	add_score()
	pygame.mixer.music.play()

#my_car.fly_no = 50

def game_window():	
	GAME_PAUSED = False
	initalize()
	global d_count,bad_car_speed,music_cnt
	while  True:
		for event in pygame.event.get():
			if(event.type == QUIT):
				pygame.mixer.music.stop()
				return main_window()
			elif(event.type == Road_event and not GAME_PAUSED):
				d_count +=1
			elif(event.type == bad_car_event and not GAME_PAUSED):
				if(bad_car_speed<max_bad_speed):
					bad_car_speed+= 1
				elif(bad_car_speed >= max_bad_speed):
					bad_car_speed -= 1
			elif event.type == KEYDOWN and event.key == K_a and my_car.fly_no and not my_car.fly_power and not GAME_PAUSED:
				my_car.activate_fly()
			elif event.type == music_event and not GAME_PAUSED:
				if(music_cnt%2 == 0):
					pygame.mixer.music.queue("./music1.mid")
					music_cnt = 0
				else:
					pygame.mixer.music.queue("./music2.mid")
				music_cnt += 1
			elif event.type == KEYDOWN and event.key == K_p:
				GAME_PAUSED = not GAME_PAUSED
				if(GAME_PAUSED):
					pygame.mixer.music.stop()
				else:
					pygame.mixer.music.play(-1,0.0)

		if(GAME_PAUSED):
			continue
		move_road()
		move_cars()
		draw_cars(display_surf)
		my_car.move(my_speed)
		my_car.draw(display_surf)
		if(my_car.collide_many(bad_cars) and not my_car.fly_power):
			sound1.play()
			game_over(display_surf)
			pygame.mixer.music.stop()
			pygame.time.delay(1000)
			return main_window()
		if(my_car.fly_power):
			my_car.move_fly_xy(0,-10)
			my_car.fly_power -= 5
		display_surf.blit(Score_board,Score_rect)
		display_surf.blit(fly_board,(5,5))
		#display_surf.blit(ALL_CARS[int(random.randrange(0,CARS_LEN))],(25,50))
		pygame.display.update()
		clock.tick(FPS)

def main_window():
	width_box = 100
	height_box = 50
	pen_obj = pygame.font.SysFont("arial",70,True,True)
	game_head = pen_obj.render("SAVE MY CAR",True,WHITE)
	head_rect = game_head.get_rect()
	head_rect.center = (WIDTH/2,50)
	pen_obj = pygame.font.SysFont("arial",50,True,True)
	play_box = pen_obj.render("   PLAY   ",True,GREEN,WHITE)
	play_box_rect = play_box.get_rect()
	play_box_rect.center = (WIDTH/2,150)
	qw1 = play_box_rect
	qw1.size = (qw1.width+5,qw1.height+5)
	qw1.top -= 10
	qw1.left -= 10

	quit_box = pen_obj.render("   QUIT   ",True,GREEN,WHITE)
	quit_box_rect = quit_box.get_rect()
	quit_box_rect.center = (WIDTH/2,250)
	qw2 = quit_box_rect
	qw2.size = (qw2.width+5,qw2.height+5)
	qw2.top -= 10
	qw2.left -= 10
	while True:
		for event in pygame.event.get():
			if(event.type==QUIT):
				pygame.quit()
				sys.exit()
		display_surf.fill(BLUE)
		display_surf.blit(game_head,head_rect)
		display_surf.blit(play_box,play_box_rect)
		display_surf.blit(quit_box,quit_box_rect)
		position = pygame.mouse.get_pos()
		pressed = pygame.mouse.get_pressed()
		if(play_box_rect.collidepoint(position)):
			pygame.draw.rect(display_surf,BLACK,qw1,10)
			if(pressed[0]):
				pygame.draw.rect(display_surf,RED,qw1,10)
				pygame.display.update()
				pygame.time.delay(200)
				game_window()
		elif(quit_box_rect.collidepoint(position)):
			pygame.draw.rect(display_surf,BLACK,qw2,10)
			if(pressed[0]):
				pygame.draw.rect(display_surf,RED,qw2,10)
				pygame.display.update()
				pygame.time.delay(200)
				pygame.quit()
				sys.exit()
		pygame.display.update()
main_window()

#how to play game
# use arrow key to move
# press a to fly
#press p to pause