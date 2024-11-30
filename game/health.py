import os
from direct.gui.OnscreenText import OnscreenText  # Import for displaying text

class HealthDisplay:
    def __init__(self, game):
        self.game = game
        
        # Try loading the arial font from Panda3D's internal fonts
        font_path = 'models/fonts/arial.ttf'
        if os.path.exists(font_path):
            font = self.game.loader.load_font(font_path)
        else:
            # Attempt to use the built-in font if custom font is not found
            try:
                font = self.game.loader.load_font('builtin')
            except IOError:
                # If 'builtin' font is not found, fallback to another external font
                external_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'  # Example path
                if os.path.exists(external_font_path):
                    font = self.game.loader.load_font(external_font_path)
                else:
                    # Finally, load the built-in default font
                    font = self.game.loader.load_font('arial')

        # Create OnscreenText objects for displaying health, instructions, etc.
        self.health_text = OnscreenText(text="Health: 100", pos=(-1.1, 0.9), scale=0.07, font=font, fg=(1, 1, 1, 1))
        self.pause_text = OnscreenText(text="P = Pause", pos=(-1.1, 0.83), scale=0.07, font=font, fg=(1, 1, 1, 1))
        self.hit_text = OnscreenText(text="E = Hit", pos=(-1.1, 0.76), scale=0.07, font=font, fg=(1, 1, 1, 1))
        
        # Initial health value
        self.health = 100

    def update(self):
        # Update the health display
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
