import sys, copy, random 
import pygame

class Board():
	def __init__(self, side, UI = True, level = "undetermined"):
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
		self._play_again_rect.centery = 200
		self._diff = self._font.render(" Choose Difficulty ", 1, (0,0,0), (192,192,192))
		self._diff_rect = self._diff.get_rect()
		self._diff_rect.centerx = 300
		self._diff_rect.centery = 300
		self._quit = self._font.render(" Quit ", 1, (0,0,0), (192,192,192))
		self._quit_rect = self._quit.get_rect()
		self._quit_rect.centerx = 300
		self._quit_rect.centery = 400

		self._level = level
		if self._level == "undetermined" and UI:
			self._choose_diff = pygame.Surface(self._size)
			self._choose_diff.fill((128, 128, 128))
			self._choose_diff.set_alpha(170)
			self._easy = self._font.render(" Easy ", 1, (0,0,0), (192,192,192))
			self._easy_rect = self._easy.get_rect()
			self._easy_rect.centerx = 300
			self._easy_rect.centery = 120
			self._intermediate = self._font.render(" Intermediate ", 1, (0,0,0), (192,192,192))
			self._intermediate_rect = self._intermediate.get_rect()
			self._intermediate_rect.centerx = 300
			self._intermediate_rect.centery = 240
			self._advanced = self._font.render(" Advanced ", 1, (0,0,0), (192,192,192))
			self._advanced_rect = self._advanced.get_rect()
			self._advanced_rect.centerx = 300
			self._advanced_rect.centery = 360
			self._expert = self._font.render(" Expert ", 1, (0,0,0), (192,192,192))
			self._expert_rect = self._expert.get_rect()
			self._expert_rect.centerx = 300
			self._expert_rect.centery = 480

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
		if level == "undetermined" and UI:
			self._screen.blit(self._choose_diff, (0,0))
			self._screen.blit(self._easy, self._easy_rect)
			self._screen.blit(self._intermediate, self._intermediate_rect)
			self._screen.blit(self._advanced, self._advanced_rect)
			self._screen.blit(self._expert, self._expert_rect)
		if UI:
			pygame.display.flip()
		self._UI = UI

		self._occupied = []
		self._circles = []
		self._crosses = []
	def draw_empty(self):
		for pos in self._positions:
			self._screen.blit(self._cell, pos)
		pygame.display.flip()

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
			self._screen.blit(self._diff, self._diff_rect)
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

	def get_rand_play(self):
		pos = (random.uniform(0, self._side), random.uniform(0, self._side))
		pos_no = self.get_mouse_pos(pos)
		loop = True
		while loop:
			randomize = False
			if self.is_occupied(pos_no) or not pos_no:
				randomize = True
			if randomize:
				pos = (random.uniform(0, self._side), random.uniform(0, self._side)))
				pos_no = self.get_mouse_pos(pos)
			else:
				loop = False
		return pos_no
		
	def get_good_play(self):
		occ_pos = copy.deepcopy(self._occupied)
		circles = copy.deepcopy(self._circles)
		crosses = copy.deepcopy(self._crosses)

		if self._level == "advanced" or self._level == "expert":
			if len(self._crosses) == 1:
				if self._crosses[0] == (200, 200):
					return (0,0)
				else:
					return (200,200)

		


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

		if self._level == "expert":
			occ_edges = []
			corners = [1,3,7,9]
			edges = [2,4,6,8]
			for edge in edges:
						if self.is_occupied(edge):
							occ_edges.append(edge)
			if len(self._crosses) == 2:
				if (self._crosses[0] != (200,200) and 
						len(occ_edges) != 0):
					if len(occ_edges) == 0:
						return self.get_pos(edge[0])
					if len(occ_edges) == 1:
						if (edges[0] in occ_edges 
							or edges[3] in occ_edges):
							return self.get_pos(edges[1])
						else:
							return self.get_pos(edges[0])
					if len(occ_edges) == 2:
						if ((edges[0] in occ_edges and
							edges[3] in occ_edges) or
							(edges[1] in occ_edges and
							edges[2] in occ_edges)):
							return self.get_pos(1)
						else:
							if edges[0] in occ_edges:
								return self.get_pos(1)
							elif edges[3] in occ_edges:
								return self.get_pos(9)

				else:
					free_edges = list(set(edges) - set(occ_edges))
					return self.get_pos(free_edges[0])
			if (len(self._crosses) == 3 and 
				len(occ_edges) == 3 and
				self.get_pos_no(self._crosses[0]) in corners):
				for corner in corners:
						if self.is_occupied(corner):
							occ_corner = corner
				if occ_corner == corners[0]:
					return self.get_pos(corners[3])
				if occ_corner == corners[3]:
					return self.get_pos(corners[0])
				if occ_corner == corners[1]:
					return self.get_pos(corners[2])
				if occ_corner == corners[2]:
					return self.get_pos(corners[1])


		return self.get_pos(self.get_rand_play())

	def get_play(self):
		if self._level == "easy":
			return self.get_pos(self.get_rand_play())
		if (self._level == "intermediate" or
			self._level == "advanced" or
			self._level == "expert"):
			return self.get_good_play()



def tictactoe_game(level):
	level = level
	choose_diff = False
	tictac = Board(600, True, level)
	while level == "undetermined":
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_click = pygame.mouse.get_pos()
				if tictac._easy_rect.collidepoint(mouse_click):
					tictac._level = "easy"
					level = "easy"
					tictac.draw_empty()
				if tictac._intermediate_rect.collidepoint(mouse_click):
					tictac._level = "intermediate"
					level = "intermediate"
					tictac.draw_empty()
				if tictac._advanced_rect.collidepoint(mouse_click):
					tictac._level = "advanced"
					level = "advanced"
					tictac.draw_empty()
				if tictac._expert_rect.collidepoint(mouse_click):
					tictac._level = "expert"
					level = "expert"
					tictac.draw_empty()


	while not tictac._end_game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

			if event.type == pygame.MOUSEBUTTONUP:	
				mouse_click = pygame.mouse.get_pos()
				mouse_pos = tictac.get_mouse_pos(mouse_click)
				if mouse_pos:
					tictac.add_move(mouse_pos, "x")
					tictac.draw_board_state()
					if not tictac._end_game:
						next_pos = tictac.get_play()
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
				if tictac._diff_rect.collidepoint(mouse_click):
					tictac._end_decision = False
					choose_diff = True
	return tictac._end_decision, tictac._level, choose_diff

def tictactoe():
	level = "undetermined"
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.mixer.init(44100, -16, 1, 512)
	bgmusic = pygame.mixer.Sound("./sounds/bgmusic.wav")		
	bgmusic.play(-1)
	while 1:
		exit, lvl, diff = tictactoe_game(level)
		level = lvl
		if diff:
			level = "undetermined"
		if exit:
			sys.exit()

tictactoe()

