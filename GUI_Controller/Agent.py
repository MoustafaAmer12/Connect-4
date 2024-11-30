from GUI_Controller.Side import Side

class Agent(Side):
    def __init__(self, color, sound, solver):
        super().__init__(color, sound)
        self.solver = solver