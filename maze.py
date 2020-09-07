"""This program generates a maze of given width and height and outputs an image based on that"""

from dataclasses import dataclass
from datetime import datetime
from random import random, seed, getrandbits, choice, randint
from PIL import Image
import sys

@dataclass
class Point:
    """A point object, with an x and y."""
    pos_x: float
    pos_y: float

@dataclass
class Tile:
    """A maze tile object, has a point and visited property."""
    loc: Point
    visited: bool = False
    north_wall: bool = True
    east_wall: bool = True
    south_wall: bool = True
    west_wall: bool = True

@dataclass
class NeighboringTile:
    """A neighboring tile object, has a tile object and a direction, from the perspective of the original tile, 0 being north, 1 east, 2 south and 3 west."""
    tile: Tile
    direction: int

class Maze:
    """Generates a maze of given width and height and outputs it as an image."""
    maze_tiles = None
    width = None
    height = None

    def __init__(self, output_path, width, height, method, image_scale):
        """Creates a new maze of size width * height and sets config options."""

        # Set size and width values
        self.width = width
        self.height = height

        # Generating maze using RDFS method
        self.__generate_maze(method)

        # Create maze image
        self.__create_maze_image(output_path, image_scale)

        print("Program finished!")

    def __generate_maze(self, method):
        """Generates maze using chosen method."""

        # Create maze of given size
        self.maze_tiles = [[Tile(Point(x, y)) for x in range(self.width)]for y in range(self.height)]

        # Init randomization
        seed(datetime.now())

        # Run the randomized depth first search algorithm to generate a maze
        if method == 0:
            self.__run_RDFS()

        # Unknown method, log error
        else:
            print("ERROR: Couldn't generate maze because method is unknown!")

        print("Generating maze done!")

    def __create_maze_image(self, output_path, image_scale):
        """Prints current maze to console."""

        print("Creating maze image...")

        # Get pixels
        pixels = self.__maze_to_pixels(0, 255)

        # Create image from pixels
        self.__create_image(output_path, image_scale, pixels, self.width * 2 + 1, self.height * 2 + 1)

        print("Creating image done!")

    def __maze_to_pixels(self, wall_value, tile_value):
        """Creates and returns pixels based on maze."""

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
                above_row_pixels.extend([wall_value, wall_value if element.north_wall else tile_value])
                current_row_pixels.extend([wall_value if element.west_wall else tile_value, tile_value])

                # Final column in tiles
                if element.loc.pos_y == self.height - 1:
                    final_row_pixels.extend([wall_value, wall_value if element.south_wall else tile_value])

                # Final char of row, add east wall
                if element.loc.pos_x == self.width - 1:
                    above_row_pixels.append(wall_value)
                    current_row_pixels.append(wall_value if element.east_wall else tile_value)

                    # Add wall to final row in final column
                    if element.loc.pos_y == self.height - 1:
                        final_row_pixels.append(wall_value)

            # Add above and current row to pixels
            pixels += above_row_pixels
            pixels += current_row_pixels

        # Add final row to pixels
        pixels += final_row_pixels

        # Return pixels
        return pixels

    def __create_image(self, path, scale, pixels, width, height):
        """Creates image and saves it to path based on pixels and size."""

        # Create image from pixels
        img = Image.new('L', (width, height))
        img.putdata(pixels)
        img = img.resize((width * scale, height * scale), Image.NEAREST)
        img.save(path)

    def __run_RDFS(self):
        """Generates a maze using the randomized depth-first search algorithm."""

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
            neighboring_tile = self.__get_random_neighbor(current_tile.loc.pos_x, current_tile.loc.pos_y)
            current_tile.visited = True # Tile is now visited

            # Got a non-visited neighboring tile, remove walls towards tile
            if neighboring_tile:
                self.__remove_walls(current_tile, neighboring_tile.tile, neighboring_tile.direction) # Remove walls between tiles at direction
                current_tile = neighboring_tile.tile # Now visiting this tile
                backtrack_tiles.append(current_tile) # Add new tile to backtrack list
            
            # No non-visited neighboring tiles, backtrack (.pop() gets and removes last item)
            else:
                current_tile = backtrack_tiles.pop()

        self.__add_random_entrances()

        print("Depth-first search done!")

    def __get_random_neighbor(self, pos_x, pos_y):
        """Returns a random neighboring tile based on x and y coords."""
        
        neighboring_tiles = []

        # Northern tile
        if pos_y != 0:
            new_tile = self.maze_tiles[pos_y - 1][pos_x]
            if not new_tile.visited and not new_tile.south_wall == False and not new_tile.west_wall == False and not new_tile.east_wall == False:
                neighboring_tiles.append(NeighboringTile(new_tile, 0))

        # Eastern tile
        if pos_x != self.width - 1:
            new_tile = self.maze_tiles[pos_y][pos_x + 1]
            if not new_tile.visited and not new_tile.north_wall == False and not new_tile.west_wall == False and not new_tile.south_wall == False:
                neighboring_tiles.append(NeighboringTile(new_tile, 1))

        # Southern tile
        if pos_y != self.height - 1:
            new_tile = self.maze_tiles[pos_y + 1][pos_x]
            if not new_tile.visited and not new_tile.north_wall == False and not new_tile.west_wall == False and not new_tile.east_wall == False:
                neighboring_tiles.append(NeighboringTile(new_tile, 2))
        
        # Western tile
        if pos_x != 0:
            new_tile = self.maze_tiles[pos_y][pos_x - 1]
            if not new_tile.visited and not new_tile.south_wall == False and not new_tile.north_wall == False and not new_tile.east_wall == False:
                neighboring_tiles.append(NeighboringTile(new_tile, 3))

        # No non-visited neighboring tiles, return empty list
        if not neighboring_tiles:
            return neighboring_tiles

        # Return random neighboring tile
        return choice(neighboring_tiles)

    def __remove_walls(self, tile, dest_tile, direction):
        """Removes the wall between tile and neighboring tile objects."""

        # Destroy north wall
        if direction == 0:
            tile.north_wall = False
            dest_tile.south_wall = False

        # Destroy east wall
        elif direction == 1:
            tile.east_wall = False
            dest_tile.west_wall = False

        # Destroy south wall
        elif direction == 2:
            tile.south_wall = False
            dest_tile.north_wall = False

        # Destroy west wall
        elif direction == 3:
            tile.west_wall = False
            dest_tile.east_wall = False

    def __add_random_entrances(self):
        """Adds a random entrance and exit, always on opposite sides."""

        # Place horizontal entrance/ exits
        if getrandbits(1) == 0:
            choice(self.maze_tiles[0]).north_wall = False
            choice(self.maze_tiles[-1]).south_wall = False

        # Place vertical entrance/ exits
        else:
            choice(self.maze_tiles)[0].west_wall = False
            choice(self.maze_tiles)[-1].east_wall = False

