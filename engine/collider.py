from typing import Callable

from .gameObject import GameObject
from .mask import Mask


class Collider():
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
        check_collided(self, obj):
            Checks if the object is in the collided list
    '''

    def __init__(self,
                 heights: list[int],
                 mask: Mask,
                 on_collide: Callable[[GameObject],
                                      None]):
        self.heights = heights
        self.mask = mask
        self.collided: list[GameObject] = []
        self.on_collide = on_collide

    def check_collided(self, obj) -> bool:
        '''Returns True if the object is in the collided list, otherwise, return False and add the object to the collided list\n
        If class does not require special collided checking, simply write `return super().check_collided(obj)`
        '''
        if obj in self.collided:
            return True
        self.collided.append(obj)
        return False
