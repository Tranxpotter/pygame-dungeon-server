from abc import ABC, abstractmethod

class GameObject(ABC):
    '''Abstract Class of Any Objects'''
    @abstractmethod
    def __init__(self, x:int, y:int, collider, alive:bool = True, *args, **kwargs):
        self.x = x
        self.y = y
        self.collider = collider
        self.alive = alive

    @abstractmethod
    def update(self, dt: float): ...

    @abstractmethod
    def draw(self, camera_pos: tuple[int, int]): ...
