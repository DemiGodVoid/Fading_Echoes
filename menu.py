from panda3d.core import Point3, TextNode, WindowProperties  # Import WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
import subprocess

class GameApp(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class
        super().__init__()

        # Set the window title to "GHOSTS OF WAR"
        window_props = WindowProperties()
        window_props.setTitle("GHOSTS OF WAR")
        self.win.requestProperties(window_props)

        # Set the background color to black
        self.set_background_color(0, 0, 0)

        # Create a "Start Game" button to run map.py
        self.start_button = DirectButton(
            text="Start Game",
            scale=0.1,
            command=self.launch_map,
            pos=(-1.2, 0, 0.2)
        )

        # Create a "Credits" button below the "Start Game" button
        self.credits_button = DirectButton(
            text="Credits",
            scale=0.1,
            command=self.toggle_credits,
            pos=(-1.2, 0, -0.1)
        )

        # Add text in the center of the screen with a creepy style
        self.title_text = OnscreenText(
            text="Ghosts Of War",
            fg=(1, 0, 0, 1),
            pos=(0, 0.6),
            scale=0.15,
            align=TextNode.ACenter
        )

        # Add text at the bottom of the screen
        self.made_by_text = OnscreenText(
            text="Made by Jokas",
            fg=(1, 1, 1, 1),
            pos=(0, -0.4),
            scale=0.07
        )

        # Track whether credits are visible
        self.credits_visible = False

    def toggle_credits(self):
        # Toggle visibility of the credits text
        if self.credits_visible:
            self.title_text.setText("Ghosts Of War")
            self.title_text.setFg((1, 0, 0, 1))
            self.credits_visible = False
        else:
            self.title_text.setText("Game By: Jokas\nCoded by: void\nRunning off of Panda3D engine")
            self.title_text.setFg((0.5, 0.5, 0.5, 1))
            self.credits_visible = True

    def launch_map(self):
        # Launch map.py when "Start Game" is clicked
        subprocess.Popen(['python3', 'map.py'])
        self.quit()

# Create and run the app
app = GameApp()
app.run()
