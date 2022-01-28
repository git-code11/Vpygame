import pygame
from pygame.locals import *
import sys
import random
import math
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
COLORS_LIST = [BLUE,ANCOLOR,MDF_1,MDF_2,MDF_3,MDF_4,MDF_5,MDF_6,MDF_7]
count_x,count_y = 5,5 
WALL_GAP = 5
FPS = 30
WIDTH,HEIGHT = (800,600) 
USE_RANDOM_BACKGROUND = True
SHOW_ARROW_ALWAYS = False
pygame.init()
display_surf = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("my_third_game")
clock = pygame.time.Clock()
music = pygame.mixer.music.load("music2.mid")
sound1 = pygame.mixer.Sound("match2.wav")
sound2 = pygame.mixer.Sound("match5.wav")
GUN_HEAT_EVENT = pygame.USEREVENT + 1
GUN_HEAT_REDUCER_EVENT = pygame.USEREVENT + 2
SHOOTING_HAS_NO_LIMIT = True
_background_1 = pygame.transform.scale(pygame.image.load("../cars/back_car.jpg"),(WIDTH,HEIGHT))
_background_2 = pygame.transform.scale(pygame.image.load("../cars/the_sky.jpg"),(WIDTH,HEIGHT))
_background_3 = pygame.Surface((WIDTH,HEIGHT))
_background_3.fill(GREEN)
_background_list = [_background_1,_background_2,_background_3]
class Game_board:
	def __init__(self,_size=(WIDTH,HEIGHT),_color=[BLUE,GREEN],box_size = (50,50),box_space = (4,4),
								_margin = (25,25),_background = RED,_len_box = (10,10),_need_rect = False,_width=0,use_rect_maker=False):
		self._size = _size
		if(not use_rect_maker):
			self._board = self.define_board(_size=_size,_color=_color,box_size = box_size,box_space = box_space,
									_margin = _margin,_background = _background,_len_box = _len_box,_need_rect = _need_rect,_width=_width)
		else:
			self._board = self.define_board_rect(_size=_size,box_size = box_size,box_space = box_space,
									_margin = _margin,_len_box = _len_box)
		self._row_X_col = self._board[3]
	
	def draw(self,surf):
		surf.blit(self._board[0],self._board[1])

	def hover(self,_surf,_color=(190,95,120)):
		self.board_hover(_surf,_color=_color,_list_list=self._board[2])

	def generate_list(self):
		x=len(self._board[2])
		y=len(self._board[2][0])

		lst = [0]*(x*y)
		k = 0
		for row in range(y):
			for col in range(x):
				lst[k] = self._board[2][col][row]
				k+= 1
		return lst
	
	def define_board(self,_size=(WIDTH,HEIGHT),_color=[BLUE,GREEN],box_size = (50,50),box_space = (4,4),
		_margin = (25,25),_background = RED,_len_box = (10,10),_need_rect = False,_width=0):
		#global count_x,count_y
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
		return (_surf,_rect,cols,(count_x,count_y))

	def define_board_rect(self,_size=(WIDTH-50,HEIGHT-50),box_size = (50,50),box_space = (4,4),
		_margin = (25,25),_len_box = (10,10)):
		#global count_x,count_y
		_surf=pygame.Surface(_size)
		_rect=pygame.Rect(*_margin,*_size)
		if type(_len_box) == tuple or type(_len_box) == list:
			count_x,count_y = _len_box
		else:
			count_x = int((_size[0]-box_space[0])/(box_size[0]+box_space[0]))
			count_y = int((_size[1]-box_space[1])/(box_size[1]+box_space[1]))
		cols = []
		for x in range(count_x):
			rows = []
			for y in range(count_y):
				_z_rect = pygame.Rect(_margin[0]+ box_size[0]*x + box_space[0]*(x+1),
				_margin[1]+box_size[1]*y + box_space[1]*(y+1),
				box_size[0],
				box_size[1]
				)
				rows.append(_z_rect)
			cols.append(rows)
	
		return (_surf,_rect,cols,(count_x,count_y))


	def board_hover(self,_surf,_color=RED,_list_list = [],_width=0):
		position = pygame.mouse.get_pos()
		for rows in _list_list:
			for _p_rect in rows:
				if(_p_rect.collidepoint(position)):
					pygame.draw.rect(_surf,_color,_p_rect,_width)
		#print(display_surf.get_at(position))


