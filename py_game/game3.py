import pygame
from pygame.locals import *
import sys
import random
from copy import deepcopy as d_copy
#my colors
BLACK  = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ANCOLOR = (125,125,125)
WHITE = (255,255,255)
YELLOW = (255,255,0)
MDF_1 = (255,0,255)
MDF_2 = (0,255,255)
MDF_3 = (125,78,255)
MDF_4 = (19,100,125)
MDF_5 = (45,45,45)
MDF_6 = (180,180,180)
MDF_7 = (120,45,59)
COLORS_LIST = [BLUE,GREEN,ANCOLOR,MDF_1,MDF_2,MDF_3,MDF_4,MDF_5,MDF_6,MDF_7]
WARN_COLOR = [RED,YELLOW]
MY_SNAKE_COLOR = [BLACK,WHITE]
FPS = 22
WIDTH,HEIGHT = (550,600) 

pygame.init()
display_surf = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("my_second_game")
clock = pygame.time.Clock()
music = pygame.mixer.music.load("music2.mid")
sound1 = pygame.mixer.Sound("match2.wav")
sound2 = pygame.mixer.Sound("match5.wav")
box_size = (20,20)
box_space = (0,0)
_margin = (20,20)
min_food = 1
max_food = 5

#margin = (10,10)

FOOD_COLOR = [
	(255,0,255),
	(200,100,45),
	(145,67,52),
	(90,90,90)
]

reduce_timer_speed = 10
max_auto_timer = 150
min_auto_timer=800
change_timer = 800

allow_barrier = True
show_board = False

def define_board(_size=(WIDTH,HEIGHT),_color=[BLUE,GREEN],box_size = (50,50),box_space = (4,4),
	_margin = (25,25),_background = RED,_len_box = (10,10),_need_rect = False,_width=0):
	global count_x,count_y
	_surf = pygame.Surface((_size[0]-2*_margin[0],_size[1]-2*_margin[1]))
	if _background != 0:
		_surf.fill(_background)
	_rect = _surf.get_rect()
	_rect.topleft = _margin
	if type(_len_box) == tuple or type(_len_box) == list:
		count_x,count_y = _len_box
	else:
		count_x = int((_rect.width-box_space[0])/(box_size[0]+box_space[0]))
		count_y = int((_rect.height-box_space[1])/(box_size[1]+box_space[1]))
	m_x = 0
	cols = []
	for x in range(count_x):
		m_y = 0
		rows = []
		for y in range(count_y):
			pygame.draw.rect(_surf,_color[(m_x%2+m_y)%2],
				(
					box_size[0]*x + box_space[0]*(x+1),
					box_size[1]*y + box_space[1]*(y+1),
					box_size[0],
					box_size[1]
				),_width
			)

			if(_need_rect):
				_z_rect = pygame.Rect(_margin[0]+ box_size[0]*x + box_space[0]*(x+1),
					_margin[1]+box_size[1]*y + box_space[1]*(y+1),
					box_size[0],
					box_size[1]
					)
				rows.append(_z_rect)
			m_y += 1

		if(_need_rect):
			cols.append(rows)
		m_x += 1
	return (_surf,_rect,cols)

def board_hover(_surf,_color=RED,_list_list = [],_width=0):
	position = pygame.mouse.get_pos()
	for rows in _list_list:
		for _p_rect in rows:
			if(_p_rect.collidepoint(position)):
				pygame.draw.rect(_surf,_color,_p_rect,_width)
	#print(display_surf.get_at(position))



class GameObject:
	def __init__(self):
		self.image = 0
		self.rect = 0

	def move(self,x,y):
		self.rect.move_ip(x,y)

	def draw(self,surf):
		surf.blit(self.image,self.rect)

	def add(self,img):
		self.image = img
		self.rect = img.get_rect()

	def collide_one(self,obj):
		if(self == obj):
			raise Exception("Same Value Included")
		return self.rect.colliderect(obj.rect)

	def collide_many(self,obj_list):
		for obj in obj_list:
			if(self == obj):
				continue
			if(self.collide_one(obj)):
				return (True,obj)
		return False

