from panda3d.core import Point3, TextNode, WindowProperties, CardMaker
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, OnscreenText
import subprocess

class MapApp(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class
        super().__init__()

        # Set the window title to "Map Selector"
        window_props = WindowProperties()
        window_props.setTitle("Map Selector")
        self.win.requestProperties(window_props)

        # Set the background color to black
        self.set_background_color(0, 0, 0)

        # Create a tappable horizontal button across the screen
        self.create_map_button()

    def create_map_button(self):
        # Create the tappable button across the screen
        self.map_button = DirectButton(
            frameColor=(0.5, 0.5, 0.5, 1),  # Gray outline
            frameSize=(-1.5, 1.5, -0.2, 0.2),  # Wide horizontal button
            pos=(0, 0, 0),  # Centered horizontally and vertically
            relief=2,  # Raised button style
            command=self.launch_game  # Taps launch the game
        )

        # Inner black box for aesthetics
        self.inner_box = DirectButton(
            frameColor=(0, 0, 0, 1),  # Black inner box
            frameSize=(-1.48, 1.48, -0.18, 0.18),  # Slightly smaller than the outer box
            pos=(0, 0, 0),
            state=0,  # Static element (non-clickable)
            parent=self.map_button
        )

        # Add the placeholder "No image" text inside the button
        self.create_placeholder_image()

        # Add the map name text inside the button
        self.map_text = OnscreenText(
            text="Map_1_Beta_FreshLime",
            fg=(1, 0, 0, 1),  # Red text
            pos=(0.3, 0),  # Slightly right of the center
            scale=0.08,
            align=TextNode.ALeft,
            parent=self.inner_box  # Attach to the inner black box
        )

    def create_placeholder_image(self):
        # Create a gray square placeholder for the image inside the button
        card_maker = CardMaker('placeholder')
        card_maker.setFrame(-0.15, 0.15, -0.15, 0.15)  # Define square dimensions
        placeholder = self.inner_box.attachNewNode(card_maker.generate())
        placeholder.setPos(-0.8, 0, 0)  # Position to the left within the button
        placeholder.setColor(0.5, 0.5, 0.5, 1)  # Gray color

        # Add "No image" text inside the square
        OnscreenText(
            text="No image",
            fg=(0, 0, 0, 1),  # Black text
            pos=(-0.8, 0),  # Centered within the placeholder
            scale=0.05,
            align=TextNode.ACenter,
            parent=self.inner_box  # Attach to the inner black box
        )

    def launch_game(self):
        # Launch the actual game when the button is clicked
        subprocess.Popen(['python3', 'game/main.py'])
        self.quit()

# Create and run the app
app = MapApp()
app.run()