class Score_board:
	def __init__(self,_color = WHITE,_font_size = 30,_font_name="arial",bold=True,italic=True,_place=1):
		self.font_obj  = pygame.font.SysFont(_font_name,_font_size,bold,italic)
		self.score = -1
		self.surf =  0
		self.rect = 0
		self._color = _color
		self.pos = 0
		self._place = _place
		self.win_game = "STILL_PLAYING"
		self.mnst = 0
		self.update_score()
		self.make_game_over_board()
	def update_score(self):
		self.score +=1
		self.surf =self.font_obj.render(f"Score {self.score}",True,self._color)
		self.rect = self.surf.get_rect()
	
	def draw(self,surf):
		if(self._place == 0):
			self.rect.topleft = (10,10)
		elif(self._place == 1):
			self.rect.topright = (WIDTH - 10,10)
		surf.blit(self.surf,self.rect)

	def game_notify_board_(self,_title="Game Over",_window_size = (WIDTH,HEIGHT),_displayed_box_size = (250,150),_font_size=(50,70),_font_name=("arial","arial")):
		_displayed_box_size = list(_displayed_box_size)
		if(_displayed_box_size[0]<_font_size[0]*2):
			_displayed_box_size[0] = 300

		if(_displayed_box_size[1]<_font_size[1]*2):
			_displayed_box_size[1] = _font_size[1]*2+10

		gm_obj = pygame.font.SysFont(_font_name[0],_font_size[0],True,True)
		gm_score_obj = pygame.font.SysFont(_font_name[1],_font_size[1],True,True)
		gm_surf = pygame.Surface(_displayed_box_size)
		rect_pd = gm_surf.get_rect()
		rect_pd.center = (_window_size[0]/2,_window_size[1]/2)

		def _over(_surf):
			pygame.mixer.music.stop()
			pygame.time.wait(500)
			pygame.mixer.music.load("music1.mid")
			pygame.mixer.music.play(-1,0.0)
			gm_surf.fill(WHITE)
			_board = gm_obj.render(_title,True,RED)
			gm_surf.blit(_board,(int((_displayed_box_size[0]-_board.get_rect().width)/2),int(_displayed_box_size[1]/2) - _board.get_rect().size[1]))
			_board_2 = gm_score_obj.render(f"{self.score}",True,BLACK)
			gm_surf.blit(_board_2,(int((_displayed_box_size[0]-_board_2.get_rect().width)/2),int(_displayed_box_size[1]/2) + 5))
			_surf.blit(gm_surf,rect_pd)
			pygame.display.update()
			pygame.time.delay(3000)
			#print("Done")
			main_window()
		return _over

	def make_game_over_board(self):
		self.game_over_func = self.game_notify_board_()
		self.game_win_func = self.game_notify_board_(_title="Congratulation",_displayed_box_size = (300,150))
	
	def game_is_over(self,_surf):
		if(not self.win_game and self.win_game != "STILL_PLAYING"):
			self.game_over_func(_surf)

	def game_is_win(self,_surf):
		if(self.mnst):
			self.mnst+= 1
		if(self.win_game and self.win_game != "STILL_PLAYING" and self.mnst>10):
			self.game_win_func(_surf)

	def failed(self):
		self.win_game = False

	def win(self):
		self.win_game = True
		self.mnst = 1


class GameObject:
	UP = 0
	DOWN = 1
	RIGHT = 3
	LEFT = 4
	def __init__(self):
		self.image = 0
		self.rect = 0
		self.mask = 0
	def move(self,x,y):
		self.rect.move_ip(x,y)

	def move_up(self,_dist):
		self.move(0,-_dist)

	def move_down(self,_dist):
		self.move(0,_dist)

	def move_right(self,_dist):
		self.move(_dist,0)

	def move_left(self,_dist):
		self.move(-_dist,0)

	def change_center(self,x,y):
		self.rect.center = (x,y)
	
	def draw(self,surf):
		surf.blit(self.image,self.rect)

	def add(self,img):
		self.image = img
		self.rect = img.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

	def collide_one(self,obj):
		if(self == obj):
			raise Exception("Same Value Included")
		print(self,obj)
		print(obj.mask.overlap(self.mask,((obj.rect.top - self.rect.top),(obj.rect.left - self.rect.left))))
		return self.mask.overlap(obj.mask,((self.rect.top - obj.rect.top),(self.rect.left - obj.rect.left))) != None

	def collide_many(self,obj_list):
		for obj in obj_list:
			if(self == obj):
				continue
			if(self.collide_one(obj)):
				return (True,obj)
		return False

	def is_inside(self,pos):
		return self.rect.collidepoint(pos)