def print_program_info(error_message):
    """Prints help about maze generator usage and an optional error message, Leave error message empty for help."""

    # Print error message and arguments format
    if error_message:
        print('\nERROR:', error_message, "\nUse 'Maze.py (--)help' for more information.\n")

    # Print help info
    else:
        print("\nThis program generates a maze using command line arguments to determine the maze's characteristics!\n")
        print("Width and height determine the maze's size.")
        print("Method determines the algorithm used to generate the maze, 0 being Randomized Depth First Search.")
        print("Output path being the name the file is saved as, will automatically add .png extension if not specified already.\n")

    print("Arguments format: output path as string, width as int, height as int, method as int and image scale as int (optional).\n")

def create_maze():
    """Parses command line arguments and creates a maze if valid. This is the program entrance."""

    # Get all args
    args = sys.argv[1:]

    # Print help
    if args[0] == "help" or args[0] == "-help" or args[0] == "--help":
        print_program_info("")
        return

    print("\nParsing command line arguments...")

    # Check argument count
    if len(args) > 5:
        print_program_info("Too many arguments! Expected 4 or 5 arguments, but received too many!")
        return

    if len(args) < 4:
        print_program_info("Too few arguments! Expected 4 or 5 arguments, but received too few!")
        return

    # No scale, add 1
    if len(args) == 4:
        args[4] = 1

    # Convert strings to int
    try:
        args[1] = int(args[1])
        args[2] = int(args[2])
        args[3] = int(args[3])
        args[4] = int(args[4])

    # Throw errors
    except ValueError:
        print_program_info("Value type error! Expected valid integers, but got ValueError instead!")
        return

    # Check if maze bigger than 0
    if args[1] < 1 or args[2] < 1 or args[4] < 1:
        print_program_info("Size error! Width, height and image scale must be bigger than 0!")
        return

    # Add .png extensions
    if not args[0].endswith(".png"):
        args[0] += ".png"

    print("Command line arguments parsed succesfully! Generating maze using arguments:", args, "\n")

    # Arguments succesfully verified, generate maze
    Maze(args[0], args[1], args[2], args[3], args[4])

# Run program entrance
create_maze()