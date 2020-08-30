"""This program will allow users to create a maze"""

from dataclasses import dataclass
from datetime import datetime
from random import random, seed, getrandbits, choice, randint

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

@dataclass
class Tile:
    """A maze tile object, has a point and visited property"""
    loc: Point
    visited: None
    north_enabled: None
    east_enabled: None
    south_enabled: None
    west_enabled: None

class Maze():
    """The maze object itself"""
    wall_char = None
    space_char = None
    maze_tiles = None
    width = None
    height = None

    def __init__(self, wall_char, space_char, width, height):
        """Creates a new maze of size width * height and sets config options"""
        self.wall_char = wall_char
        self.space_char = space_char

        self.width = width
        self.height = height

        # Init maze tiles
        self.maze_tiles = [[Tile(Point(x, y), False, True, True, True, True) for x in range(self.width)]for y in range(self.height)]

    def print_walls(self):
        """Prints current maze to console"""
        
        # Row below is a row without tiles but only walls only calculated on the final row of tileset
        row_below = ''

        for row in self.maze_tiles:
            # Row above is a row without tiles but only walls
            row_above = ''
            # Current row is a row with tiles and walls
            current_row = ''

            # Loop through each row in maze tiles
            for element in row:
                row_above += self.wall_char + (self.wall_char if element.north_enabled else self.space_char)
                current_row += (self.wall_char if element.west_enabled else self.space_char) + self.space_char

                # Final column in tiles
                if (element.loc.pos_y == self.height - 1):
                    row_below += self.wall_char + (self.wall_char if element.south_enabled else self.space_char)

                # Final char of row, add east wall
                if (element.loc.pos_x == self.width - 1):
                    row_above += self.wall_char
                    current_row += self.wall_char if element.east_enabled else self.space_char

                    # Add wall to row_below if final column
                    if (element.loc.pos_y == self.height - 1):
                        row_below += self.wall_char
            
            # Print the row above and current row
            print(row_above)
            print(current_row)

        # Print the final row
        print (row_below)
    
    def generate_maze(self):
        """Generates a maze randomly"""

        # Make randomization random by seeding it
        seed(datetime.now())

        tile = choice(choice(self.maze_tiles))

        neighbor_tiles = []

        if (tile.loc.pos_x != 0):
            neighbor_tiles.append(self.maze_tiles[tile.loc.pos_y][tile.loc.pos_x - 1])

        if (tile.loc.pos_y != 0):
            neighbor_tiles.append(self.maze_tiles[tile.loc.pos_y - 1][tile.loc.pos_x])

        if (tile.loc.pos_x != self.width - 1):
            neighbor_tiles.append(self.maze_tiles[tile.loc.pos_y][tile.loc.pos_x + 1])

        if (tile.loc.pos_y != self.height - 1):
            neighbor_tiles.append(self.maze_tiles[tile.loc.pos_y + 1][tile.loc.pos_x])

        # Todo: Check visited tiles

        newTile = choice(neighbor_tiles)

        newTile.north_enabled = False
        newTile.south_enabled = False

        print(neighbor_tiles)



    def place_wall_random(self, x, y):
        """Places a wall randomly at x and y"""
        if getrandbits(1):
            self.maze_tiles[y][x] = True

MAZE = Maze('#', '.', 2, 2)

MAZE.generate_maze()

MAZE.print_walls()