class Game_box(GameObject):
	USING_ABS_RECT = 6
	USING_REL_RECT = 7
	def __init__(self,_color= WHITE,_size=(20,20),_margin=(0,0),_init_coord=(0,0),_background=BLACK,abs_min = (0,0),abs_max=(WIDTH,HEIGHT)):
		super().__init__()
		self._size = _size
		self._margin = _margin
		self._color = _color
		self._background = _background
		self.rect = pygame.Rect(*_init_coord,*self._size)
		self.abs_rect = pygame.Rect(*self.get_abs_pos(),*self._size)
		self._surface_make()
		self.abs_max = abs_max
		self.abs_min = abs_min
		
	def _surface_make(self):
		self.image = pygame.Surface(self._size)
		if(self._background):
			self.image.fill(self._background)
	def add(self,img):
		self.image = pygame.transform.scale(img,self._size)
		super().add(self.image)

	def get_abs_pos(self):
		return (self.rect.left + self._margin[0],self.rect.top +self._margin[1])
	
	def get_rel_pos(self):
		return (self.abs_rect.left - self._margin[0],self.abs_rect.top - self._margin[1])
	
	def reset_abs_pos(self,x,y):
		self.abs_rect.topleft = (x,y)
		self._margin = (x,y)
		self.rect.topleft = (0,0)

	def reset_rel_pos(self,x,y):
		self.rect.topleft = x,y
		self.abs_rect.topleft = self.get_abs_pos()

	def update_rel_pos(self,x,y):
		self.rect.topleft = (self.rect.left+x,self.rect.top+y)
		self.abs_rect.topleft = (self.abs_rect.left+x,self.abs_rect.top+y)

	def update_abs_pos(self,x,y):
		self.abs_rect.topleft = (self.abs_rect.left+x,self.abs_rect.top+y)
		self.rect.topleft = (self.abs_rect.left-self._margin[0],self.abs_rect.top-self._margin[1])

	def reset_margin(self,x,y):
		self._margin = (x,y)
		self.abs_rect.topleft = self.get_abs_pos()
		
	def update_rel_margin(self,x,y):
		self.reset_margin(self._margin[0]+x,self._margin[1]+y)

	def draw(self,surf,_rect_type=7):
		if(_rect_type == Game_box.USING_ABS_RECT):
			surf.blit(self.image,self.abs_rect)
		else:
			surf.blit(self.image,self.rect)

	def draw_rel(self,surf):
		self.draw(surf,7)

	def draw_abs(self,surf):
		self.draw(surf,6)
	
	def use_rect(self,_color=0,_width=0,_clear=True):
		if(not _color):
			_color = self._color
		if(_clear):
			self._surface_make()
		pygame.draw.rect(self.image,_color,self.rect,_width)
		self.add(self.image)

	def use_circle(self,_color=0,_radius=0,_width=0,_clear=True):
		if(not _color):
			_color = self._color
			_color = self._color
		if(not _radius):
			_radius = int( min(self.rect.size)/2)
		if(_clear):
			self._surface_make()
		l = list(_color)
		if(l[0]>1):
			l[0] = l[0]-1
		else:
			l[0] = 250
		self.image.fill(l)
		self.image.set_colorkey(l)
		pygame.draw.circle(self.image,_color,self.rect.center,_radius,_width)
		self.add(self.image)

	def move(self,x,y,_func=0,_force=False):
		if(self.abs_rect.left + x <self.abs_min[0] or self.abs_rect.right + x > self.abs_max[0]
			or self.abs_rect.top + x <self.abs_min[1] or self.abs_rect.bottom + y >self.abs_max[1]):
			#print("height-box_space")
			if(_func):
				_func(self)
			if(_force):
				self.update_rel_pos(x,y)
			#print("touched_body")
			return 
		self.update_rel_pos(x,y)

	def change_rel_center(self,x,y):
		self.rect.rect.center = (x,y)
		self.reset_rel_pos(*self.rect.topleft)

	def change_abs_center(self,x,y):
		self.rect.abs_rect.center = (x,y)
		self.reset_abs_pos(*self.rect.topleft)

	def collide_one(self,obj):
		if(self == obj):
			raise Exception("Same Value Included")
		print(self,obj)
		print(obj.mask.overlap(self.mask,((obj.abs_rect.top - self.abs_rect.top),(obj.abs_rect.left - self.abs_rect.left))))
		return self.mask.overlap(obj.mask,((self.abs_rect.top - obj.abs_rect.top),(self.abs_rect.left - obj.abs_rect.left))) != None

	def point_inside_box_me(self,pos):
		return self.abs_rect.collidepoint(pos)

	def box_inside_box_me(self,_box):
		return self.abs_rect.contains(_box.abs_rect)

	def box_inside_box_me_mask(self,_box):
		super()
		return self.abs_rect.contains(_box.abs_rect)
	
def get_random(lst,_num):
	bst  = []
	for i in range(_num):
		val = random.choice(lst)
		bst.append(val)
		lst.remove(val)
	return bst

class Blocks:
	pass

