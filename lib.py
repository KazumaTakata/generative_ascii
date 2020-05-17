from enum import Enum, auto
from typing import Dict, Tuple, Sequence, List, Type
import time
import random
from random import randrange
from abc import ABCMeta, abstractmethod
import os
import sys, tty
from select import select

class BackOrFront(Enum):
    BACK = auto()
    FRONT = auto()


class Color(Enum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MEGANTA = auto()
    CYAN = auto()
    WHITE = auto()


class ObjectKind(Enum):
    Rect = auto()
    Tri = auto()
    

ColorToFG: Dict[Color, int] = {
    Color.BLACK: 30,
    Color.RED: 31,
    Color.GREEN: 32,
    Color.YELLOW: 33,
    Color.BLUE: 34,
    Color.MEGANTA: 35,
    Color.CYAN: 36,
    Color.WHITE: 37
}

ColorToBG: Dict[Color, int] = {
    Color.BLACK: 40,
    Color.RED: 41,
    Color.GREEN: 42,
    Color.YELLOW: 43,
    Color.BLUE: 44,
    Color.MEGANTA: 45,
    Color.CYAN: 46,
    Color.WHITE: 47
}


def setColor(color_code: Color, back_or_front: BackOrFront):
    if back_or_front == BackOrFront.BACK:
        print(f"\u001b[{ColorToBG[color_code]}m", end='')
    else:
        print(f"\u001b[{ColorToFG[color_code]}m", end='')

def resetColor():
    print("\u001b[0m", end='')

def moveCusorTo(x:int, y:int):
    print(f"\u001b[{x};{y}H", end='')

def moveCusorRight():
    print(f"\u001b[1C", end='')


def clearScreen(color:Color):
    setColor(color, BackOrFront.BACK)
    print(f"\u001b[2J", end='')

def hideCursor():
    print(f"\u001b[?25l", end='')


def drawRect(x:int, y:int, width:int, height:int, color:Color):
    setColor(color, BackOrFront.BACK)
    for j in range(height):
        moveCusorTo(y+j,x)
        for i in range(width):
            print(" ", end='', flush=True)

    

class Pos:
    x:int
    y:int
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y


class Object(metaclass=ABCMeta):
    pos:Pos
    color:Color
    velo:int
    @abstractmethod
    def draw(self) -> None: pass 

    def update(self):
        self.pos.y += self.velo

    
    @classmethod 
    @abstractmethod
    def rand_gen(cls, rand:bool): pass



    
class BitImage(Object):
    width:int
    height:int
    data:List[str]

    def __init__(self, pos:Pos, color:Color, filename:str):
        self.pos = pos
        self.color = color
        self.velo = randrange(1, 3)
        f = open(filename, "r")
        self.data = f.read().split('\n')


    def draw(self):
        for j in range(len(self.data)):
            setColor(self.color, BackOrFront.BACK)
            moveCusorTo(self.pos.y+j,self.pos.x)
            for i in range(len(self.data[j])):
                if self.data[j][i] == '+':
                    print(" ", end='', flush=True)
                else:
                    moveCusorRight()


    @classmethod
    def rand_gen(cls, rand:bool):
       pass 
 


def rand_gen_bitimage(rand:bool, filename:str):
    y:int
    if rand:
        y = randrange(90)
    else:
        y = 0
    width = randrange(10) 
    height = randrange(10) 
    x = randrange(90)
    bitimage: BitImage = BitImage(Pos(x, y), random.choice(list(Color)), filename)

    return bitimage 


class Rect(Object):
    width:int
    height:int

    def __init__(self, pos:Pos, color:Color, width:int, height:int):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height
        self.velo = randrange(1, 3)

    def draw(self):
        setColor(Color.WHITE, BackOrFront.BACK)

        moveCusorTo(self.pos.y-1,self.pos.x+1)
        for i in range(self.width):
            print(" ", end='', flush=True)
        
        for j in range(self.height):
            setColor(self.color, BackOrFront.BACK)
            moveCusorTo(self.pos.y+j,self.pos.x)
            for i in range(self.width):
                print(" ", end='', flush=True)
                
            setColor(Color.WHITE, BackOrFront.BACK)
            if j != self.height - 1: 
                print(" ", end='', flush=True)
    
    @classmethod
    def rand_gen(cls, rand:bool):
        y:int
        if rand:
            y = randrange(90)
        else:
            y = 0
        width = randrange(10) 
        height = randrange(10) 
        x = randrange(90)
        rect: Rect = cls(Pos(x, y), random.choice(list(Color)),  width, height)

        return rect

class Triangle(Object):
    width:int
    height:int

    def __init__(self, pos:Pos, color:Color, height:int):
        self.pos = pos
        self.color = color
        self.height = height
        self.velo = randrange(1, 3)

    def draw(self):
        setColor(self.color, BackOrFront.BACK)
        for j in range(self.height):
            moveCusorTo(self.pos.y+j,self.pos.x)
            for i in range(j):
                print(" ", end='', flush=True)
                
    
    @classmethod
    def rand_gen(cls, rand:bool):
        y:int
        if rand:
            y = randrange(90)
        else:
            y = 0
        height = randrange(10) 
        x = randrange(90)
        triangle: Triangle = cls(Pos(x, y), random.choice(list(Color)), height)

        return triangle 



class Scene:

    window_rows:int
    window_columns:int
    objects: List[Object]

    def __init__(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        self.window_rows = int(rows)
        self.window_columns = int(columns)
        self.objects = []

    def add(self, obj:Object):
        self.objects.append(obj)





