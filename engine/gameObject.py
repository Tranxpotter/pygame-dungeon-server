from abc import ABC, abstractmethod
from typing import Literal


class GameObject(ABC):
    '''Abstract Class of Any Objects'''
    @abstractmethod
    def __init__(self, *args, **kwargs):...
    
    @abstractmethod
    def update(self, dt:float):...

    @abstractmethod
    def draw(self, camera_pos:tuple[int, int]):...