THROW_BALL_EVENT = pygame.USEREVENT +3
PLAYER_MARGIN_FROM_BOTTOM = 10 
class Player(GameObject):
	def __init__(self,num_blocks,block_size,_color=[BLUE,WHITE],_center_pos=0,abs_max=(WIDTH,HEIGHT),abs_min=(0,0)):
		super().__init__()
		self._num_blocks_x = num_blocks
		self.block_size = block_size
		self.has_gun = False
		self.gun_1 = Gun(_size=(block_size[0],block_size[1]*3),_color=_color[1])
		self.gun_2 = Gun(_size=(block_size[0],block_size[1]*3),_color=_color[1])
		self._bart = 0
		self._color = _color
		self.abs_max = abs_max
		self.abs_min = abs_min
		self.hold_ball_firm=False
		self.ball_on_board = True
		self.the_ball = 0
		self.start_ball =False
		self.first_move  = False
		self.the_game_is_already_started = False
		self.speed_set()
		self.load()
		if(not _center_pos):
			self.load_pos(WIDTH/2,HEIGHT-self._size[1]/2-PLAYER_MARGIN_FROM_BOTTOM)
	
	def show_arrow(self,surf,_control=True):
		if(self.ball_on_board or SHOW_ARROW_ALWAYS):
			self._bart.draw_arrow(surf)
		if(_control):
			self._bart.arrow_on_action()
			if(self.the_ball):
				self.arrow_rotate_ball(self.the_ball)

	def add_ball(self,_ball):
		self.the_ball = _ball
		self.the_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top -self.the_ball._size[1]/2)

	def enable_gun(self):
		self.has_gun = True
		self.load()

	def disable_gun(self):
		self.has_gun = False
		self.load()

	def load(self):
		surf_1 =Bart(_size=(self.block_size[0]*self._num_blocks_x,self.block_size[1]*2),_color=self._color[0])
		temp_rect = d_copy(self.rect)
		if(self.has_gun):
			self._size = (surf_1._size[0] + self.gun_1._size[0]*2,self.gun_1._size[1])
			mkt_surf = pygame.Surface(self._size)
			mkt_surf.fill(BLACK)
			mkt_surf.set_colorkey(BLACK)
			self.add(mkt_surf)

			self.gun_1.reset_rel_pos(0,0)
			self.gun_1.draw_rel(self.image)
			surf_1.reset_rel_pos(self.gun_1.rect.right,self.gun_1.rect.size[1]/2 - surf_1.rect.size[1]/2)
			surf_1.draw_rel(self.image)
			self.gun_2.reset_rel_pos(surf_1.rect.right,0)
			self.gun_2.draw_rel(self.image) 
		 
		else:
			self._size = surf_1._size
			self.add(pygame.Surface(self._size)) 
			surf_1.reset_rel_pos(0,0)
			surf_1.draw_rel(self.image)
		self._bart = surf_1
		if(temp_rect == 0):
			self.load_pos(WIDTH/2,HEIGHT/2)
		else:
			self.load_pos(*temp_rect.center)
	
	def update_pos(self,x,y):
		self.gun_1.reset_margin(x,y)
		self.gun_2.reset_margin(x,y)
		self._bart.reset_margin(x,y)
		self._bart.update_bart()
		if(self.the_ball and self.ball_on_board):
			self.the_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top-self.the_ball._size[1]/2)

	def load_pos(self,x,y):
		self.rect.center = (x,y)
		if(self.rect.left<0):
			self.rect.left = 0
		elif(self.rect.right>WIDTH):
			self.rect.right = WIDTH

		if(self.rect.bottom>HEIGHT):
			self.rect.bottom = HEIGHT

		self.update_pos(*self.rect.topleft)

	def shoot_with_gun(self,_surf,_default=True):
		if(not self.the_game_is_already_started):
			return
		if(not self.has_gun):
			return
		self.gun_1.show_bullets(_surf)
		self.gun_1.move_bullets()
		self.gun_2.show_bullets(_surf)
		self.gun_2.move_bullets()
		if(_default):
			key = pygame.key.get_pressed()
			if(key[K_SPACE]):
				self.gun_1.shoot()
				self.gun_2.shoot()
		else:
			for event in pygame.event.get(KEYDOWN):
				if(event.key == K_SPACE):
					self.gun_1.shoot()
					self.gun_2.shoot()

	def shooting_with_gun_init(self,_surf):
		self.shoot_with_gun(_surf,_default=False)

	def gun_reduce_heat(self):
		self.gun_1.reduce_heat()
		self.gun_2.reduce_heat()

	def gun_normal_reduce_heat(self):
		self.gun_1.norm_heat_reducer()
		self.gun_2.norm_heat_reducer()

	
	def change_center(self,x,y):
		self.load_pos(x,y)

	def speed_set(self,_speed = 10):
		self._speed_val = _speed

	def move(self,x,y):
		if(self.rect.left + x < self.abs_min[0]):
			self.rect.left = self.abs_min[0]
			x=0
		
		if(self.rect.right + x > self.abs_max[0]):
			self.rect.right = self.abs_max[0]
			x=0
		
		if(self.rect.top + y < self.abs_min[1]):
			self.rect.top = self.abs_min[1]
			y=0
		
		if(self.rect.bottom + y > self.abs_max[1]):
			self.rect.bottom = self.abs_max[1]
			y=0
		
		self.rect.top += y
		self.rect.left += x

		self.update_pos(*self.rect.topleft)
		#print(self.ball_on_board)
	def move_player_by_key(self):
		key = pygame.key.get_pressed()
		if key[K_RIGHT]:
			self.move(self._speed_val,0)
			
		elif key[K_LEFT]:
			self.move(-self._speed_val,0)
		elif key[K_UP] and False:
			self.move(0,-self._speed_val)
		elif key[K_DOWN] and False:
			self.move(0,self._speed_val)
		elif key[K_a]:
			self.the_game_is_already_started = True
			self.throw_ball()
		elif key[K_h]:
			self.hold_ball_firm = True
			pass

	def move_player_by_mouse(self):
		pos = pygame.mouse.get_pos()
		self.load_pos(*pos)

	def bullet_hit_block(self,blocks):
		if(self.has_gun):
			self.gun_1.bullets_collide_with_block(blocks)
			self.gun_2.bullets_collide_with_block(blocks)

	def collide_with_ball(self,_ball=0):
		if(not self.start_ball):
			return
		if(not _ball):
			_ball = self.the_ball
		if(self._bart.collide_one(_ball)):
			if(self.hold_ball_firm):
				_ball.stop()
				_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top-self.the_ball._size[1]/2)
				#_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top)
				self.ball_on_board = True
				self.first_move = True
			else:
				#print("hello")
				if(self.first_move):
					_ball.hit_bart()
					self.first_move = False
				else:
					_ball.hit_player()
				self.ball_on_board = False
		elif(self.has_gun and (self.gun_1.collide_one(_ball) or self.gun_1.collide_one(_ball))):
			if(self.hold_ball_firm):
				_ball.stop()
				_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top-self.the_ball._size[1]/2)
				#_ball.reset(self._bart.abs_rect.centerx,self._bart.abs_rect.top)
				self.ball_on_board = True
				self.first_move = True
			else:
				if(self.first_move):
					_ball.hit_bart()
					self.first_move = False
				else:
					_ball.hit_player()
				self.ball_on_board = False
		else:
			pass
			#self.ball_on_board = False

	def arrow_rotate_ball(self,_ball=0):
		if(self.ball_on_board):
			if(not _ball):
				_ball = self.the_ball
			_ball.set_angle(self._bart.arrow.deg)

	def ball_hit_block(self,_blocks,_ball=0):
		if(not _ball):
			_ball =self.the_ball
		_ball.collide_with_blocks(_blocks)

	def show_ball(self,_surf,_ball=0):
		if(not _ball):
			_ball = self.the_ball
		_ball.draw(_surf)

	def throw_ball(self):
		if(self.ball_on_board):
			#print("qqq")
			self.arrow_rotate_ball(self.the_ball)
			pygame.time.set_timer(THROW_BALL_EVENT,100)
			self.ball_on_board = False
			self.hold_ball_firm = False
			self.moving_ball()
			self.start_ball = True
			self.first_move = True

	def moving_ball(self,_ball=0):
		#print("hello")
		if(not self.start_ball):
			return
		if(self.ball_on_board):
			pygame.time.set_timer(THROW_BALL_EVENT,0)
			return
		if(not _ball):
			_ball = self.the_ball
		_ball.move()
		#print(_ball._speed)


