from GUI_Controller.Agent import Agent
from GUI_Controller.Player import Player

class PlayerFactory:
    def __init__(self, color: str, human: bool):
        self.color = color
        self.human = human
    
    def create_player(self, sound, solver = None):
        if self.human:
            return Player(self.color, sound)
        else:
            if not solver:
                raise ValueError("Solver is required for creating agent")
            return Agent(self.color, sound, solver)