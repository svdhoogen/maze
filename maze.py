"""This program will generate a random maze using randomized depth-first search algorithm, and then creates an image based on the created mazes"""

from dataclasses import dataclass
from datetime import datetime
from random import random, seed, getrandbits, choice, randint
from PIL import Image

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
    visited: bool = False
    north_enabled: bool = True
    east_enabled: bool = True
    south_enabled: bool = True
    west_enabled: bool = True

@dataclass
class NeighboringTile:
    """A neighboring tile object, has a tile object and a direction, from the perspective of the original tile, 0 being north, 1 east, 2 south and 3 west"""
    tile: Tile
    direction: int

class Maze():
    """The maze object"""
    maze_tiles = None
    width = None
    height = None

    def __init__(self, width, height):
        """Creates a new maze of size width * height and sets config options"""

        # Set size and width values
        self.width = width
        self.height = height

        print("Initializing empty maze tiles...")

        # Init default maze tiles, all walls enabled
        self.maze_tiles = [[Tile(Point(x, y)) for x in range(self.width)]for y in range(self.height)]

        # Generate a new maze
        self.__generate_maze()

        # Create maze image
        self.__create_maze_image()

        print("Program finished!")

    def __generate_maze(self):
        """Generates a maze randomly"""

        # Make randomization random by seeding it
        seed(datetime.now())

        # Run the randomized depth first search algorithm to generate a maze
        self.__run_depth_first_search()

    def __create_maze_image(self):
        """Prints current maze to console"""

        print("Creating maze image...")

        # Get pixels
        pixels = self.__get_maze_pixels(0, 255)

        # Create image from pixels
        self.__create_image('maze.png', pixels, self.width * 2 + 1, self.height * 2 + 1)

        print("Creating image done!")

    def __get_maze_pixels(self, wall_value, tile_value):
        """Creates maze pixels based on maze tiles"""

        # Contains the pixels used to create image, and image height and width
        pixels = []

        # Row below is a row without tiles but only walls only calculated on the final row of tileset
        final_row_pixels = []

        # Determine row pixel data from maze tiles
        for row in self.maze_tiles:
            above_row_pixels = [] # Row above is a row without tiles but only walls
            current_row_pixels = [] # Current row is a row with tiles and walls

            # Get above, current and final row pixels
            for element in row:
                above_row_pixels.extend([wall_value, wall_value if element.north_enabled else tile_value])
                current_row_pixels.extend([wall_value if element.west_enabled else tile_value, tile_value])

                # Final column in tiles
                if (element.loc.pos_y == self.height - 1):
                    final_row_pixels.extend([wall_value, wall_value if element.south_enabled else tile_value])

                # Final char of row, add east wall
                if (element.loc.pos_x == self.width - 1):
                    above_row_pixels.append(wall_value)
                    current_row_pixels.append(wall_value if element.east_enabled else tile_value)

                    # Add wall to final row in final column
                    if (element.loc.pos_y == self.height - 1):
                        final_row_pixels.append(wall_value)

            # Add above and current row to pixels
            pixels += above_row_pixels
            pixels += current_row_pixels

        # Add final row to pixels
        pixels += final_row_pixels

        return pixels

    def __create_image(self, path, pixels, width, height):
        """Creates image and saves it to path based on pixels and size"""

        # Create image from pixels
        img = Image.new('L', (width, height))
        img.putdata(pixels)
        img.save(path)

    def __run_depth_first_search(self):
        """Generates a maze using the randomized depth-first search algorithm"""

        print("Starting depth first search!")

        # Loop variables
        neighboring_tile = None
        backtrack_tiles = []

        # Get random start tile
        start_tile = choice(choice(self.maze_tiles))
        current_tile = start_tile
        backtrack_tiles.append(current_tile)

        # Do until all paths have been made
        while neighboring_tile or backtrack_tiles:
            neighboring_tile = self.__get_random_neighboring_tile(current_tile.loc.pos_x, current_tile.loc.pos_y)

            # Got a non-visited neighboring tile, remove walls towards tile
            if neighboring_tile:
                self.__remove_tiling_walls(current_tile, neighboring_tile.tile, neighboring_tile.direction) # Remove walls between tiles at direction
                current_tile.visited = True # Tile is now visited
                current_tile = neighboring_tile.tile # Now visiting this tile
                backtrack_tiles.append(current_tile) # Add new tile to backtrack list
            
            # No non-visited neighboring tiles, backtrack (.pop() gets and removes last item)
            else:
                current_tile = backtrack_tiles.pop()

        self.__add_random_entrances()

        print("Depth-first search done!")

    def __get_random_neighboring_tile(self, pos_x, pos_y):
        """Returns a random neighboring tile based on x and y coords"""
        neighboring_tiles = []

        # Northern tile
        if (pos_y != 0):
            new_tile = self.maze_tiles[pos_y - 1][pos_x]
            if (not new_tile.visited and not new_tile.south_enabled == False and not new_tile.west_enabled == False and not new_tile.east_enabled == False):
                neighboring_tiles.append(NeighboringTile(new_tile, 0))

        # Eastern tile
        if (pos_x != self.width - 1):
            new_tile = self.maze_tiles[pos_y][pos_x + 1]
            if (not new_tile.visited and not new_tile.north_enabled == False and not new_tile.west_enabled == False and not new_tile.south_enabled == False):
                neighboring_tiles.append(NeighboringTile(new_tile, 1))

        # Southern tile
        if (pos_y != self.height - 1):
            new_tile = self.maze_tiles[pos_y + 1][pos_x]
            if (not new_tile.visited and not new_tile.north_enabled == False and not new_tile.west_enabled == False and not new_tile.east_enabled == False):
                neighboring_tiles.append(NeighboringTile(new_tile, 2))
        
        # Western tile
        if (pos_x != 0):
            new_tile = self.maze_tiles[pos_y][pos_x - 1]
            if (not new_tile.visited and not new_tile.south_enabled == False and not new_tile.north_enabled == False and not new_tile.east_enabled == False):
                neighboring_tiles.append(NeighboringTile(new_tile, 3))

        # No non-visited neighboring tiles, return empty list
        if not neighboring_tiles:
            return neighboring_tiles

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

    def __add_random_entrances(self):
        """Adds a random entrance and exit, which are always on opposite sides"""

        # Place horizontal entrance/ exits
        if getrandbits(1) == 0:
            choice(self.maze_tiles[0]).north_enabled = False
            choice(self.maze_tiles[-1]).south_enabled = False

        # Place vertical entrance/ exits
        else:
            choice(self.maze_tiles)[0].west_enabled = False
            choice(self.maze_tiles)[-1].east_enabled = False

Maze(1000, 1000)