class Custom_box(Game_box):
	circle = 2
	square = 1
	image = 3
	def __init__(self,_size,_color=RED,_abs_post=(0,0),_img_type=1,_img_surf=0):
		super().__init__(_size=_size,_background=BLACK,_color=_color)
		self.image.set_colorkey(BLACK)
		self.reset_margin(*_abs_post)
		
		if(_img_type == Custom_box.circle):
			self.use_circle()
		elif(_img_type == Custom_box.image):
			self.add(_img_surf)
		else:
			self.use_rect()

class Bart(Custom_box):
	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)
		#self.image.set_colorkey(0)
		self.arrow = Arrow()
	def update_bart(self):
		self.arrow.reset_pos(self.abs_rect.centerx,self.abs_rect.top)

	def arrow_on_action(self):
		self.arrow.rotate_using_key(min_angle=0+15,max_angle=180-15)

	def draw_arrow(self,_surf):
		self.arrow.draw_distance(_surf)

	def collide_with_ball(self,_ball):
		pass

class Arrow:
	def __init__(self,_init_pos=(WIDTH/2,HEIGHT/2),_color=WHITE):
		self._init_pos = _init_pos
		self._color = _color
		self.deg = 90
		
	def move(self,x,y):
		self._init_pos = (self._init_pos[0]+x,self._init_pos[1]+y)
	def reset_pos(self,x,y):
		self._init_pos = (x,y)

	def draw(self,surf,abs_new_pos=(0,0),_color=WHITE,_width=2):
		pygame.draw.line(surf,_color,self._init_pos,abs_new_pos,_width)

	def draw_distance(self,surf,_dist=50,angle="qq",_color=WHITE,_width=2):
		if(angle == "qq"):
			angle = self.deg
		_abs_pos = [self._init_pos[0] + math.cos(math.radians(angle))*_dist,self._init_pos[1]  - math.sin(math.radians(angle))*_dist]
		self.draw(surf=surf,abs_new_pos=_abs_pos,_color=_color,_width=_width)

	def rotate_using_key(self,max_angle=180,min_angle=0):
		key = pygame.key.get_pressed()
		if(key[K_UP] and self.deg>min_angle):
			self.deg-= 15
		elif(key[K_DOWN] and self.deg<max_angle):
			self.deg+=15



