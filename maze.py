"""This program will allow users to create a maze"""

from dataclasses import dataclass

@dataclass
class Point:
    """A point object, with an x and y"""
    pos_x: float
    pos_y: float

@dataclass
class Line:
    """A line object, has a start and end point"""
    start: Point
    end: Point

class Maze():
    """The maze object itself"""
    wall_char = None
    space_char = None
    entrance_x = None
    exit_x = None
    maze_body = None
    width = None
    height = None

    def __init__(self, wall_char, space_char, width, height):
        """Creates a new maze of size width * height and sets config options"""
        self.wall_char = wall_char
        self.space_char = space_char

        self.width = width
        self.height = height

        self.maze_body = [[False for x in range(self.width)]for y in range(self.height)]

    def print_walls(self):
        """Prints current maze to screen"""        
        print(''
                .join([(self.space_char if x == self.entrance_x else self.wall_char)
                for x in range(self.width + 2)]))

        for row in self.maze_body:
            print(
                self.wall_char
                + ''.join([(self.space_char if not element else self.wall_char)for element in row])
                + self.wall_char)

        print(''
                .join([(self.space_char if x == self.exit_x else self.wall_char)
                for x in range(self.width + 2)]))

    def set_entrance(self, entrance_x):
        """Sets entrance for maze. This will be at top only for now"""
        if self.__validate_opening(entrance_x + 1):
            self.entrance_x = entrance_x + 1

    def set_exit(self, exit_x):
        """Sets exit for maze. This will be at bottom only for now"""
        if self.__validate_opening(exit_x + 1):
            self.exit_x = exit_x + 1

    def __validate_opening(self, pos_x):
        """Validates a to check whether it conforms to maze bounds"""
        try:
            if pos_x < 0 or pos_x > self.width:
                print("ERROR: Opening x is out of range! Couldn't add opening!")
                return False

            return True

        except TypeError:
            print("ERROR: Invalid opening x argument! Couldn't add opening!")

    def add_wall_horizontal(self, start_x, end_x, pos_y):
        """Adds a horizontal wall from start to end x, at y"""
        wall = Line(Point(start_x, pos_y), Point(end_x, pos_y))

        if self.__validate_wall(wall):
            for pos_x in range(wall.start.pos_x, wall.end.pos_x):
                self.maze_body[wall.start.pos_y][pos_x] = True

    def add_wall_vertical(self, start_y, end_y, pos_x):
        """Adds a vertical wall from start to end y, at x"""
        wall = Line(Point(pos_x, start_y), Point(pos_x, end_y))

        if self.__validate_wall(wall):
            for pos_y in range(wall.start.pos_y, wall.end.pos_y):
                self.maze_body[pos_y][wall.start.pos_x] = True

    def __validate_wall(self, line):
        """Validates a wall to check whether it conforms to maze bounds"""
        try:
            if line.start.pos_x < 0 or line.start.pos_x > self.width:
                print("ERROR: Start pos x is invalid! Couldn't add wall!")
                return False

            if line.start.pos_y < 0 or line.start.pos_y > self.height:
                print("ERROR: Start pos y is invalid! Couldn't add wall!")
                return False

            if line.end.pos_x < 0 or line.end.pos_x > self.width:
                print("ERROR: End pos x is invalid! Couldn't add wall!")
                return False

            if line.end.pos_y < 0 or line.start.pos_y > self.height:
                print("ERROR: End pos y is invalid! Couldn't add wall!")
                return False

            return True

        except AttributeError:
            print("ERROR: Invalid line object! Couldn't add wall!")
        except TypeError:
            print("ERROR: Invalid position arguments! Couldn't add wall!")

MAZE = Maze('#', ' ', 15, 15)

MAZE.set_entrance(14)
MAZE.set_exit(8)

MAZE.print_walls()
