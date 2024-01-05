from typing import Callable
import math

from .gameObject import GameObject
from .mask import Mask
from .utils import vec_orthogonal, vec_addition, vec_opposite, vec_normalize, point_to_line_distance


class Collider:
    '''
        Added to the attributes of any class that can collide with other objects as `self.collider`

        Parameters
        ----------
        heights `list`[`int`]:
            The heights of which the object can collide at
        mask `Mask`:
            Mask of the object, used for collision detection
        on_collide `Callable`[[GameObject], None]:
            Function to call when a collision is detected, takes in the other colliding object as argument

        Attributes
        ----------
        collided `list`[`GameObject`]:
            Stores all the object that has collided with this collider

        Methods
        -------
        on_collide(self, obj `GameObject`):
            Function to call when a collision is detected, originally it only checks if the object has collided before and return if its True.
        check_collided(self, obj `GameObject`):
            Checks if the object is in the collided list
        finish_collision_check(self):
            Called once the collision detection is done with this object
    '''

    def __init__(self,
                 heights: list[int],
                 mask: Mask,):
        self.heights = heights
        self.mask = mask
        self.collided: list[GameObject] = []
    
    def on_collide(self, obj:GameObject):
        if self.check_collided(obj):
            return

    def check_collided(self, obj:GameObject) -> bool:
        '''Returns True if the object is in the collided list, otherwise, return False and add the object to the collided list\n
        If class does not require special collided checking, simply write `return super().check_collided(obj)`
        '''
        if obj in self.collided:
            return True
        self.collided.append(obj)
        return False

    def on_finish_collision_check(self) -> None:
        ...

class FastCollider(Collider):
    def __init__(self, heights: list[int], mask: Mask):
        super().__init__(heights, mask)
        self.original_mask = mask
    
    def on_move(self, move_vec:tuple[int|float, int|float]):
        if move_vec == (0, 0):
            self.mask = self.original_mask
            return
        new_mask_corners = []
        if self.mask.radius:
            '''Circle stuff'''
            #Find the 2 furthest points from the center line in the original circle
            center = self.mask.center
            norm = vec_normalize(move_vec)
            d_x, d_y = round(self.mask.radius * norm[0], 1), round(self.mask.radius * norm[1], 1)
            if move_vec[1] >= 0:
                new_mask_corners.append((center[0] + d_x, center[1] + d_x))
                new_mask_corners.append((center[0] - d_x, center[1] - d_y))
            else:
                new_mask_corners.append((center[0] - d_x, center[1] - d_x))
                new_mask_corners.append((center[0] + d_x, center[1] + d_y))
            
            for corner in reversed(new_mask_corners.copy()):
                new_mask_corners.append((corner[0] + move_vec[0], corner[1] + move_vec[1]))
            


        elif self.mask.corners:
            '''Polygon stuff'''
            center = self.mask.center
            corners = self.mask.corners

            points_distance = [(corner, round(point_to_line_distance(corner, (center, vec_addition(center, move_vec))), 1)) for corner in corners]
            distances = list(map(lambda x:x[1], points_distance))

            furthest_points = [
                [corner for corner, _ in filter(lambda x: x[1] == max(distances), points_distance)], 
                [corner for corner, _ in filter(lambda x: x[1] == min(distances), points_distance)]
            ] #[0] are +ve, [1] and -ve
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

            for corner in corners:
                distance = point_to_line_distance(corner, new_line)
                if distance > 0 or corner in no_projection_corners:
                    new_mask_corners.append(corner)
                elif distance < 0 and corner:
                    new_mask_corners.append((corner[0] + move_vec[0], corner[1] + move_vec[1]))
                else:
                    if move_vec[1] >= 0:
                        new_mask_corners.append((corner[0] + move_vec[0], corner[1] + move_vec[1]))
                        new_mask_corners.append(corner)
                    else:
                        new_mask_corners.append(corner)
                        new_mask_corners.append((corner[0] + move_vec[0], corner[1] + move_vec[1]))
        
        
        self.mask = Mask(corners=new_mask_corners)