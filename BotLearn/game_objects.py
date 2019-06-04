from help_classes.base_game import GameObject
from arcade.draw_commands import load_texture, draw_texture_rectangle
from help_classes.content_manager import LoadSprite

class MatrixBasedGameObject(GameObject):
    
    def __init__(self, pos_x, pos_y, mat_rows, mat_cols, mat_width, mat_height):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mat_rows = mat_rows
        self.mat_cols = mat_cols
        self.mat_width = mat_width
        self.mat_height = mat_height

    @property
    def pos_x(self):
        return self._pos_x
    
    @pos_x.setter
    def pos_x(self, value):
        if value >= 0 and value < self.mat_cols:
            self._pos_x = value

    @property
    def pos_y(self):
        return self._pos_y
    
    @pos_y.setter
    def pos_x(self, value):
        if value >= 0 and value < self.mat_rows:
            self._pos_y = value

class TextureMatrixObject(MatrixBasedGameObject):
    
    def __init__(self, pos_x, pos_y, mat_rows, mat_cols, mat_width, mat_height, url):
        super().__init__(pos_x, pos_y, mat_rows, mat_cols, mat_width, mat_height)

        self.sprite = LoadSprite(url)
        self.sprite._set_center_x((self.pos_x+0.5)*self.mat_width / self.mat_cols)
        self.sprite._set_center_y((self.pos_y+0.5)*self.mat_height / self.mat_rows)
        
        self.sprite._set_width(self.mat_width / self.mat_cols)
        self.sprite._set_height(self.mat_height / self.mat_rows)

    def on_draw(self):
        self.sprite.draw()

class PlayerMatrixObject(TextureMatrixObject):
    pass
        #draw_texture_rectangle((self.pos_x + 0.5)*self.mat_width / self.mat_rows ,\
        #                       (self.pos_y + 0.5)*self.mat_height / self.mat_cols,\
        #                        self.mat_width / self.mat_rows,\
        #                        self.mat_height / self.mat_cols,\
        #                       self.texture)

#class TextureMatrixObject(MatrixBasedGameObject):
    
#    def __init__(self, pos_x, pos_y, mat_rows, mat_cols, mat_width, mat_height, url):
#        super().__init__(pos_x, pos_y, mat_rows, mat_cols, mat_width, mat_height)

#    def on_draw(self):

#        draw_texture_rectangle((self.pos_x + 0.5)*self.mat_width / self.mat_rows ,\
#                               (self.pos_y + 0.5)*self.mat_height / self.mat_cols,\
#                                self.mat_width / self.mat_rows,\
#                                self.mat_height / self.mat_cols,\
#                               self.texture)