class Box(GameObject):
	UP = 0
	DOWN = 1
	RIGHT = 3
	LEFT = 4
	def __init__(self,_color= WHITE,_size=(20,20),_margin=(0,0),_box_space=(0,0),_min_box_pos=(0,0),_max_box_pos=(10,10),_init_coord=(0,0)):
		super().__init__()
		self._size = _size
		self._pos = (0,0)
		self._margin = _margin
		self._box_space = _box_space
		self._color = _color
		self._x = 0
		self._y = 0
		self._max_box_pos = _max_box_pos
		self._min_box_pos = _min_box_pos
		self._can_jump = False
		self.rect = pygame.Rect(*self.get_pos(*_init_coord),*self._size)
		self._func = 0

	def add_func(self,func):
		self._func = func
	def add(self,img):
		self.img = pygame.transform.scale(img,self._size)

	def get_coord(self):
		return (self._x,self._y)

	def get_pos(self,x,y,_func=0):
		if(x<self._min_box_pos[0] or x>self._max_box_pos[0] or
			y<self._min_box_pos[1] or y>self._max_box_pos[1]):
			#print("hit wall")
			if(self._func):
				self._func(self)
			if(self._can_jump):
				self.jump_wall(x,y)
		else:
			self._x,self._y = x,y
			pos_x = self._margin[0] + self._size[0]*x +self._box_space[0]*(x+1)
			pos_y = self._margin[1] + self._size[1]*y +self._box_space[1]*(y+1)
			self._pos = (pos_x,pos_y)
		return self._pos
	def look_ahead(self,_num):
		temp_pos = self.get_coord()
		temp_func = self._func
		self._func = 0
		if(_num == Box.UP):
			self.move_up()
		elif(_num == Box.DOWN):
			self.move_down()
		elif(_num == Box.RIGHT):
			self.move_right()
		elif(_num == Box.LEFT):
			self.move_left()

		k_bool = self.get_coord() == temp_pos;
		self.move(*temp_pos)
		self._func = temp_func
		return k_bool

	def can_bypass(self):
		self._can_jump = True

	def no_bypass(self):
		self._can_jump = False
	

	def jump_wall(self,x,y):
		if(x<self._min_box_pos[0]):
			x = self._max_box_pos[0]
		elif(x>self._max_box_pos[0]):
			x = self._min_box_pos[0]
		else:
			pass

		if(y<self._min_box_pos[1]):
			y = self._max_box_pos[1]
		elif(y>self._max_box_pos[1]):
			y = self._min_box_pos[1]
		else:
			pass

		self.move(x,y)

	def move(self,x,y):
		self.rect.topleft =self. get_pos(x,y)
		#print(x,y)

	def move_rel(self,x,y):
		self.move(self._x+x,self._y+y)
		#print(self._x,self._y)

	def move_up(self):
		self.move_rel(0,-1)

	def move_down(self):
		self.move_rel(0,1)

	def move_left(self):
		self.move_rel(-1,0)

	def move_right(self):
		self.move_rel(1,0)

	def draw_rect(self,_surf,_width=0,_color=0):
		if(_color==0):
			_color = self._color
		pygame.draw.rect(_surf,_color,self.rect,_width)

	def draw_circle(self,_surf,_radius=0,_width=0,_color=0):
		if(_color==0):
			_color = self._color
		if(not _radius):
			_radius = int( min(self.rect.size)/2)
		pygame.draw.circle(_surf,_color,self.rect.center,_radius,_width)

	def draw_ellipse(self,_surf,_width=0,_color=0):
		if(_color==0):
			_color = self._color
		pygame.draw.ellipse(_surf,_color,self.rect,_width)


def move_act():
	key = pygame.key.get_pressed()
	if key[K_RIGHT]:
		my_box.move_right()
	elif key[K_LEFT]:
		my_box.move_left()
	elif key[K_UP]:
		my_box.move_up()
	elif key[K_DOWN]:
		my_box.move_down()
	else:
		pass

move_list_pos = [0,0,0,0] #up,left,right,down
def move_act_1():
	global move_list_pos
	for event in pygame.event.get([KEYDOWN,KEYUP]):
		if(event.type == KEYDOWN):
			if event.key == K_RIGHT:
				move_list_pos = [0,0,1,0] 
			elif event.key == K_LEFT:
				move_list_pos = [0,1,0,0] 
			elif event.key == K_UP:
				move_list_pos = [1,0,0,0] 
			elif event.key == K_DOWN:
				move_list_pos = [0,0,0,1] 
			else:
				pass
		elif(event.type == KEYUP):
			move_list_pos = [0,0,0,0] 

	if(move_list_pos[0]):
		my_box.move_up()
	elif(move_list_pos[1]):
		my_box.move_left()
	elif(move_list_pos[2]):
		my_box.move_right()
	elif(move_list_pos[3]):
		my_box.move_down()
	else:
		pass


