from abc import ABC, abstractmethod
class AbstractWeapon(ABC):
    @abstractmethod
    def __init__(self, name:str, description:str, level:int, enchantments:dict, cooldown:float, *args, **kwargs) -> None:
        self.name = name
        self.description = description
        self.level = level
        self.enchantments = enchantments
        self.cooldown = cooldown
        self.current_cooldown:float = 0
    
    @abstractmethod
    def on_attack(self, angle:float):...

    @abstractmethod
    def on_equip(self):...

    @abstractmethod
    def on_unequip(self):...

    @abstractmethod
    def on_levelup(self):...

    @abstractmethod
    def on_enchant(self, enchantment:dict):...

class RangedWeapon(AbstractWeapon):
    ...
    
    