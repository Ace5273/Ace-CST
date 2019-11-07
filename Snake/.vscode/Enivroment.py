from help_classes.base_game import GameObject

class Enviroment(GameObject):
    def __init__(self, width, height, col_num, row_num):
        super().__init__()  
        self.lines = []
        build_line_array(width, height, col_num, row_num)
        self.game_board = []
    

    def build_line_array(self, width, height, col_num, row_num):

        for i in range(col_num + 1):
            self.lines.append([i*(width-1)/col_num,
                                1,
                                i*(width-1)/col_num,
                                height])

        for j in range(row_num + 1):
            self.lines.append([1,
                                j*(height-1)/row_num,
                                width,
                                j*(height-1)/row_num])
    
    def on_draw(self):
        for line in self.lines:
            draw_line(line[0], line[1], line[2], line[3], BLACK, 5)