class Gun(Custom_box):
	def __init__(self,_size,_color=BLUE,_abs_post=(0,0),_img_type=1,_img_surf=0):
		super().__init__(_size=_size,_color=_color,_abs_post=_abs_post,_img_type=_img_type,_img_surf=_img_surf)
		self._bullets = []
		self.bullet_property()
		self.heat_temp = 0
		self.can_shoot = True
		self.force_shoot = True and SHOOTING_HAS_NO_LIMIT
		if(not self.force_shoot):
			pygame.time.set_timer(GUN_HEAT_REDUCER_EVENT,500)
	def heated_up(self):
		if(self.force_shoot):
			return
		if(self.heat_temp>100):
			self.can_shoot = False
			pygame.time.set_timer(GUN_HEAT_EVENT,500)
			pygame.time.set_timer(GUN_HEAT_REDUCER_EVENT,0)
			
	def reduce_heat(self):
		self.heat_temp -= 5
		#print("hello in reduce_heat",self.heat_temp)
		if(self.heat_temp<90):
			self.can_shoot =True
			pygame.time.set_timer(GUN_HEAT_EVENT,0)
			pygame.time.set_timer(GUN_HEAT_REDUCER_EVENT,500)

	def norm_heat_reducer(self):
		#print("hello in reducer",self.heat_temp)
		if(self.heat_temp>2):   
			self.heat_temp -=3

	def load_bullets(self):
		bult = Bullets(_size=(self._size[0]/2,self._size[1]/4),_color=self._bullet_color,
			 _abs_post=(self.abs_rect.centerx - self._size[0]/4,self.abs_rect.top-self._size[1]/8))
		#_abs_post=(self.abs_rect.centerx - self._size[0]/2,self.abs_rect.top-self._size[1])
		self._bullets.append(bult)
	
	def bullet_property(self,_color=RED,_speed=(0,-10)):
		self._bullet_speed = _speed
		self._bullet_color = _color

	def shoot(self):
		if(self.can_shoot or self.force_shoot):
			self.load_bullets()
			self.heat_temp += 5
		self.move_bullets()
		self.heated_up()
	def move_bullets(self):
		k = len(self._bullets) 
		if(k):
			lent =  -self._bullets[0]._size[1] 
			for  bt in self._bullets:
				bt.move(self._bullet_speed[0],self._bullet_speed[1] + lent,self.bullet_delete)
	
	def show_bullets(self,_surf):
		for bt in self._bullets:
			bt.draw_abs(_surf)

	def bullet_delete(self,blt):
		if(blt in self._bullets):
			self._bullets.remove(blt)

	def bullets_collide_with_block(self,_block_list):
		for bullet in self._bullets:
			bullet.collide_with_blocks(_block_list,self.bullet_delete)



class Bullets(Custom_box):
	def __init__(self,_size,_color=RED,_abs_post=(0,0),_img_type=1,_img_surf=0):
		super().__init__(_size=_size,_color=_color,_abs_post=_abs_post,_img_type=_img_type,_img_surf=_img_surf)

	def collide_with_blocks(self,_block_list,func1=0):
		for blk in _block_list.blocks:
			if(blk == 0):
				continue
			if(self.abs_rect.colliderect(blk)):
				_block_list.hitted_block(blk)
				#print("block_meet_bullet")
				if(func1):
					func1(self)
				

class Block_List:
	def __init__(self,container_size=(int(WIDTH*0.9),int(HEIGHT*0.6)),_color=COLORS_LIST,box_size = (25,25),box_space = (4,4),
								_margin = (int(WIDTH*0.05),int(10)),_len_box = (10,10)):
		#blcoks variable holds block_rect
		block_board = Game_board(_size=container_size,box_size = box_size,box_space = box_space,
								_margin = _margin,_len_box =-1,use_rect_maker=True) 
		#(_surf,_rect,cols,(count_x,count_y))
		self._margin = _margin
		self.container_size = container_size
		self.block_size = box_size
		self.block_num_x_y = block_board._row_X_col
		self.blocks = block_board.generate_list()    
		self.temp_block = d_copy(self.blocks[0])
		self.block_live = [4]*len(self.blocks)
		self.reset_img_list()
		self.create_blocks_rect_img(colors=_color)
		self.bad_block_img_1 = pygame.Surface(self.block_size)
		self.bad_block_img_1.fill(YELLOW)
		self.bad_block_img_2 = pygame.Surface(self.block_size)
		self.bad_block_img_2.fill(RED)
		self._score = 0

	def add_win_score_board(self,score):
		self._score = score

	def create_blocks_rect_img(self,colors=COLORS_LIST):
		for color in colors:
			self.make_rect_block_image(_color=color)

	def make_rect_block_image(self,_color=BLUE):
		blk = pygame.Surface(self.block_size)
		blk.fill(_color)
		self.add_img(blk)

	def reset_img_list(self):
		self.img = []

	def add_img(self,_img):
		if(_img.get_rect().size == self.block_size):
			self.img.append(_img)
		else:
			self.img.append(pygame.transform.scale(_img,self.block_size))
	
	def add_block(self,x,y):
		if(x<self._margin[0]):
			x= _margin[0]
		if(x>self._margin[0]+self.container_size[0]):
			x= self._margin[0]+self.container_size[0]-self.block_size[0]
		if(y<self._margin[1]):
			y = _margin[1]
		if(y>self._margin[1]+self.container_size[1]):
			y= self._margin[1]+self.container_size[1]-self.block_size[1]
		_block = d_copy(self.temp_block)
		_block.topleft = (x,y)
		self.blocks.append(_block)

	def remove_block(self,_block):
		self.blocks.remove(_block)

	def hitted_block(self,_block):
		index = self.blocks.index(_block)
		self.block_live[index] -= 1
		if(self.block_live[index]):
			sound2.play()
			pass
			#self.block_live[index] -= 1
		else:
			sound1.play()
			self.blocks[index] = 0
			self._score.update_score()
		if(self._score.score == len(self.blocks)):
			self._score.win()

	def draw_blocks(self,_surf):
		lent = len(self.img)
		if(lent>0):
			z=0
			for block in self.blocks:
				z+= 1
				if(block == 0):
					continue
				#_surf.blit(self.img[random.randrange(0,lent)],block)
				index = self.blocks.index(block)
				if(self.block_live[index]==2):
					_surf.blit(self.bad_block_img_2,block)
				elif(self.block_live[index]==1):
					_surf.blit(self.bad_block_img_1,block)
				else:
					_surf.blit(self.img[z%lent],block)
		else:
			for block in self.blocks:
				if(block == 0):
					continue
				index = self.blocks.index(block)
				if(self.block_live[index]==2):
					_surf.blit(self.bad_block_img_2,block)
				elif(self.block_live[index]==1):
					_surf.blit(self.bad_block_img_1,block)
				else:
					_surf.blit(self.img[0],block)



