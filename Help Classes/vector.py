import math
from arcade import Color, draw_point, draw_line 
from arcade.color import BLACK

class Point():
    """
    Represent a class of a point in 2d space
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Define a point by either it's coordinates(x, y) or
        by another point

        Args:
            x: the x coordinate
            y: the y coordinate
        """
        
        self.list = [x, y]

    @property
    def x(self):
        """
        The x coordinate
        """

        return self.list[0]

    @x.setter
    def x(self, value) -> float:
        self.list[0] = value

    @property
    def y(self):
        """
        The y coordinate
        """
        return self.list[1]

    @y.setter
    def y(self, value):
        self.list[1] = value

    def get_list(self):
        """
        Get the point as a list

        Return:
            List[x, y]
        """
        return self.list

    def distance(self, point):
        """
        Get the distance between this point and another point

        Args:
            point: The other point

        Return:
            The distance - float
        """
        return math.sqrt((point.x-self.x)**2+(point.y-self.y)**2)

    def angle(self, point):
        """
        Get the angle of this point with another point

        Args:
            point: The other point

        Return:
            The angle in *degrees* - float
        """

        return math.fmod(math.degrees(math.atan2(point.y - self.y, point.x - self.x)) + 360, 360)

    @staticmethod
    def duplicate(point):
        """
        Create a duplicate from another point

        Args:
            point: The other point

        Return:
            The duplicated point - Point
        """
        return Point(point.x, point.y)

    #region Arithemetic Functions

    def add_point(self, point):
        """
        Add an other point's coordinates to this point coordinates

        Args:
            point: The other point

        Return:
            None
        """

        self.x += point.x
        self.y += point.y

    def add_number(self, number):
        """
        Add a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.add_point(Point(number, number))

    def sub_point(self, point):
        """
        Subtract an other point's coordinates to this point coordinates

        Args:
            point: The other point

        Return:
            None
        """

        self.x -= point.x
        self.y -= point.y

    def sub_number(self, number):
        """
        Subtruct a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """

        self.sub_point(Point(number, number))

    def mul_point(self, point):
        """
        Multiply an other point's coordinates to this point coordinates

        Args:
            point: The other point

        Return:
            None
        """

        self.x *= point.x
        self.y *= point.y

    def mul_number(self, number):
        """
        Add a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.mul_point(Point(number, number))

    def div_point(self, point):
        """
        Divide an other point's coordinates to this point coordinates

        Args:
            point: The other point

        Return:
            None
        """

        self.x /= point.x
        self.y /= point.y

    def div_number(self, number):
        """
        Divide a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.mul_point(Point(number, number))

    # endregion
    
    # region Operators

    def __do__(self, action, other):
        new_point = Point.duplicate(self)
        obj_lst = set(['Point'])
        type_lst = set(['float', 'int'])

        if other.__class__.__name__  in obj_lst:
            getattr(new_point, action + '_' + other.__class__.__name__ .lower())(other)
            return new_point

        if other.__class__.__name__  in type_lst:
            getattr(new_point, action + '_number')(other)
            return new_point
        
        raise TypeError("Not supported")

    def __pos__(self):
        return Point.duplicate(self)

    def __neg__(self):
        return Point.duplicate(self) * -1

    def __add__(self, other):
        return self.__do__('add', other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__do__('sub', other)

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        return self.__do__('mul', other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self.__do__('div', other)

    def __rtruediv__(self, other):
        return self / other
    
    def __eq__(self, other):

        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        
        raise Exception("Not supported")


    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    # endregion

    def draw(self, color: Color = BLACK, size: float = 10):
        """
        Draw the point on the screen

        Args:
            color: The color of the point
            size: The size of the point

        Return:
            None
        """

        draw_point(self.x, self.y, color, size)
    
    def draw_line(self, point, color: Color = BLACK, size: float = 5):
        draw_line(self.x, self.y, point.x, point.y, color, size)

class Vector():
    """
    This class represent a vector in 2d space
    """

    def __init__(self, start_x: float = 0, start_y: float = 0, end_x: float = 0, end_y: float = 0, length: float = 0, angle: float = 0):
        """
        Define a vector by start_x, start_y and either end_x, end_y or length, angle

        Args:
            start_x: The x coordinate of the start point
            start_y: The y coordinate of the start point 
            end_x: The x coordinate of the end point
            end_y: The y coordinate of the end point 
            length: The length of a vector(always positive)
            angle: The angle of the vector(in degrees and between 0 too 360)

        """

        self.list = [Point(start_x, start_y)]
        self._angle = angle

        if end_x != 0 or end_y != 0:
            self.list.append(Point(end_x, end_y))

        else:
            self.list.append(self.list[0] + Point(  length * math.cos(math.radians(angle)), 
                                                    length * math.sin(math.radians(angle))))

    @property
    def length(self):
        """
        The length of the vector
        """

        return self.list[0].distance(self.list[1])

    @length.setter
    def length(self, value):
        
        # Set the end_point with it's length
        self.list[1] = self.list[0] + Point(value * math.cos(math.radians(self.angle)),
                                            value * math.sin(math.radians(self.angle)))

    @property
    def angle(self):
        """
        The angle of the vector
        """

        # The vector might have the same start and end point and in this case
        # there is no angle.
        # So let's remember the angle from the constructor and use it instead.
        if(self.start_point == self.end_point):
            return self._angle

        self._angle = math.fmod(self.list[0].angle(self.list[1]), 360)

        return self._angle

    @angle.setter
    def angle(self, value):

        if(self.start_point == self.end_point):
            self._angle = value
            return

        # self._angle = value
        self.list[1] = Point(self.length * math.cos(math.radians(value)),
                             self.length * math.sin(math.radians(value)))

    @property
    def start_point(self):
        """
        The start point of the vector
        """
        return self.list[0]

    @start_point.setter
    def start_point(self, point):
        self.list[0] = point

    @property
    def end_point(self):
        """
        The end point of the vector
        """
        return self.list[1]

    @end_point.setter
    def end_point(self, point):
        self.list[1] = point

    # Get a slope from the vector
    # the first parameter if there is one
    # the second is the slope
    def _get_slope(self):
        """
        get the slope of the vector

        Return:
            bool - if has slope(could be infinite)
            float - the slope value
        """
        if self.end_point.x - self.start_point.x == 0:
            return False, 0
        return True, (self.end_point.y - self.start_point.y)/(self.end_point.x - self.start_point.x)

    def get_intesected_point(self, vec):

        """
        Get an intersected point between this and other vector

        Args:
            vec - The other vector
        
        Return:
            bool - has intersecting point(They both have the same slope therfor there are inifinite)
            Point - The intersected point
        """

        has_slope1, m1 = self._get_slope()
        has_slope2, m2 = vec._get_slope()

        # If both slopes are equal
        # Then there are infinite number of intersecting points
        if m1 == m2:
            return False, 0

        # The first vector has a slope but the other doesn't
        elif has_slope1 and not has_slope2:
            return True, Point(vec.start_point.x, m1*(vec.start_point.x - self.start_point.x) + self.start_point.y)

        # The second vector has a slope but the other doesn't
        elif not has_slope1 and has_slope2:
            return True, Point(self.start_point.x, m2*(self.start_point.x - vec.start_point.x) + vec.start_point.y)

        # calculate both x and y
        x = (m2 * vec.start_point.x - m1 * self.start_point.x +
             self.start_point.y - vec.start_point.y) / (m2 - m1)
        y = m1(x - self.start_point.x) + self.start_point.y

        # return a point
        return Point(x, y)

    def is_point_on_vec(self, point, approximation=0.0001):
        """
        Check if a given point is on the vector

        Args:
            point - The point to check
            approximation(optional) - how close can we approximate the point on the vector
        
        Return:
            bool - The point is on the vector
        """

        # The length of the vector subtruct from the lengths that created
        # by the start and end points are bigger from our approximation than
        # the point ins't in the vector
        if math.fabs(self.length - (self.start_point.distance(point) + self.end_point.distance(point))) >= approximation:
            return False
        return True

    @staticmethod
    def ONE():
        return Vector(end_x= 1)
    
    @staticmethod
    def duplicate(vec):
        return Vector(vec.start_point.x, vec.start_point.y, vec.end_point.x, vec.end_point.y, vec.length, vec.angle)

    def get_as_list(self):
        """
        Get the vector as a list

        Return:
            A list [[start.x, start.y],[end.x, end.y]]
        """

        return list(map(lambda i: i.get_list(), self.list))
    
    #region Arithemetic Functions

    def add_vector(self, vector):
        """
        Add an other vector's coordinates to this vector coordinates

        Args:
            vector: The other vector

        Return:
            None
        """

        self.start_point += vector.start_point
        self.end_point += vector.end_point
    
    def add_point(self, point):
        """
        Add a point to this vector coordinates

        Args:
            point: The point

        Return:
            None
        """

        self.add_vector(Vector(point.x, point.y, point.x, point.y))

    def add_number(self, number):
        """
        Add a number to this vector coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.add_point(Point(number, number))

    def sub_vector(self, vector):
        """
        Subtract an other vector's coordinates to this vector coordinates

        Args:
            vector: The other vector

        Return:
            None
        """

        self.start_point -= vector.start_point
        self.end_point -= vector.end_point
    
    def sub_point(self, point):
        """
        Subtruct a point from this vector coordinates

        Args:
            point: The point

        Return:
            None
        """

        self.sub_vector(Vector(point.x, point.y, point.x, point.y))

    def sub_number(self, number):
        """
        Subtruct a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """

        self.sub_point(Point(number, number))

    def mul_vector(self, vector):
        """
        Multiply an other vector's coordinates to this vector coordinates

        Args:
            vector: The other vector

        Return:
            None
        """

        self.start_point *= vector.start_point
        self.end_point *= vector.end_point
    
    def mul_point(self, point):
        """
        Multiply a point from this vector coordinates

        Args:
            point: The point

        Return:
            None
        """

        self.mul_vector(Vector(point.x, point.y, point.x, point.y))

    def mul_number(self, number):
        """
        Add a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.mul_point(Point(number, number))

    def div_vector(self, vector):
        """
        Divide an other vector's coordinates to this vector coordinates

        Args:
            vector: The other vector

        Return:
            None
        """

        self.start_point /= vector.start_point
        self.end_point /= vector.end_point

    def div_point(self, point):
        """
        Divide a point from this vector coordinates

        Args:
            point: The point

        Return:
            None
        """

        self.div_vector(Vector(point.x, point.y, point.x, point.y))

    def div_number(self, number):
        """
        Divide a number to this point coordinates

        Args:
            number: The number

        Return:
            None
        """
        self.div_point(Point(number, number))

    #endregion
    
    # region Operators

    def __do__(self, action, other):
        new_vector = Vector.duplicate(self)
        obj_lst = set(['Vector', 'Point'])
        type_lst = set(['float', 'int'])

        if other.__class__.__name__  in obj_lst:
            getattr(new_vector, action + '_' + other.__class__.__name__ .lower())(other)
            return new_vector

        if other.__class__.__name__  in type_lst:
            getattr(new_vector, action + '_number')(other)
            return new_vector
        
        raise TypeError("Not supported")

    def __pos__(self):
        return Vector.duplicate(self)

    def __neg__(self):
        return Vector.duplicate(self) * -1

    def __add__(self, other):
        return self.__do__('add', other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.__do__('sub', other)

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        return self.__do__('mul', other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self.__do__('div', other)

    def __rtruediv__(self, other):
        return self / other
    
    def __eq__(self, other):

        if isinstance(other, Vector):
            return self.start_point == other.start_point and self.end_point == other.end_point
        
        raise TypeError("Isn't a vector")

    def __repr__(self):
        return self.start_point.__repr__() + self.end_point.__repr__()

    # endregion