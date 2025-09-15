from panda3d.core import Point3, TextNode, WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton
from direct.gui.OnscreenText import OnscreenText
import subprocess

class GameApp(ShowBase):
    def __init__(self):
        super().__init__()
        window_props = WindowProperties()
        window_props.setTitle("Fading Echoes.")
        self.win.requestProperties(window_props)
        self.set_background_color(0, 0, 0)

        self.start_button = DirectButton(
            text="Start Game - Endless",
            scale=0.1,
            command=self.launch_map,
            pos=(-1.2, 0, 0.2)
        )

        self.credits_button = DirectButton(
            text="Credits",
            scale=0.1,
            command=self.toggle_credits,
            pos=(-1.2, 0, -0.1)
        )

        self.title_text = OnscreenText(
            text="Fading Echoes.",
            fg=(1, 0, 0, 1),
            pos=(0, 0.6),
            scale=0.15,
            align=TextNode.ACenter
        )

        self.made_by_text = OnscreenText(
            text="Made by Void",
            fg=(1, 1, 1, 1),
            pos=(0, -0.4),
            scale=0.07
        )

        self.credits_visible = False

    def toggle_credits(self):
        if self.credits_visible:
            self.title_text.setText("Fading Echoes.")
            self.title_text.setFg((1, 0, 0, 1))
            self.credits_visible = False
        else:
            self.title_text.setText("Game By: Void\nCoded by: void\nRunning off of Panda3D engine")
            self.title_text.setFg((0.5, 0.5, 0.5, 1))
            self.credits_visible = True

    def launch_map(self):
        subprocess.Popen(['python3', 'map.py'])
        self.quit()

app = GameApp()
app.run()