class Ball(Custom_box):
	top_side = "TS"
	bottom_side = "BS"
	left_side="LS"
	right_side = "RS"
	def __init__(self,_size=[15,15],_color=YELLOW,_abs_post=(0,0),_img_type=2,_img_surf=0):
		super().__init__(_size=_size,_color=_color,_abs_post=_abs_post,_img_type=_img_type,_img_surf=_img_surf)
		self.use_circle()
		self._vel = 10
		self._speed = (0,0)
		self._temp_speed = (0,0)
		self._diff = 15
		self._bounce()
		self._score = 0
	
	def set_velocity(self,vel=10):
		self._vel = vel
	def add_fail_notice(self,score_bd=0):
		self._score = score_bd

	def stop(self):
		self._speed = (0,0)

	def set_angle(self,ang):
		#print("hello+++>>>")
		self._speed = self.eqn(angle=ang,_dist=self._vel)
		#print(self._speed)

	def pause(self):
		self._temp_speed = self._speed
		self._speed = self._temp_speed
	
	def unpause(self):
		self._speed = self._temp_speed
		self._temp_speed = (0,0)

	def eqn(self,angle,_dist):
		x = int(math.cos(math.radians(angle))*_dist)
		y = -int(math.sin(math.radians(angle))*_dist)
		return (x,y)
	def reset(self,x,y):
		self.rect.center = x,y

	def move_manual(self,x,y):
		self.rect.left += x
		self.rect.top += y
		#self.rect.move_ip(x,y)
		self.hit_environment()
	
	def move(self):
		#pygame.time.delay(100)
		self.move_manual(*self._speed)

	def _bounce(self,_dir="TS"):
		diff = self._diff
		#print(_dir)
		if(_dir == Ball.top_side):
			angle = random.randrange(0+diff,180-diff)
			self._speed = self.eqn(angle=angle,_dist=self._vel)
		elif(_dir == Ball.bottom_side):
			angle = random.randrange(180+diff,360-diff)
			self._speed = self.eqn(angle=angle,_dist=self._vel)
			#print(self._speed)
		elif(_dir == Ball.left_side):
			angle = random.randrange(90+diff,270-diff)
			self._speed = self.eqn(angle=angle,_dist=self._vel)
		elif(_dir == Ball.right_side):
			angle = random.randrange(-90+diff,90-diff)
			self._speed = self.eqn(angle=angle,_dist=self._vel)
		else:
			pass
		
	def hit_bart(self):
		self.move()

	def hit_player(self):
		temp = self._speed
		self._bounce()
		if(self._speed == temp):
			print("hhjjj")
			self._bounce()

	def hit_environment(self,_ball=0):
		if(self.rect.top<=0):
			self._bounce(_dir="BS")
		elif(self.rect.bottom>=HEIGHT):
			#self._bounce(_dir="TS")
			self._score.failed()
		elif(self.rect.left<=0):
			self._bounce(_dir="RS")
		elif(self.rect.right>=WIDTH):
			self._bounce(_dir="LS")
		else:
			pass

	def hit_block_2(self,block):		
		if(self.rect.bottom >= block.top and (block.left<= self.rect.left and block.right>=self.rect.left)):
			self._bounce(_dir="TS")
		elif(self.rect.top <= block.bottom and (block.left<= self.rect.left and block.right>= self.rect.left)):
			self._bounce(_dir="BS")
		elif(self.rect.left <= block.right and (block.top<= self.rect.top and block.bottom>=self.rect.top)):
			self._bounce(_dir="RS")
		elif(self.rect.right >= block.left and (block.top<= self.rect.top and block.bottom>= self.rect.top)):
			self._bounce(_dir="LS")
		else:
			if(self.rect.bottom >= block.top):
				self._bounce(_dir="TS")
			elif(self.rect.top <= block.bottom):
				self._bounce(_dir="BS")
			elif(self.rect.left-5 <= block.right):
				self._bounce(_dir="RS")
			elif(self.rect.right >= block.left):
				self._bounce(_dir="LS")
			else:
				pass
				#print("help me vic o")
			

	def hit_block(self,block):		
		if(self.rect.bottom >= block.top and self.rect.top < block.top):
			self._bounce(_dir="TS")
		elif(self.rect.top <= block.bottom and self.rect.top > block.top):
			self._bounce(_dir="BS")
		elif(self.rect.left <= block.right and self.rect.left > block.right):
			self._bounce(_dir="RS")
		elif(self.rect.right >= block.left and self.rect.left < block.right):
			self._bounce(_dir="LS")
		else:
			pass
			#print("help me vic o")

	def collide_with_blocks(self,_block_list):
		for blk in _block_list.blocks:
			if(blk == 0):
				continue
			if(self.rect.colliderect(blk)):
				#print("Balling")
				self.hit_block(blk)
				_block_list.hitted_block(blk)
				return


