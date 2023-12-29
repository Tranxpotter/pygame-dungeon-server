from engine.gameObject import GameObject
from engine.collider import Collider

class testObject(GameObject):
    def __init__(self, x: int, y: int, *args, collider: Collider | None = None, **kwargs):
        super().__init__(x, y, *args, collider=collider, **kwargs)
    
    def update(self, dt: float):
        return super().update(dt)
    
    def draw(self, camera_pos: tuple[int, int]):
        return super().draw(camera_pos)

a = testObject(10, 10)