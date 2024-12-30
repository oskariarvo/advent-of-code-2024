# Animation module copied from shaansheikh: https://gist.github.com/shaansheikh/6336238447ea2e351d0aa395e748d03a

from typing import List
import time
from termcolor import colored

CURSOR_UP = "\033[F"

class WarehouseVisualizer:
    def __init__(self):
        self.frames = 0
        self.num_lines = 0

    def __val_to_char(self, val):
        if val == '#':
            return colored('#', 'blue', None, ['bold'])
        if val in '[]O':
            return colored(val, 'green', None, ['bold'])
        if val == '@':
            return colored(val, 'red', None, ['bold'])
        if val == '.':
            return ' '
        return val
    
    def __grid_to_str(self, grid: List[List[chr]]):
        return '\n'.join([''.join([self.__val_to_char(c) for c in gridline]) for gridline in grid])
    
    def show_frame(self, grid: List[List[chr]], frametime=0):
        """
        Print out another frame of the animatio to the terminal. It will print on top of the last frame
        grid: A 2d list where each cell contains one character
        frametime: How long each frame should remain on the screen in seconds
        """
        info = f'Move: {self.frames+1}\n'
        frame = info + self.__grid_to_str(grid)
        if self.frames == 0:
            self.num_lines = len(grid)
        else:
            assert self.num_lines == len(grid)
        
        print(CURSOR_UP * (self.num_lines+1), end="")
        print(frame)
        self.frames += 1
        time.sleep(frametime)