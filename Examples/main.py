import sys
  
# setting path
sys.path.append('../')

import menu
import curses

def greet(stdscr):
	stdscr.clear()
	# get screen height and width
	screen_height, screen_width = stdscr.getmaxyx()
	#calculate x, y position
	x = int(screen_width * 0.2)
	y = int(screen_height / 2)

	stdscr.addstr(y, x, 'Press any key to exit')
	stdscr.refresh()
	stdscr.getch()

# menu items
main_menu_items = ['Start', 'Choose']
start_items = ['Programs', 'Files']
start_programs_items = ['CAD', 'VSCode', 'Sublime']
choose_items = ['Apples', 'Pears', 'Bananas']

# menu objects
Start_Programs_menu = menu.SubMenu(start_programs_items, callback_funcs = [greet, greet, greet])
Start_menu = menu.SubMenu(start_items, submenus=[Start_Programs_menu, None], callback_funcs = [None, greet])
Choose_menu = menu.SubMenu(choose_items, callback_funcs = [greet, greet, greet])
Main_menu = menu.Menu(main_menu_items, submenus=[Start_menu, Choose_menu])
curses.wrapper(Main_menu.main)
