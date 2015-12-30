import sys, copy, pygame
import numpy.random as rand

class Board():
	def __init__(self, side, UI = True):
		self._end_game = False
		#pygame.mixer.pre_init(44100, -16, 1, 512)
		#pygame.mixer.init(44100, -16, 1, 512)
		pygame.init()
		self._font = pygame.font.SysFont("arial", 40, bold=True)
		self._move_sound = pygame.mixer.Sound("./sounds/move.wav")
		self._win_sound = pygame.mixer.Sound("./sounds/win.wav")
		self._win_sound.set_volume(0.3)
		self._lose_sound = pygame.mixer.Sound("./sounds/lose.wav")
		self._lose_sound.set_volume(0.4)
		self._tie_sound = pygame.mixer.Sound("./sounds/tie.wav")

		self._side = side
		self._size = self._side, self._side
		self._screen = pygame.display.set_mode(self._size)

		self._win_screen = pygame.Surface(self._size)
		self._win_screen.fill((128, 128, 128))
		self._win_screen.set_alpha(170)
		self._play_again = self._font.render(" Play Again ", 1, (0,0,0), (192,192,192))
		self._play_again_rect = self._play_again.get_rect()
		self._play_again_rect.centerx = 300
		self._play_again_rect.centery = 250
		self._quit = self._font.render(" Quit ", 1, (0,0,0), (192,192,192))
		self._quit_rect = self._quit.get_rect()
		self._quit_rect.centerx = 300
		self._quit_rect.centery = 350

		self._scale = side/3
		pos1, pos2 = self._scale, 2*self._scale
		self._positions = [(0,0), (pos1,0), (pos2,0),
						(0,pos1), (pos1,pos1), (pos2,pos1),
						(0,pos2), (pos1,pos2), (pos2,pos2)]
		self._win_cons=[[(0,0),(0,pos1),(0,pos2)],
			[(pos1,0),(pos1,pos1),(pos1,pos2)],
			[(pos2,0),(pos2,pos1),(pos2,pos2)],
			[(0,0),(pos1,0),(pos2,0)],
			[(0,pos1),(pos1,pos1),(pos2,pos1)],
			[(0,pos2),(pos1,pos2),(pos2,pos2)],
			[(0,0),(pos1,pos1),(pos2,pos2)],
			[(pos2,0),(pos1,pos1),(0,pos2)]]
		self._win_type = "tie"
		self._end_decision = "undecided"

		self._cell = pygame.image.load("./images/cell.bmp").convert()
		self._cross = pygame.image.load("./images/cross.bmp").convert()
		self._circle = pygame.image.load("./images/circle.bmp").convert()
		self._red_cross = pygame.image.load("./images/red_cross.bmp").convert()
		self._red_circle = pygame.image.load("./images/red_circle.bmp").convert()
		for pos in self._positions:
			self._screen.blit(self._cell, pos)
		if UI:
			pygame.display.flip()
		self._UI = UI

		self._occupied = []
		self._circles = []
		self._crosses = []

	def get_pos(self, pos_no):
		if pos_no < 1 or pos_no > 9:
			raise Exception("Must be an integer between 1 and 9.")
		return self._positions[pos_no - 1]

	def get_pos_no(self, pos):
		return self._positions.index(pos) + 1

	def add_move(self, pos_no, player_type):
		pos = self.get_pos(pos_no)
		self._occupied.append(pos)
		if player_type == "x":
			if self._UI: self._move_sound.play()
			self._crosses.append(pos)
		elif player_type == "o":
			self._circles.append(pos)

	def check_win_con(self):
		for win_con in self._win_cons:
			if set(win_con).issubset(set(self._circles)):
				self._win_type = "o"
				self._win_pos = win_con
				self._end_game = True
				self._win_screen.fill((204, 0, 0))
			if set(win_con).issubset(set(self._crosses)):
				self._win_type = "x"
				self._win_pos = win_con
				self._end_game = True
				self._win_screen.fill((0, 204, 0))

		if len(self._occupied) == 9:
			self._end_game = True
			

	def draw_board_state(self):
		for circ_pos in self._circles:
			self._screen.blit(self._circle, circ_pos)
		for cross_pos in self._crosses:
			self._screen.blit(self._cross, cross_pos)

		self.check_win_con()
		if self._end_game:
			if self._win_type == "x":
				for pos in self._win_pos:
					self._screen.blit(self._red_cross, pos)
					self._win_sound.play()
			elif self._win_type == "o":
				for pos in self._win_pos:
					self._screen.blit(self._red_circle, pos)
					self._lose_sound.play()
			elif self._win_type == "tie":
				self._tie_sound.play()
			self._screen.blit(self._win_screen, (0,0))
			self._screen.blit(self._play_again, self._play_again_rect)
			self._screen.blit(self._quit, self._quit_rect)

		pygame.display.flip()

	def is_occupied(self, pos_no):
		for oc_pos in self._occupied:
			if self.get_pos_no(oc_pos) == pos_no:
				return True
		return False

	def get_mouse_pos(self, mouse_pos):
		for pos in self._positions:
			if (pos[0] <= mouse_pos[0] <= pos[0] + self._scale and
				pos[1] <= mouse_pos[1] <= pos[1] + self._scale):
				pos_clicked = pos
				pos_clicked_no = self.get_pos_no(pos_clicked)
		if not self.is_occupied(pos_clicked_no):
			return pos_clicked_no
		else:
			return False

	def get_rand_pos(self):
		pos = rand.uniform(0, self._side, 2)
		pos_no = self.get_mouse_pos(pos)
		loop = True
		while loop:
			randomize = False
			if self.is_occupied(pos_no) or not pos_no:
				randomize = True
			if randomize:
				pos = rand.uniform(0, self._side, 2)
				pos_no = self.get_mouse_pos(pos)
			else:
				loop = False
		return pos_no

	def find_best_move(self, occ=[], circ=[], cross=[], 
						p_type="o", root=True):
		if root:
			occ_pos = copy.deepcopy(self._occupied)
			circles = copy.deepcopy(self._circles)
			crosses = copy.deepcopy(self._crosses)
		else:
			occ_pos = copy.deepcopy(occ)
			circles = copy.deepcopy(circ)
			crosses = copy.deepcopy(cross)
		possible_pos = list(set(self._positions) - set(occ_pos))
		if len(possible_pos) == 0:
			return "terminates"
		for pos in possible_pos:
			if root:
				occ_pos = copy.deepcopy(self._occupied)
				circles = copy.deepcopy(self._circles)
				crosses = copy.deepcopy(self._crosses)
			else:
				occ_pos = copy.deepcopy(occ)
				circles = copy.deepcopy(circ)
				crosses = copy.deepcopy(cross)
			test_board = Board(600, False)
			test_board._occupied = occ_pos
			test_board._crosses = crosses
			test_board._circles = circles
			pos_no = test_board.get_pos_no(pos)

			if p_type == "o":
				occ_pos.append(pos)
				circles.append(pos)
				test_board.add_move(pos_no, p_type)
				test_board.check_win_con()
				if test_board._end_game:
					print "o wins or tie"
					print occ_pos
					return occ_pos[len(self._occupied)]
				else:
					iterate = self.find_best_move(occ_pos, circles, 
											crosses, "x", False)
					if iterate == "terminates":
						continue
					elif iterate == "x wins":
						break
					else:
						return iterate

			if p_type == "x":
				occ_pos.append(pos)
				crosses.append(pos)
				test_board.add_move(pos_no, p_type)
				test_board.check_win_con()
				if (test_board._end_game and
					test_board._win_type == "x"):
					print "x wins"
					return "x wins"
				if (test_board._end_game and
					test_board._win_type == "tie"):
					print "tie"
					print occ_pos
					return occ_pos[len(self._occupied)]
				else:
					iterate =  self.find_best_move(occ_pos, circles,  
											crosses, "o", False)
					if iterate == "terminates":
						continue
					else:
						return iterate
		return "terminates"

	def get_game_tree(self, occ=[], circ=[], cross=[], 
						p_type="o", root=True):
		if root:
			occ_pos = copy.deepcopy(self._occupied)
			circles = copy.deepcopy(self._circles)
			crosses = copy.deepcopy(self._crosses)
		else:
			occ_pos = copy.deepcopy(occ)
			circles = copy.deepcopy(circ)
			crosses = copy.deepcopy(cross)
		possible_pos = list(set(self._positions) - set(occ_pos))
		if len(possible_pos) == 0:
			self._temp.append((occ_pos, circles, crosses))
		for win_con in self._win_cons:
			if set(win_con).issubset(set(circles)):
				self._temp.append((occ_pos, circles, crosses))
			if set(win_con).issubset(set(crosses)):
				self._temp.append((occ_pos, circles, crosses))
		for pos in possible_pos:
			if root:
				print "done"
				occ_pos = copy.deepcopy(self._occupied)
				circles = copy.deepcopy(self._circles)
				crosses = copy.deepcopy(self._crosses)
			else:
				occ_pos = copy.deepcopy(occ)
				circles = copy.deepcopy(circ)
				crosses = copy.deepcopy(cross)

			if p_type == "o":
				occ_pos.append(pos)
				circles.append(pos)
				self.get_game_tree(occ_pos, circles,  
									crosses, "x", False)

			if p_type == "x":
				occ_pos.append(pos)
				crosses.append(pos)
				self.get_game_tree(occ_pos, circles,  
									crosses, "o", False)
	def get_best_play(self):
		self._temp = []
		accepted, tiemakers = [], []
		index = len(self._occupied)
		self.get_game_tree()
		for tree, o_tree, x_tree in self._temp:
			if ((tree[index], tree[index+1]) not in accepted or 
				(tree[index], tree[index+1]) not in tiemakers):
				test_board = Board(600, False)
				test_board._occupied = tree
				test_board._crosses = x_tree
				test_board._circles = o_tree
				test_board.check_win_con()
				if test_board._win_type == "o":
					print "o"
					accepted.append((tree[index], tree[index+1]))
				if test_board._win_type == "tie":
					print "tie"
					tiemakers.append((tree[index], tree[index+1]))
		accepted = list(set(accepted))
		tiemakers = list(set(tiemakers))

		print accepted, tiemakers
		if len(accepted) == 9 - index:
			return accepted[0][0]
		else:
			return tiemakers[0][0]

	def get_ok_play(self):
		occ_pos = copy.deepcopy(self._occupied)
		circles = copy.deepcopy(self._circles)
		crosses = copy.deepcopy(self._crosses)

		possible_pos = list(set(self._positions) - set(occ_pos))
		for pos in possible_pos:
			occ_pos = copy.deepcopy(self._occupied)
			circles = copy.deepcopy(self._circles)
			crosses = copy.deepcopy(self._crosses)

			
				
			occ_pos.append(pos)
			circles.append(pos)
			test_board = Board(600, False)
			test_board._occupied = occ_pos
			test_board._crosses = crosses
			test_board._circles = circles
			test_board.check_win_con()
			if (test_board._end_game and
				test_board._win_type == "o"):
				return circles[-1]

		for pos in possible_pos:
			occ_pos = copy.deepcopy(self._occupied)
			circles = copy.deepcopy(self._circles)
			crosses = copy.deepcopy(self._crosses)

			occ_pos.append(pos)
			circles.append(pos)

			possible_pos_x = list(set(self._positions) - set(occ_pos))
			for pos_x in possible_pos_x:
				occ_pos_x = copy.deepcopy(occ_pos)
				crosses_x = copy.deepcopy(crosses)

				occ_pos_x.append(pos_x)
				crosses_x.append(pos_x)
				test_board = Board(600, False)
				test_board._occupied = occ_pos_x
				test_board._crosses = crosses_x
				test_board._circles = circles
				test_board.check_win_con()

				if (test_board._end_game and
					test_board._win_type == "x"):
					return crosses_x[-1]

				if (test_board._end_game and
					test_board._win_type == "tie"):
					return circles[-1]
		if (self._crosses[0] == (200, 200) and 
				len(self._crosses) == 1):
			return (0,0)
		if (self._crosses[0][0] != 200 and 
			self._crosses[0][1] != 200 and
				len(self._crosses) == 1):
			return (200,200)
		return self.get_pos(self.get_rand_pos())



def tictactoe_game():
	tictac = Board(600)
	while not tictac._end_game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

			#if pygame.mouse.get_pressed()[0] == 0:
			if event.type == pygame.MOUSEBUTTONUP:	
				mouse_click = pygame.mouse.get_pos()
				mouse_pos = tictac.get_mouse_pos(mouse_click)
				if mouse_pos:
					tictac.add_move(mouse_pos, "x")
					tictac.draw_board_state()
					if not tictac._end_game:
						next_pos = tictac.get_ok_play()
						next_pos_no = tictac.get_pos_no(next_pos)
						tictac.add_move(next_pos_no, "o")
						tictac.draw_board_state()
	while tictac._end_decision == "undecided":
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_click = pygame.mouse.get_pos()
				if tictac._play_again_rect.collidepoint(mouse_click):
					tictac._end_decision = False
				if tictac._quit_rect.collidepoint(mouse_click):
					tictac._end_decision = True
	return tictac._end_decision

def tictactoe():
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.mixer.init(44100, -16, 1, 512)
	bgmusic = pygame.mixer.Sound("./sounds/bgmusic.wav")		
	bgmusic.play(-1)
	while 1:
		if tictactoe_game():
			sys.exit()

tictactoe()