class Snake:
	UP = 0
	DOWN = 1
	RIGHT = 3
	LEFT = 4
	def __init__(self,_score,_color =[BLACK,WHITE],start_pos = (4,4),_size = box_size,error_color=[RED,YELLOW],_barrier=False):
		self._boxes = []
		self._boxes_len = 0
		self._size = _size
		self._color = _color
		self.error_color = error_color
		self._dir=Snake.RIGHT
		self._score_board = _score
		self.game_over = 0
		self._gms_failed = False
		self.zx_auto = True
		self._barrier = _barrier
		bnt_1 = Box(_color=_color[1],_size = box_size,_box_space = box_space,_margin = _margin,_max_box_pos=(count_x-1,count_y-1))
		bnt_1.move(*start_pos)
		self._last_pos = d_copy(bnt_1.rect)
		self._last_box_coord = bnt_1.get_coord()
		bnt_1.move_right()
		self._new_pos = d_copy(bnt_1.rect)
		self._new_box_coord = bnt_1.get_coord()
		self.add_box(_color=_color[0])
		self.add_box(_color=_color[1])
	
	def failed(self,_func):
		self.game_over = _func

	def _is_over(self):
		if(self._gms_failed):
			self.game_over()

	def add_food(self,_food):
		self._snake_food = _food

	def add_box(self,_color=0):
		if(_color == 0):
			_color = self._color[1]

		if(self._boxes_len == 0):
			_pos = self._new_box_coord
		else:
			_pos = self._last_box_coord
		#print("my_pos",_pos)
		pst_box = Box(_color=_color,_size = box_size,_box_space = box_space,_margin = _margin,_max_box_pos=(count_x-1,count_y-1))
		pst_box.move(*_pos)
		if(self._barrier):
			pst_box.no_bypass()
			pst_box.add_func(self.hit_barrier)
		else:
			pst_box.can_bypass()
		self._boxes.append(pst_box)
		#print("--",self._boxes[-1]._x,self._boxes[-1]._y)
		self._boxes_len += 1
	def update(self,_num):
		if(self._gms_failed or self._boxes[0].look_ahead(_num)):
			self._gms_failed = True
			self.hit_barrier()
			#print("here")
			return
		if(self._dir == _num):
			pass
		elif(not (self._dir+1 == _num  or self._dir-1 == _num)):
			self._dir = _num
		else:
			_num = self._dir

		self._last_box_coord = self._boxes[-1].get_coord()
		for i in range(self._boxes_len-1,0,-1):
			self._boxes[i].move(*self._boxes[i-1].get_coord())
		if(_num == Snake.UP):
			self._boxes[0].move_up()
		elif(_num == Snake.DOWN):
			self._boxes[0].move_down()
		elif(_num == Snake.LEFT):
			self._boxes[0].move_left()
		elif(_num == Snake.RIGHT):
			self._boxes[0].move_right()
		self._new_box_coord = self._boxes[0].get_coord()
		self.eat_self()

	def hit_barrier(self,args=0):
		self._color = self.error_color
		self._gms_failed = True
		#print("hitted")

	def eat_self(self):
		for i in range(self._boxes_len):
			ps_coord = self._boxes[i].get_coord()
			for j in range(self._boxes_len):
				if(i==j):
					continue
				else:
					if(ps_coord == self._boxes[j].get_coord()):
						self.hit_barrier()
						#print("collideed")
	def eat_food(self,food_list):
		_list = food_list._foods
		head_coord = self._boxes[0].get_coord()
		for _food in _list:
			if(head_coord == _food.get_coord()):
				food_list.remove(_food)
				self.eaten()

	def eaten(self):
		sound2.play()
		self.add_box()
		self._score_board.update_score()

	def draw(self,_surf):
		for i in range(1,self._boxes_len):
			self._boxes[i].draw_rect(_surf,_color = self._color[1])
		self._boxes[0].draw_circle(_surf,_color = self._color[0])

	def start_auto(self,_timer=min_auto_timer,_pn=change_timer):
		self._sn_timer = _timer
		self._event_id = pygame.USEREVENT +3
		pygame.time.set_timer(self._event_id,_timer)
		self._event_inc = pygame.USEREVENT +4
		pygame.time.set_timer(self._event_inc,_pn)

	def stop_auto(self):
		pygame.time.set_timer(self._event_id,0)
		pygame.time.set_timer(self._event_inc,0)

	def reset(self,_timer):
		self.stop_auto()
		self.start_auto(_timer)

	def _auto_move(self):
		for event in pygame.event.get([self._event_id,self._event_inc]):
			if(event.type == self._event_id):
				if(self.zx_auto):
					self.update(self._dir)

			elif(event.type == self._event_inc):
				if(self._sn_timer >=max_auto_timer):
					self.reset(self._sn_timer - reduce_timer_speed)
				else:
					pygame.time.set_timer(self._event_inc,0)
					#print(self._sn_timer)

	def move(self):
		key = pygame.key.get_pressed()
		self.zx_auto = False
		if key[K_RIGHT]:
			self.update(3)
		elif key[K_LEFT]:
			self.update(4)
		elif key[K_UP]:
			self.update(0)
		elif key[K_DOWN]:
			self.update(1)
		else:
			self.zx_auto = True
		self.eat_food(self._snake_food)


