from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
import os
import subprocess

class GameApp(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class
        super().__init__()

        # Set the background color to black
        self.set_background_color(0, 0, 0)

        # Create a button in the center of the screen
        self.start_button = DirectButton(
            text="Start Game",
            scale=0.1,
            command=self.start_game,
            pos=(0, 0, 0)  # Position the button in the center
        )

        # Add text at the bottom of the screen
        self.made_by_text = OnscreenText(
            text="Made by Jokas",
            fg=(1, 1, 1, 1),  # White color
            pos=(0, -0.4),  # Positioning the text at the bottom
            scale=0.07
        )

    def start_game(self):
        # When the button is clicked, execute main.py and quit the current app
        subprocess.Popen(['python', 'game/main.py'])
        self.quit()

# Create and run the app
app = GameApp()
app.run()
