from panda3d.core import WindowProperties
from direct.task import Task
from direct.gui.DirectGui import DirectButton

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.is_paused = False
        self.quit_button = None
        self.create_pause_menu()

        # Bind the 'P' key to toggle pause
        self.game.accept('p', self.toggle_pause)

        # Store a reference to the main update task
        self.main_update_task = None

    def create_pause_menu(self):
        """Create the pause menu with the 'Quit Game' button."""
        # Create the button for "Quit Game", 10x larger than before
        self.quit_button = DirectButton(
            text="Quit Game", 
            scale=1.0,  # Make the button 10x bigger (from 0.1 to 1.0)
            pos=(0, 0, 0),  # Center the button
            command=self.quit_game, 
            relief=None
        )
        
        # Set the button's background color to dark gray
        self.quit_button.set_color(0.2, 0.2, 0.2, 1)  # Dark gray background
        self.quit_button['text_fg'] = (1, 1, 1, 1)  # White text color
        self.quit_button['text_scale'] = 0.2  # Adjust text size for larger button

        # Initially hide the pause menu
        self.quit_button.hide()

    def toggle_pause(self):
        """Toggle between pause and play mode."""
        if not self.is_paused:
            self.show_pause_menu()
            # Add the pause menu update task and store the reference
            self.game.task_mgr.add(self.pause_update, "pause_update")
            # Stop the main update task (freeze movement)
            if self.main_update_task:
                self.game.task_mgr.remove(self.main_update_task)
            self.is_paused = True
            print("Game Paused")
        else:
            self.hide_pause_menu()
            # Restart update task
            self.main_update_task = self.game.task_mgr.add(self.game.update, "game_update")
            # Remove the pause update task
            self.game.task_mgr.remove("pause_update")
            self.is_paused = False
            print("Game Resumed")

    def show_pause_menu(self):
        """Show the pause menu and unlock the cursor."""
        print("Showing pause menu...")
        # Display the quit button
        self.quit_button.show()

        # Hide the cursor when pausing the game
        props = WindowProperties()
        props.set_cursor_hidden(True)  # Hide cursor
        self.game.win.request_properties(props)

    def hide_pause_menu(self):
        """Hide the pause menu and lock the cursor back to center."""
        print("Hiding pause menu...")
        # Hide the quit button
        self.quit_button.hide()

        # Show the cursor when resuming the game
        props = WindowProperties()
        props.set_cursor_hidden(False)  # Show cursor
        self.game.win.request_properties(props)

    def pause_update(self, task):
        """Update the pause menu while paused."""
        return Task.cont  # This should now work without error

    def quit_game(self):
        """Quit the game when the quit button is pressed."""
        print("Quitting game...")
        self.game.userExit()
