import curses


class DataWindow:

    col_width = 20
    col_list = []
    row_list = []
    table_name = ''
    max_elem = 5

    def __init__(self, main_window):
        self.main_window = main_window
        self.height, self.width = main_window.win.getmaxyx()
        self.win = main_window.win.subwin(
            self.height - 2, self.width - 2, 1, 1)
        self.win.bkgd(' ', curses.color_pair(1))
        self.win.box()
        self.top = 0
        self.max_lines = self.height - 7
        self.current = 0
        self.bottom = 0
        self.left = 0
        self.max_cols = (self.width - 2) // self.col_width

    def redraw(self):
        self.height, self.width = self.main_window.height, self.main_window.width
        self.win = self.main_window.win.subwin(
            self.height - 2, self.width - 2, 1, 1)
        self.max_lines = self.height - 7
        self.max_cols = (self.width - 2) // self.col_width
        self.win.clear()
        self.win.bkgd(' ', curses.color_pair(1))
        self.win.box()
        self.set_title(self.table_name)
        self.add_columns(self.col_list)
        self.add_rows(self.row_list)

    def set_title(self, string):
        self.table_name = string
        self.win.addstr(0, 4, ' Table: ' + string + ' ',
                        curses.color_pair(2) | curses.A_UNDERLINE)

    def swipe(self, direction):
        if len(self.col_list) <= self.max_cols - 1:
            return
        self.left = max(0, min(self.left + direction,
                               len(self.col_list) - self.max_cols))
        self.redraw()

    def scroll(self, direction):
        next_line = self.current + direction
        if (((direction == -1) and (self.top > 0 and self.current == 0)) or
        ((direction == 1) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom))):
            self.top += direction
        elif (((direction == -1) and (self.top > 0 or self.current > 0)) or
              ((direction == 1) and (next_line < self.max_lines) and (self.top + next_line < self.bottom))):
            self.current = next_line
        self.redraw()

    def add_columns(self, col_list):
        self.col_list = col_list
        self.max_cols = min(len(col_list), self.max_cols)
        for (index, col) in enumerate(col_list[self.left:self.left + self.max_cols]):
            is_primary = 'PRI' in col
            width_pos = 2 + index * self.col_width
            self.win.addstr(1, width_pos, self.ellipsize(col[0]),
                            curses.color_pair(1) | curses.A_BOLD |
                            (curses.A_UNDERLINE if is_primary else curses.A_NORMAL))

    def add_rows(self, row_list):
        self.row_list = row_list
        self.bottom = len(row_list)
        self.page = self.bottom // self.max_lines
        for (row_idx, row) in enumerate(row_list[self.top:self.top + self.max_lines]):
            for (i, col_el) in enumerate(row[self.left:self.left + self.max_cols]):
                is_selected = 2 if row_idx == self.current else 1
                width_pos = 2 + i * self.col_width
                self.win.addstr(row_idx + 2, 2 + i*self.col_width, ' ' * self.col_width,
                                curses.color_pair(is_selected))
                self.win.addstr(row_idx + 2, width_pos,
                                self.ellipsize(row[self.left + i]),
                                curses.color_pair(is_selected))
        self.win.refresh()

    def ellipsize(self, string):
        string = str(string)
        if len(string) > self.col_width:
            return string[:self.col_width - 2] + '..'
        else:
            return string

    def column_resize(self, value):
        self.col_width = max(10, min(self.col_width + value, 40))
