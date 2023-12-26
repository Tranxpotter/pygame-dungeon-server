from typing import Literal

from .gameObject import GameObject
from .weapon import AbstractWeapon

class Player(GameObject):
    def __init__(self, 
                 player_name:str, 
                 x:int, 
                 y:int, 
                 weapon:AbstractWeapon, 
                 skills, 
                 max_hp:int, 
                 attack:int,
                 defence:int,
                 accuracy:int,
                 evade:int,
                 speed:int,
                 crit_rate:float,
                 crit_bonus:float
                 ):
        self.player_name = player_name
        self.x = x
        self.y = y
        
        self.weapon = weapon
        self.skills = skills

        self.max_hp = max_hp
        self.attack = attack
        self.defence = defence
        self.accuracy = accuracy
        self.evade = evade
        self.speed = speed
        self.crit_rate = crit_rate
        self.crit_bonus = crit_bonus

        self.stat_changes = {
            "max_hp":[],
            "attack":[],
            "defence":[],
            "accuracy":[],
            "evade":[],
            "speed":[],
            "crit_rate":[],
            "crit_damage":[]
        }

    
    def update(self, dt: float):
        return super().update(dt)

        
    def draw(self, camera_pos: tuple[int, int]):
        return super().draw(camera_pos)
    
    

