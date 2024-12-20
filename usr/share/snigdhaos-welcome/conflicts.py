import gi
import os

# Ensure the correct GTK version is available
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # Import GTK for creating GUI components

# Get the directory of the current script to handle resource paths
base_dir = os.path.dirname(os.path.realpath(__file__))

class Conflicts(Gtk.Window):
    def __init__(self):
        # Initialize the window with a title and default size
        super(Conflicts, self).__init__(title="Information")
        self.set_border_width(10)  # Add border width for better spacing
        self.set_default_size(550, 250)  # Set default window size
        self.connect("delete-event", self.close)  # Handle window close event
        # Set the window icon from the images folder
        self.set_icon_from_file(os.path.join(base_dir, 'images/snigdhaos-icon.png'))
        self.set_position(Gtk.WindowPosition.CENTER)  # Center the window on the screen

        # Create a vertical box container for organizing the widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)  # Optional: Allow widgets to have different sizes
        self.add(vbox)  # Add the vertical box to the window

        # List of warning messages and titles
        warnings = [
            ("Warning 1", "xcursor-breeze conflicts with breeze"),
            ("Warning 2", "visual-studio-code-bin conflicts with code"),
            ("Warning 3", "synapse (zeitgeist) conflicts with catfish"),
            ("Warning 4", "Either choose libreoffice-fresh or libreoffice-still"),
            ("Warning 5", "Either choose virtualbox for linux or linux-lts"),
            ("Warning 6", "midori (zeitgeist) conflicts with catfish")
        ]

        # Loop through each warning and create UI components dynamically
        for title, message in warnings:
            # Create a header label with bold and italic markup
            header = Gtk.Label(xalign=0)  # Align the header text to the left
            header.set_markup(f"<b><i>{title}</i></b>")
            vbox.pack_start(header, False, False, 0)  # Add header to the vertical box
            
            # Create a message label for each warning
            msg_label = Gtk.Label()
            msg_label.set_text(message)  # Set the message text
            msg_label.set_xalign(0)  # Align the message text to the left
            vbox.pack_start(msg_label, False, False, 0)  # Add message label to the vertical box

        # Add a "Close" button at the bottom of the window
        close_button = Gtk.Button(label="Close")  # Create a button labeled "Close"
        close_button.connect("clicked", self.close)  # Connect the button click to close the window
        vbox.pack_start(close_button, False, False, 0)  # Add the button to the vertical box

    def close(self, widget, event=None):
        # Close the window when the "Close" button is clicked or the window is closed
        self.destroy()

# Main execution block: Runs when the script is executed directly
if __name__ == "__main__":
    # Create an instance of the Conflicts window
    window = Conflicts()
    window.show_all()  # Display all widgets in the window
    Gtk.main()  # Start the GTK event loop to handle user interactions
