import math

from .gameObject import GameObject

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
        pierce `int`:
            The number of collider the projectile can pass through
        damage `int`:
            The damage this projectile can deal
        source `GameObject`:
            The source of this projectile
    '''
    def __init__(self, name:str, description:str, speed:int|float, angle:float, pierce:int, damage:int, source:GameObject):
        self.name = name
        self.description = description
        self.speed = speed
        self.angle = angle
    
    @property
    def dx(self):
        return self.speed * math.cos(self.angle)

    @property
    def dy(self):
        return self.speed * math.sin(self.angle)



