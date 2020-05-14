"""This program will allow users to create a maze"""

from dataclasses import dataclass
from datetime import datetime
from random import random, seed, getrandbits

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
        if self.__validate_opening(entrance_x):
            self.entrance_x = entrance_x

    def set_exit(self, exit_x):
        """Sets exit for maze. This will be at bottom only for now"""
        if self.__validate_opening(exit_x):
            self.exit_x = exit_x

    def __validate_opening(self, pos_x):
        """Validates a to check whether it conforms to maze bounds"""
        try:
            if pos_x < 1 or pos_x > self.width:
                print("ERROR: Opening x is out of range! Couldn't add opening!")
                return False

            return True

        except TypeError:
            print("ERROR: Invalid opening x argument! Couldn't add opening!")

    def add_wall_horizontal(self, pos_x, pos_y, width):
        """Adds a horizontal wall from start to end x, at y"""
        wall = Line(Point(pos_x, pos_y), Point(pos_x + width, pos_y))

        if self.__validate_wall(wall):
            for pos_x in range(wall.start.pos_x, wall.end.pos_x):
                self.maze_body[wall.start.pos_y][pos_x] = True

    def add_wall_vertical(self, pos_x, pos_y, height):
        """Adds a vertical wall from start to end y, at x"""
        wall = Line(Point(pos_x, pos_y), Point(pos_x, pos_y + height))

        if self.__validate_wall(wall):
            for pos_y in range(wall.start.pos_y, wall.end.pos_y):
                self.maze_body[pos_y][wall.start.pos_x] = True

    def __validate_wall(self, wall):
        """Validates a wall to check whether it conforms to maze bounds"""
        try:
            if wall.start.pos_x < 0 or wall.end.pos_x > self.width or wall.start.pos_x > wall.end.pos_x:
                print("ERROR: Pos x is out of bounds! Couldn't add wall! Start: {}, end: {}"
                        .format(wall.start.pos_x, wall.end.pos_x))
                return False

            if wall.start.pos_y < 0 or wall.start.pos_y > self.height or wall.start.pos_y > wall.end.pos_y:
                print("ERROR: Pos y is out of bounds! Couldn't add wall! Start: {}, end: {}"
                        .format(wall.start.pos_y, wall.end.pos_y))
                return False

            if wall.start.pos_x == wall.end.pos_x and wall.start.pos_y == wall.end.pos_y:
                print ("ERROR: Start and end position is identical! Couldn't add wall!")
                return False

            return True

        except AttributeError:
            print("ERROR: Invalid line object! Couldn't add wall!")
        except TypeError:
            print("ERROR: Invalid position arguments! Couldn't add wall!")

    def generate_maze(self):
        """Generates a maze randomly"""

        seed(datetime.now())

        for y in range(self.height):
            for x in range(self.width):
                # Entrance/ exit tile always empty
                if y is 0 and x == self.entrance_x - 1 or y is self.height - 1 and x == self.exit_x - 1:
                    continue

                top_taken = y == 0 or self.maze_body[y-1][x]
                left_taken = x == 0 or self.maze_body[y][x-1]
                top_left_taken = x == 0 or y == 0 or self.maze_body[y-1][x-1]
                top_right_taken = x == self.width-1 or y == 0 or self.maze_body[y-1][x+1]

                if not top_taken or not left_taken:
                    self.place_wall_random(x,y)

    def place_wall_random(self, x, y):
        """Places a wall randomly at x and y"""
        if getrandbits(1):
            self.maze_body[y][x] = True

MAZE = Maze('#', ' ', 15, 15)

MAZE.set_entrance(2)

MAZE.set_exit(8)

MAZE.generate_maze()

MAZE.print_walls()