class Food(Box):
	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)
		self.tps = random.randrange(0,2)
	def generate_food(self,_snake):
		_list = []
		for _ps in _snake._boxes:
			_list.append(_ps.get_coord())
		_f_cod = random.randrange(self._min_box_pos[0],self._max_box_pos[0]),random.randrange(self._min_box_pos[1],self._max_box_pos[0])
		
		if(_f_cod in _list):
			for i in range(self._min_box_pos[0],self._max_box_pos[0]):
				for j in range(self._min_box_pos[1],self._max_box_pos[1]):
					if(not ((i,j) in _list)):
						_f_cod = (i,j)
		self.move(*_f_cod)
	def draw(self,_surf):
		color = random.choice(FOOD_COLOR)
		if(self.tps == 0):
			self.draw_circle(_surf, _color=color)
		elif(self.tps == 1):
			self.draw_rect(_surf,_color=color)
		elif(self.tps == 2):
			self.draw_ellipse(_surf,_color=color)

class Food_list:
	def __init__(self,_snake):
		self._foods = []
		self._snake=_snake

	def make_food(self,_num):
		for i in range(_num):
			_l_food = Food(_size = box_size,_box_space = box_space,_margin = _margin,_max_box_pos=(count_x-1,count_y-1))
			_l_food.generate_food(self._snake)
			self._foods.append(_l_food)

	def draw(self,_surf):
		for food in self._foods:
			food.draw(_surf)
	def remove(self,_fds):
		if(len(self._foods)>0):
			if(_fds in self._foods):
				self._foods.remove(_fds)
		else:
			self.make_food(random.randrange(min_food,max_food))
		self.empty()
	def empty(self):
		if(len(self._foods)==0):
			self.remove(0)
		else:
			return

class Score_board:
	def __init__(self,_color = WHITE,_font_size = 30,_font_name="arial",bold=True,italic=True,_place=1):
		self.font_obj  = pygame.font.SysFont(_font_name,_font_size,bold,italic)
		self.score = -1
		self.surf =  0
		self.rect = 0
		self._color = _color
		self.pos = 0
		self._place = _place
		self.update_score()
	def update_score(self):
		self.score +=1
		self.surf =self. font_obj.render(f"Score {self.score}",True,self._color)
		self.rect = self.surf.get_rect()
	def draw(self,surf):
		if(self._place == 0):
			self.rect.topleft = (10,10)
		elif(self._place == 1):
			self.rect.topright = (WIDTH - 10,10)
		surf.blit(self.surf,self.rect)

class Game_board:
	def __init__(self,_size=(WIDTH,HEIGHT),_color=[BLUE,GREEN],box_size = (50,50),box_space = (4,4),
								_margin = (25,25),_background = RED,_len_box = (10,10),_need_rect = False,_width=0):
		self._board = define_board(_size=_size,_color=_color,box_size = box_size,box_space = box_space,
								_margin = _margin,_background = _background,_len_box = _len_box,_need_rect = _need_rect,_width=_width)
	
	def draw(self,surf):
		surf.blit(self._board[0],self._board[1])

	def hover(self,_surf,_color=(190,95,120)):
		board_hover(_surf,_color=_color,_list_list=self._board[2])