class BallList:
	def __init__(self):
		self.balls = []

	def add_ball(self,_ball):
		self.balls.append(_ball)

	def remove_ball(self,_ball):
		self.balls.remove(_ball)

	def throw(self,ball,x,y):
		pass


def game_window():
	GAME_PAUSED = False
	_size = (100,100)
	_margin = (50,50)
	box_size = (10,10)
	player_width = 15
	my_box_1 = Game_box(_margin=(0,0),_size=_size,_color=BLUE,_background=0)
	my_box_1.use_rect()

	my_box_2 = Game_box(_color=RED,_background=0)
	my_box_2.use_circle()
	my_box_2.move(10,10)
	print("-----------\n")
	#print(my_box_2.collide_one(my_box_1))
	#print(my_box_1.collide_one(my_box_2))
	print(my_box_1.mask.overlap(my_box_2.mask,((my_box_1.abs_rect.top - my_box_2.abs_rect.top),
		(my_box_1.abs_rect.left - my_box_2.abs_rect.left))) )
	print(my_box_1.mask.overlap(my_box_2.mask,((my_box_2.abs_rect.top - my_box_1.abs_rect.top),
		(my_box_2.abs_rect.left - my_box_1.abs_rect.left))) )

	print("-----------\n")
	#my_box_1.reset_margin(10,10)
	#print(my_box_1.box_inside_box_me(my_box_2))
	if(not USE_RANDOM_BACKGROUND):
		my_background = _background_list[1]
	else:
		my_background = _background_list[random.randrange(0,len(_background_list)-1)]

	my_player = Player(player_width,box_size)
	my_player.enable_gun()
	my_player.disable_gun()
	my_score = Score_board()
	#my_player.move(-10,-10)
	my_block = Block_List(container_size=(WIDTH*0.8,HEIGHT*0.5),_margin=(50,50),box_size=(30,15),box_space=(30,20))
	my_block.add_win_score_board(my_score)

	my_arrow = Arrow()

	my_ball = Ball()
	my_ball.set_velocity(15)
	my_player.add_ball(my_ball)

	my_ball.add_fail_notice(my_score)

	pygame.mixer.music.play(-1,0.0)
	while True:
		for event in pygame.event.get():
			if(event.type==QUIT):
				main_window()
			elif(event.type==GUN_HEAT_EVENT and not GAME_PAUSED):
				my_player.gun_reduce_heat()
			elif(event.type==GUN_HEAT_REDUCER_EVENT and not GAME_PAUSED):
				my_player.gun_normal_reduce_heat()
			elif(event.type == THROW_BALL_EVENT and not GAME_PAUSED):
				my_player.moving_ball()
			elif(event.type == KEYDOWN and event.key == K_p):
				GAME_PAUSED = not GAME_PAUSED
				if(GAME_PAUSED):
					pygame.mixer.music.stop()
				else:
					pygame.mixer.music.play(-1,0.0)
		if(GAME_PAUSED):
			continue	
		display_surf.blit(my_background,(0,0))
		my_box_1.draw_rel(display_surf)
		my_box_2.draw(display_surf)
		my_block.draw_blocks(display_surf)
		my_player.draw(display_surf)
		my_player.shoot_with_gun(display_surf)
		#my_player.shooting_with_gun_init(display_surf)
		my_player.bullet_hit_block(my_block)
		#my_player.move_player_by_mouse()
		my_player.move_player_by_key()
		#my_arrow.rotate_using_key(min_angle=0,max_angle=360)
		#my_arrow.draw_distance(display_surf)
		my_player.show_arrow(display_surf)
		my_player.show_ball(display_surf)
		my_player.ball_hit_block(_blocks=my_block)
		my_player.collide_with_ball()
		#print(my_player.ball_on_board)
		my_score.draw(display_surf)
		my_score.game_is_over(display_surf)
		my_score.game_is_win(display_surf)

		pygame.display.update()
		clock.tick(25)
		print("-----------\n")
		#print(my_box_2.collide_one(my_box_1))
		#print(my_box_1.collide_one(my_box_2))
		print(my_box_2.mask.overlap(my_box_1.mask,((my_box_1.abs_rect.top - my_box_2.abs_rect.top),
			(my_box_1.abs_rect.left - my_box_2.abs_rect.left))) )
		print(my_box_2.mask.overlap(my_box_1.mask,((my_box_2.abs_rect.top - my_box_1.abs_rect.top),
			(my_box_2.abs_rect.left - my_box_1.abs_rect.left))) )

		print("-----------\n")

def main_window():
	pygame.mixer.music.stop()	
	pen_obj = pygame.font.SysFont("arial",70,True,True)
	game_head = pen_obj.render("BALL * HIT * BLOCK",True,WHITE)
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

PLAYER_MARGIN_FROM_BOTTOM = 15
USE_RANDOM_BACKGROUND = False
SHOW_ARROW_ALWAYS = False
SHOOTING_HAS_NO_LIMIT = False
main_window()

#How to play
# Use Arrow Left amd right to move
# press key a to shoot_ball when on the player
# press h to hold ball to player when the ball its the player
# Use Arrow Up and Down to give the ball a direction 
# press p to pause