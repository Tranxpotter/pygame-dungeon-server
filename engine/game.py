

class Game:
    def __init__(self, max_players:int = 2, config:dict|None = None) -> None:
        self.max_players = max_players
        self.config = config
        self.players = []