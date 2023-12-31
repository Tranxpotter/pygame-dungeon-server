import math
from typing import Callable, Optional, Literal

from engine.mask import Mask

from .gameObject import GameObject
from .collider import Collider
from .obstacle import Obstacle
from .utils import get_angle, resolve, point_to_line_distance, get_mid_pt


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

        Methods
        -------
        update: 
            Called every loop to update the position of the projectile
        move: 
            The function used to move the projectile
        on_expire:
            Things to do once the pierce is used up, travel distance limit hits, or the projectile times out
    '''

    def __init__(self,
                 name: str,
                 description: str,
                 x: int,
                 y: int,
                 speed: int | float,
                 angle: float,
                 collider: Optional[Collider],
                 damage: int,
                 source: GameObject,
                 pierce: Optional[int] = None,
                 range: Optional[int] = None,
                 timer: Optional[int | float] = None, 
                 alive: bool = True):
        super().__init__(x, y, collider, alive)
        self.name = name
        self.description = description
        self.speed = speed
        self.angle = angle
        self.damage = damage
        self.source = source
        self.pierce = pierce
        self.range = range
        self.timer = timer

    def update(self, dt: float):
        '''Called every game loop to update the position and state of the projectile, \n
        when inheriting, call super().update() to do the usual range and timer checking, and also it calls move() automatically'''
        # Check expire
        if self.range and self.range <= 0:
            self.on_expire()
            return
        if self.timer and self.timer <= 0:
            self.on_expire()
            return

        self.move(dt)

    def move(self, dt: float):
        '''Moves the projectile according to its speed and the given delta time'''
        # Projectile movement
        move_distance = self.speed * dt
        if self.range:
            self.range -= move_distance
            if self.range < 0:
                move_distance = -self.range
        if self.timer:
            self.timer -= dt
            if self.timer < 0:
                move_distance = self.speed * (dt + self.timer)
        dx, dy = resolve(move_distance, self.angle)
        self.x += round(dx)
        self.y += round(dy)

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

    def __init__(
            self,
            name: str,
            description: str,
            x: int,
            y: int,
            speed: int | float,
            acceleration: int | float,
            angle: float,
            collider: Collider | None,
            damage: int,
            source: GameObject,
            pierce: int | None = None,
            range: int | None = None,
            timer: int | float | None = None, 
            alive:bool = True):
        super().__init__(
            name,
            description,
            x,
            y,
            speed,
            angle,
            collider,
            damage,
            source,
            pierce,
            range,
            timer,
            alive)
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

    def __init__(
            self,
            name: str,
            description: str,
            x: int,
            y: int,
            speed: int | float,
            angle: float,
            target: Optional[GameObject],
            accuracy: float,
            collider: Collider | None,
            damage: int,
            source: GameObject,
            pierce: int | None = None,
            range: int | None = None,
            timer: int | float | None = None, 
            alive: bool = True):
        super().__init__(
            name,
            description,
            x,
            y,
            speed,
            angle,
            collider,
            damage,
            source,
            pierce,
            range,
            timer,
            alive)
        self.target = target
        self.accuracy = accuracy

    def update(self, dt: float):
        if self.target:
            if self.collider:
                self_mask = self.collider.mask
                frm = (
                    self_mask.get_centerx(
                        self.x), self_mask.get_centery(
                        self.y))
            else:
                frm = (self.x, self.y)

            if self.target.collider:
                target_mask = self.target.collider.mask
                target = (
                    target_mask.get_centerx(
                        self.target.x), target_mask.get_centery(
                        self.target.y))
            else:
                target = (self.target.x, self.target.y)

            new_angle = get_angle(frm, target)
            angle_change = new_angle - self.angle
            if self.collider:
                self.collider.mask.rotate(angle_change, None)
            self.angle = new_angle

        return super().update(dt)

class FastProjectile(Projectile):
    def __init__(self, name: str, description: str, x: int, y: int, speed: int | float, angle: float, collider: Collider | None, damage: int, source: GameObject, pierce: int | None = None, range: int | None = None, timer: int | float | None = None, alive: bool = True):
        super().__init__(name, description, x, y, speed, angle, collider, damage, source, pierce, range, timer, alive)
        self.collisions = []
    
    





    def move(self, dt: float):
        if not self.collider:
            return super().move(dt)
        
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        move_distance = self.speed * dt
        move_x = round(move_distance * math.cos(self.angle), 1)
        move_y = round(move_distance * math.sin(self.angle), 1)

        # print(f"{move_x=}, {move_y=}")

        if self.collider.mask.radius:
            '''Circle stuff'''

        elif self.collider.mask.corners:
            center = self.collider.mask.center
            corners = self.collider.mask.corners

            points_distance = [(corner, round(point_to_line_distance(corner, (center, self.angle)), 1)) for corner in corners]
            distances = list(map(lambda x:x[1], points_distance))

            furthest_points = [
                [corner for corner, _ in filter(lambda x: x[1] == max(distances), points_distance)], 
                [corner for corner, _ in filter(lambda x: x[1] == min(distances), points_distance)]
            ] #[0] are +ve, [1] and -ve
            # print(f"{furthest_points=}")
            new_line = (furthest_points[1][0], furthest_points[0][0])
            
            #Line adjustment due to other points having the same distance from center line
            no_projection_corners = []
            if len(furthest_points[0]) > 1:
                keep_corner = furthest_points[0][0]
                no_projection_corners.append(keep_corner)
                longest_distance = 0
                for corner in furthest_points[0][1::]:
                    distance = point_to_line_distance(corner, new_line)
                    if distance > longest_distance:
                        no_projection_corners.append(corner)
                        try:
                            no_projection_corners.remove(keep_corner)
                        except ValueError:
                            pass
                        keep_corner = corner
                        longest_distance = distance
                
                new_line = (new_line[0], keep_corner)
            
            if len(furthest_points[1]) > 1:
                keep_corner = furthest_points[1][0]
                no_projection_corners.append(keep_corner)
                longest_distance = 0
                for corner in furthest_points[1][1::]:
                    distance = point_to_line_distance(corner, new_line)
                    if distance > longest_distance:
                        no_projection_corners.append(corner)
                        try:
                            no_projection_corners.remove(keep_corner)
                        except ValueError:
                            pass
                        keep_corner = corner
                        longest_distance = distance

                new_line = (keep_corner, new_line[1])
            # print(f"{new_line=}")
            # print(f"{no_projection_corners=}")

            new_polygon_corners = []
            for corner in corners:
                distance = point_to_line_distance(corner, new_line)
                if distance > 0 or corner in no_projection_corners:
                    new_polygon_corners.append(corner)
                elif distance < 0 and corner:
                    new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
                else:
                    if self.angle >= 1:
                        new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
                        new_polygon_corners.append(corner)
                    else:
                        new_polygon_corners.append(corner)
                        new_polygon_corners.append((corner[0] + move_x, corner[1] + move_y))
            
            # print(new_polygon_corners)







class FastProjectileCollider(Collider):
    def __init__(self, heights: list[int], mask: Mask):
        super().__init__(heights, mask)
    
    def on_collide(self, obj: GameObject):
        return super().on_collide(obj)



