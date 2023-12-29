import math
from typing import Optional, Literal

from .gameObject import GameObject
from .collider import Collider
from .obstacle import Obstacle
from .utils import get_angle


class Projectile(GameObject):
    '''
        Represents any projectile in the game

        Attributes
        ----------
        name `str`:
            Name of the projectile
        description `str`:
            Description of the projectile
        x `int`:
            The x-coordinate of the top left corner of the projectile
        y `int`:
            The y-coordinate of the top left corner of the projectile
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
        timer `int`|`float`:
            The time the bullet can travel before disappearing
    '''

    def __init__(self,
                 name: str,
                 description: str,
                 x:int, 
                 y:int, 
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
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.collider = collider
        self.damage = damage
        self.source = source
        self.pierce = pierce
        self.range = range
        self.timer = timer

    @property
    def dx(self):
        return self.speed * math.cos(self.angle)

    @property
    def dy(self):
        return self.speed * math.sin(self.angle)

    def update(self, dt: float):
        '''Called every game loop to update the position and state of the projectile, \n
        when inheriting, call super().update() to do the usual range and timer checking, and also it calls move() automatically'''
        #Check expire
        if self.range and self.range <= 0:
            self.on_expire()
            return
        if self.timer and self.timer <= 0:
            self.on_expire()
            return
        
        self.move(dt)
    
    def move(self, dt:float):
        '''Moves the projectile according to its speed and the given delta time'''
        #Projectile movement
        move_distance = self.speed * dt
        if self.range:
            self.range -= move_distance
            if self.range < 0:
                move_distance = -self.range
        if self.timer:
            self.timer -= dt
            if self.timer < 0:
                move_distance = self.speed * (dt + self.timer)
        
        self.x += round(self.dx * dt)
        self.y += round(self.dy * dt)
    
    def on_expire(self): ...

class AcceleratingProjectile(Projectile):
    '''
        Represents an accelerating projectile, makes accelerating projectile setup easier

        Attributes
        ----------
        acceleration `int`|`float`:
            The amount the speed will increase or decrease in 1 second
        See `Projectile` for the other attributes
    '''
    def __init__(self, name: str, description: str, x: int, y: int, speed: int | float, acceleration:int|float, angle: float, collider: Collider | None, damage: int, source: GameObject, pierce: int | None = None, range: int | None = None, timer: int | float | None = None):
        super().__init__(name, description, x, y, speed, angle, collider, damage, source, pierce, range, timer)
        self.acceleration = acceleration
    
    def move(self, dt: float):
        self.speed += self.acceleration * 0.5 * dt
        super().move(dt)
        self.speed += self.acceleration * 0.5 * dt

class HomingPorjectile(Projectile):
    '''
        Represents a homing projectile, makes homing projectile setup easier

        Attributes
        ----------
        target `gameObject` | None:
            The object that the projectile will home in on, if not given, the projectile will move at its last trajectory
        accuracy `float`:
            From 0 to 1, 0 doesn't home in at all while 1 is a a definite hit
    '''
    def __init__(self, name: str, description: str, x: int, y: int, speed: int | float, angle: float, target: Optional[GameObject], accuracy:float, collider: Collider | None, damage: int, source: GameObject, pierce: int | None = None, range: int | None = None, timer: int | float | None = None):
        super().__init__(name, description, x, y, speed, angle, collider, damage, source, pierce, range, timer)
        self.target = target
        self.accuracy = accuracy
    
    def update(self, dt: float):
        if self.target:
            if self.collider:
                self_mask = self.collider.mask
                frm = (self_mask.get_centerx(self.x), self_mask.get_centery(self.y))
            else:
                frm = (self.x, self.y)
                
            
            if self.target.collider:
                target_mask = self.target.collider.mask
                target = (target_mask.get_centerx(self.target.x), target_mask.get_centery(self.target.y))
            else:
                target = (self.target.x, self.target.y)

            
            new_angle = get_angle(frm, target)
            angle_change = new_angle - self.angle
            if self.collider:
                self.collider.mask.rotate(angle_change, None)
            self.angle = new_angle

        return super().update(dt)

