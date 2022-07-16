import curses

class SubMenu:
	def __init__(self, menu_items, submenus = None, callback_funcs = None):
		"""Initializes the SubMenu object.

		Args:
			menu_items (list of strings): ['Start', 'Choose', ... , 'Exit'] 'Exit' is added automatically
			submenus (list of SubMenu objects, optional): [Start_menu, Choose_menu, ...]. Lenght can't be greater than menu_items.
							 Defaults to None.
			callback_funcs (list of functions, optional): functions which will be called when the menu item is selected. 
							Length should be menu_items+1, extra isfor exit callback. Must accept 1 argument stdscr. Defaults to None.
		"""
		# set menu items strings and append 'Exit' option
		self.menu_items = menu_items
		self.menu_items.append('Exit')

		# default parent is None, if SubMenu has parent the variable will be set by the parent
		self.parent = None

		# if submenus are not specified, set all submenus to None
		if submenus == None:
			self.submenus = [None for i in menu_items]
		else:
			self.submenus = submenus
			# set submenus parent
			for menu in self.submenus:
				if menu != None:
					menu.parent = self

		# if callback_funcs are not specified, set all callback_funcs to None
		if callback_funcs == None:
			self.callback_funcs = [None for i in menu_items]
			self.callback_funcs.append(None)
		else:
			self.callback_funcs = callback_funcs

	def print(self, current_selection, stdscr):
		"""Prints the menu items to the screen

		Args:
			current_selection (unsigned int): number of the item selected
			stdscr (curses screen object): _description_
		"""		
		stdscr.clear()
		# get screen height and width
		self.screen_height, self.screen_width = stdscr.getmaxyx()
		# calculate x, y position
		x = int(self.screen_width * 0.2)
		y = int((self.screen_height - len(self.menu_items)) / 2)

		for row, item in enumerate(self.menu_items):
			if row == current_selection:
				stdscr.addstr(y + row, x, f'[{row}] {item}', curses.color_pair(1))
			else:
				stdscr.addstr(y + row, x, f'[{row}] {item}')
		stdscr.refresh()

class Menu(SubMenu):
	def __init__(self, main_menu_items, submenus = None, callback_funcs = None):
		SubMenu.__init__(self, main_menu_items, submenus, callback_funcs)

	def main(self, stdscr):
		"""Main loop of menu program, waiting for user input.

		Args:
			stdscr (curses screen object): provided by curses.wrapper function
		"""		
		# turn off cursor blinking
		curses.curs_set(0)

		# color scheme for selected row
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

		# set screen object as class property
		self.stdscr = stdscr

		# selected item
		current_selection = 0

		# menu depth
		current_menu = self

		current_menu.print(current_selection, self.stdscr)

		while True:
			key = self.stdscr.getch()

			# increase and decrease selection
			if key == curses.KEY_UP and current_selection > 0:
				current_selection -= 1
			elif key == curses.KEY_DOWN and current_selection < len(current_menu.menu_items) - 1:
				current_selection += 1
			# user made a selection
			elif key == curses.KEY_ENTER or key in [10, 13]:
				# if user selected last row (Exit), navigate to parent if it has one, exit otherwise
				if current_selection == len(current_menu.menu_items) - 1:
					if current_menu.parent == None:
						break
					else:
						current_menu = current_menu.parent
						current_selection = 0
				else:
					# choose relevant submenu
					if current_menu.submenus[current_selection] == None:
						current_menu.callback_funcs[current_selection](self.stdscr)
						# continue in the menu after callback returns
					else:
						current_menu = current_menu.submenus[current_selection]
						current_selection = 0

			current_menu.print(current_selection, self.stdscr)
