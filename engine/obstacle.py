from typing import Literal, Optional

from .gameObject import GameObject
from .collider import Collider

class Obstacle(GameObject):
    '''Represents any non-movable obstacles in the game
    
    Attributes
    ----------
    heights `list[int]`:
        see also `Collider`
    thickness `int`:
        pierce reduction when projectiles hit, -1 for absolute blocking
    
    Tips
    ----
    Obstacle should not be the one handling collision, therefore, on_collide should not be implemented unless otherwise needed
    '''
    def __init__(self, x: int, y: int, heights:list[int], thickness:int, collider:Optional[Collider], alive: bool = True):
        super().__init__(x, y, collider, alive)
        self.heights = heights
        self.thickness = thickness

    def update(self, dt: float):
        return super().update(dt)
    
    def draw(self, camera_pos: tuple[int, int]):
        return super().draw(camera_pos)
    
    
        
    


class BreakableObstacle(Obstacle):
    '''Represents any breakable obstacles in the game
    
    Attributes
    ----------
    hp `int`:
        hp of the obstacle, breaks when reaches 0
    max_hp `int`:
        max hp of the obstacle
    immune `bool`:
        if the obstacle is immune to damage at that moment
    resistance `float`:
        damage taken reduction of the obstacle, in percentage of damage reduced
    
    Methods
    -------

    
    Tips
    ----
    Refer to `Obstacle`
    '''
    def __init__(self, x: int, y: int, heights: list[int], thickness: int, collider: Collider | None, hp:int, max_hp:int, immune:bool, resistance:float, alive: bool = True):
        super().__init__(x, y, heights, thickness, collider, alive)
        self.hp = hp
        self.max_hp = max_hp
        self.immune = immune
        self.resistance = resistance

    def on_break(self):
        ...


    



