import os
from direct.gui.OnscreenText import OnscreenText  

class HealthDisplay:
    def __init__(self, game):
        self.game = game
        
        
        font_path = 'models/fonts/arial.ttf'
        if os.path.exists(font_path):
            font = self.game.loader.load_font(font_path)
        else:
            
            try:
                font = self.game.loader.load_font('builtin')
            except IOError:
                
                external_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  
                if os.path.exists(external_font_path):
                    font = self.game.loader.load_font(external_font_path)
                else:
                    
                    font = self.game.loader.load_font('arial')

        
        self.health_text = OnscreenText(text="Health: 100", pos=(-1.1, 0.9), scale=0.07, font=font, fg=(1, 1, 1, 1))
        self.pause_text = OnscreenText(text="I//L/O/P/W/A/S/D = Look/Move Buttons", pos=(-1.1, 0.83), scale=0.07, font=font, fg=(1, 1, 1, 1))
        self.hit_text = OnscreenText(text="E = Hit", pos=(-1.1, 0.76), scale=0.07, font=font, fg=(1, 1, 1, 1))
        
       
        self.health = 100

    def update(self):
       
        self.health_text.set_text(f"Health: {self.health}")

    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.update()

    def increase_health(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        self.update()
