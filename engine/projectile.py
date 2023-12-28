import math
from typing import Optional, Literal

from .gameObject import GameObject
from .collider import Collider
from .obstacle import Obstacle


class Projectile(GameObject):
    '''
        Represents any projectile in the game

        Attributes
        ----------
        name `str`:
            Name of the projectile
        description `str`:
            Description of the projectile
        speed `int`|`float`:
            Speed of the projectile in pixels
        angle `float`:
            The angle of the projectile it is aimed at, respective to the horizontal
        heights list[`int`]:
            The heights of the projectile, used for collision detection and ignoring
        damage `int`:
            The damage this projectile can deal
        source `GameObject`:
            The source of this projectile
        pierce `int`:
            The number of collider the projectile can pass through
        range `int`:
            The distance the bullet can travel before disappearing
    '''

    def __init__(self,
                 name: str,
                 description: str,
                 speed: int | float,
                 angle: float,
                 collider: Optional[Collider],
                 damage: int,
                 source: GameObject,
                 pierce: Optional[int] = None,
                 range: Optional[int] = None,
                 timer: Optional[int | float] = None):
        self.name = name
        self.description = description
        self.speed = speed
        self.angle = angle
        self.pierce = pierce
        self.range = range
        self.collider = collider
        self.damage = damage
        self.source = source

    @property
    def dx(self):
        return self.speed * math.cos(self.angle)

    @property
    def dy(self):
        return self.speed * math.sin(self.angle)

    def on_expire(self): ...
