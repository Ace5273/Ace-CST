from help_classes.base_game import GameObject
from arcade.draw_commands import draw_line
from arcade.color import BLACK, GREEN, RED, WHITE
from game_objects import SnakePlayer
from arcade import key
from snake_bot import BotSnake

class Environment(GameObject):
    def __init__(self, width, height, cols, rows):
        super().__init__()
        self.lines = []
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.build_line_array(width, height, cols, rows)
        self.game_board = []
        # SnakePlayer(self)
        BotSnake(self)
    

    def build_line_array(self, width, height, cols, rows):

        for i in range(cols + 1):
            self.lines.append([i*(width-1)/cols,
                                1,
                                i*(width-1)/cols,
                                height])

        for j in range(rows + 1):
            self.lines.append([1,
                                j*(height-1)/rows,
                                width,
                                j*(height-1)/rows])
    
    def on_draw(self):
        for line in self.lines:
            draw_line(line[0], line[1], line[2], line[3], WHITE, 5)
