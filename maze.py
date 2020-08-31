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

@dataclass
class NeighboringTile:
    """A neighboring tile object, has a tile object and a direction, from the perspective of the original tile, 0 being north, 1 east, 2 south and 3 west"""
    tile: Tile
    direction: None

class Maze():
    """The maze object itself"""
    wall_char = None
    space_char = None
    maze_tiles = None
    backtrack_tiles = []
    width = None
    height = None

    def __init__(self, wall_char, space_char, width, height):
        """Creates a new maze of size width * height and sets config options"""
        self.wall_char = wall_char
        self.space_char = space_char

        self.width = width
        self.height = height

        # Init maze tiles, all tiles have max walls
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

        # Run the randomized depth first search algorithm to generate a maze
        self.__run_depth_first_search(None, None)

    def __run_depth_first_search(self, start_tile, current_tile):
        """Generates a maze using the randomized depth-first search algorithm"""

        print("Looping...")

        # Generation has finished, stop recursion
        if start_tile and start_tile == current_tile:
            print("Finished!")
            return

        # Start tile is empty, start the recurring loop by selecting a random starting tile
        if not start_tile:
            print("Starting depth first search!")
            start_tile = choice(choice(self.maze_tiles))
            current_tile = start_tile

        # Get neighboring tiles
        neighboring_tile = self.__get_random_neighboring_tile(current_tile.loc.pos_x, current_tile.loc.pos_y)

        # Not empty, destory wall, set tile visited, add visited tile to backtrack tiles and update current tile
        if neighboring_tile:
            self.__remove_tiling_walls(current_tile, neighboring_tile.tile, neighboring_tile.direction)
            current_tile.visited = True
            current_tile = neighboring_tile.tile
            self.backtrack_tiles.append(current_tile)
            print("Destroying wall...")
        
        # No available neighboring tile, get previous tile & remove it from backtrack tiles
        elif self.backtrack_tiles:
            print(len(self.backtrack_tiles))
            current_tile = self.backtrack_tiles.pop()
            print("Backtracking...", len(self.backtrack_tiles))

        # Completely done!
        else:
            return

        # Recursion
        self.__run_depth_first_search(start_tile, current_tile)

    def __get_random_neighboring_tile(self, pos_x, pos_y):
        """Returns a random neighboring tile based on x and y coords"""
        neighboring_tiles = []
        
        # Western tile
        if (pos_x != 0):
            new_tile = self.maze_tiles[pos_y][pos_x - 1]
            if (not new_tile.visited):
                neighboring_tiles.append(NeighboringTile(new_tile, 3))

        # Northern tile
        if (pos_y != 0):
            new_tile = self.maze_tiles[pos_y - 1][pos_x]
            if (not new_tile.visited):
                neighboring_tiles.append(NeighboringTile(new_tile, 0))

        # Eastern tile
        if (pos_x != self.width - 1):
            new_tile = self.maze_tiles[pos_y][pos_x + 1]
            if (not new_tile.visited):
                neighboring_tiles.append(NeighboringTile(new_tile, 1))

        # Southern tile
        if (pos_y != self.height - 1):
            new_tile = self.maze_tiles[pos_y + 1][pos_x]
            if (not new_tile.visited):
                neighboring_tiles.append(NeighboringTile(new_tile, 2))

        # No non-visited neighboring tiles, return empty list
        if not neighboring_tiles:
            print("No non-visited neighboring tiles!")
            return neighboring_tiles

        print("Returning neighboring non-visited tile...")

        # Return random neighboring tile
        return choice(neighboring_tiles)

    def __remove_tiling_walls(self, tile, dest_tile, direction):
        """Removes the wall between tile and neighboring tile objects"""

        # Destroy north wall
        if (direction == 0):
            tile.north_enabled = False
            dest_tile.south_enabled = False

        # Destroy east wall
        elif (direction == 1):
            tile.east_enabled = False
            dest_tile.west_enabled = False

        # Destroy south wall
        elif (direction == 2):
            tile.south_enabled = False
            dest_tile.north_enabled = False

        # Destroy west wall
        elif (direction == 3):
            tile.west_enabled = False
            dest_tile.east_enabled = False

MAZE = Maze('#', '.', 15, 15)

MAZE.generate_maze()

MAZE.print_walls()