def game_over(score,_surf,_d_board):
	gm_obj = pygame.font.SysFont("arial",50,True,True)
	gm_score_obj = pygame.font.SysFont("arial",70,True,True)
	gm_surf = pygame.Surface((250,150))

	def _over():
		pygame.mixer.music.stop()
		sound1.play()
		pygame.time.wait(500)
		pygame.mixer.music.load("music1.mid")
		pygame.mixer.music.play(-1,0.0)
		gm_surf.fill(WHITE)
		_board = gm_obj.render(f"Game Over",True,RED)
		gm_surf.blit(_board,(int((250-_board.get_rect().width)/2),5))
		_board = gm_score_obj.render(f"{score.score}",True,BLACK)
		gm_surf.blit(_board,(int((250-_board.get_rect().width)/2),50))
		_surf.blit(gm_surf,(int((WIDTH-250)/2),200))
		pygame.display.update()
		pygame.time.delay(2000)
		main_window(_d_board)
	return _over

def get_val(lst,_num):
	bst  = []
	mnst = lst
	for i in range(_num):
		val = random.choice(lst)
		bst.append(val)
		lst.remove(val)
	return bst
#my_board = define_board(_color=[RED,GREEN],box_size=box_size,box_space=box_space,_margin=_margin,_background=0,_len_box = -1,_need_rect=True)
#my_box = Box(_size = box_size,_box_space = box_space,_margin = _margin,_max_box_pos=(count_x-1,count_y-1))

def game_window(want_board = True): 
	GAME_PAUSED = False
	my_color = d_copy(COLORS_LIST)
	screen_color,_barrier_color = get_val(my_color,2)
	barrier_width = int(box_size[0]/4)
	my_board = Game_board(_background=screen_color,_color= get_val(my_color,2),box_size=box_size,box_space=box_space,_margin=_margin,_len_box = -1,_need_rect=True)
	my_barrier = Box(_color = _barrier_color,_size = (count_x*(box_size[0]+box_space[0])+box_space[0],count_y*(box_size[1]+box_space[1])+box_space[1]),
			_box_space = (0,0),_margin = _margin)
	my_score = Score_board()
	gms_over = game_over(my_score,display_surf,want_board)
	my_snake = Snake(_color=MY_SNAKE_COLOR ,_score=my_score,start_pos=(4,4),_barrier = allow_barrier)
	my_snake.failed(gms_over)
	my_food = Food_list(my_snake)
	my_snake.add_food(my_food)
	my_food.empty()
	pygame.mixer.music.play(-1,0.0)
	my_snake.start_auto(500)
	while True:
		my_snake._auto_move()
		for event in pygame.event.get():
			if(event.type == QUIT):
				main_window(want_board)
			elif(event.type==KEYDOWN and event.key == K_p):
				GAME_PAUSED = not GAME_PAUSED
				if(GAME_PAUSED):
					pygame.mixer.music.stop()
				else:
					pygame.mixer.music.play(-1,0.0)
			else:
				pass

		if(GAME_PAUSED):
			continue

		display_surf.fill(screen_color)
		if(want_board):
			my_board.draw(display_surf)
		if(my_snake._barrier or True):
			my_barrier.draw_rect(display_surf,_width=barrier_width)
			#--my_board.hover(display_surf)
		#display_surf.blit(my_board[0],my_board[1])
		#board_hover(_color=(190,95,120),_list_list=my_board._board[2])	
		#move_act()
		#my_box.draw_circle(display_surf)
		my_snake.move()
		my_snake.draw(display_surf)
		my_food.draw(display_surf)
		my_score.draw(display_surf)
		my_snake._is_over()
		pygame.display.update()
		clock.tick(FPS)


def main_window(_d_board=True):
	pygame.mixer.music.stop()	
	pen_obj = pygame.font.SysFont("arial",70,True,True)
	game_head = pen_obj.render("SNAKEY",True,WHITE)
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
				game_window(_d_board)
		elif(quit_box_rect.collidepoint(position)):
			pygame.draw.rect(display_surf,BLACK,qw2,10)
			if(pressed[0]):
				pygame.draw.rect(display_surf,RED,qw2,10)
				pygame.display.update()
				pygame.time.delay(200)
				pygame.quit()
				sys.exit()
		pygame.display.update()


box_size = (20,20)
box_space = (3,3)
allow_barrier = False or 1
show_board = True and False 
main_window(show_board)

#how to play
#use arrows to control
#press p to pause