from help_classes.base_game import GameObject
from help_classes.vector import Vector, Point
from arcade.draw_commands import draw_circle_filled
from arcade.color import WHITE
from player import Player
from event_hook import EventHook


class Ball(GameObject):

    def __init__(self, player: Player, screen_width, screen_height):
        super().__init__()
        self.radius = 10
        self.color  = WHITE
        self.position = Point(400, 400)
        self.velocity: Vector = Vector.ONE() * 10
        self.velocity.angle = 45
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.lost = EventHook()
    
    def flip_x(self):
        self.velocity.end_point.x *= -1 

    def flip_y(self):
        self.velocity.end_point.y *= -1  
    
    def on_draw(self):
        draw_circle_filled(self.position.x, self.position.y, self.radius, self.color)
    
    def on_update(self, delta_time):
        
        if self.position.y - self.radius <= self.player.position.y + self.player.height / 2 and \
            self.position.y + self.radius >= self.player.position.y + self.player.height / 2 and \
            self.position.x >= self.player.position.x - self.player.width / 2 and \
            self.position.x <= self.player.position.x + self.player.width / 2 :

            x_diff = (self.player.position.x + self.player.width / 2) - self.position.x
            self.velocity.angle = x_diff * 178 / self.player.width + 1
        
        if self.position.x - self.radius <= 0 or \
            self.position.x + self.radius >= self.screen_width:

            self.flip_x()
        
        if self.position.y + self.radius >= self.screen_height:
            self.flip_y()
        
        if self.position.y - self.radius <= 0:
            self.lost()

        self.position += self.velocity.end_point