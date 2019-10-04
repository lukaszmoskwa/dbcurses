import curses

class BaseTabDialog:
    def __init__(self, **options):
        self.main_window = options.get('main_window')
        self.maxy, self.maxx = self.main_window.height, self.main_window.width
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

class MainTabDialog(BaseTabDialog):
    top = 0
    current = 0

    def showMainTab(self, table_list):
        curses.curs_set(0)
        self.bottom = len(table_list)
        self._maxlen = self.max_len_in_list(table_list)
        
        self.draw()

        while True:
            try:
                self.win.addstr(1,2, "Tables:" , curses.A_UNDERLINE | curses.A_REVERSE)
                for (i, x) in enumerate(table_list[self.top:self.top + self.max_lines]):
                    self.win.addstr(i+3, 2, "[" + x + "] ",
                                    curses.color_pair(1 if self.current == i else 2) | curses.A_NORMAL)
            except:
                pass
            key = self.win.getch()
            if key == 27 or key == curses.KEY_RESIZE:
                self.win.clear()
                self.main_window.resize()
                self.win.refresh()
                break
            elif key == 10:
                self.win.clear()
                self.main_window.resize()
                self.main_window.display_table(table_list[self.current])
                break
            elif key in [258, 259, ord('j'), ord('k')]:
                self.handle_input(key)
            else:
                self.win.clear()
                break

    def draw(self):
        self.win = curses.newwin(self.maxy - 2, self.maxx - (self.maxx - self._maxlen - 6 ), 1, 1)
        self.win.bkgd(' ', curses.color_pair(
            2) | curses.A_REVERSE)

        self.max_lines = self.maxy - 7
        self.win.box()
        self.win.keypad(1)

    def max_len_in_list(self, lst):
        _max = 0
        for el in lst:
            _max = len(el) if len(el) > _max else _max
        return _max

    def scroll(self, direction):
        next_line = self.current + direction
        if (((direction == -1) and (self.top > 0 and self.current == 0)) or
        ((direction == 1) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom))):
            self.top += direction
        elif (((direction == -1) and (self.top > 0 or self.current > 0)) or
              ((direction == 1) and (next_line < self.max_lines) and (self.top + next_line < self.bottom))):
            self.current = next_line
        self.draw()


            
    def handle_input(self, key):
        if key == 259 or key == ord('k'):
            self.scroll(-1)
        elif key == 258 or key == ord('j'):
            self.scroll(+1)


def showMainTabDialog(table_list, **options):
    return MainTabDialog(**options).showMainTab(table_list)
