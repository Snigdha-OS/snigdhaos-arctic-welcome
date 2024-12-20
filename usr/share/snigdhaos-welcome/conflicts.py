import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

base_dir = os.path.dirname(os.path.realpath(__file__))

class Conflicts(Gtk.Window):
    def __init__(self):
        super(Conflicts, self).__init__(title="Information")
        self.set_border_width(10)
        self.set_default_size(550, 250)
        self.connect("delete-event", self.close)
        self.set_icon_from_file(os.path.join(base_dir, 'images/snigdhaos-icon.png'))
        self.set_position(Gtk.WindowPosition.CENTER)

        # Vertical box to hold all UI elements
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)  # Optional: Allow different sized widgets
        self.add(vbox)

        # List of conflicts and messages
        warnings = [
            ("Warning 1", "xcursor-breeze conflicts with breeze"),
            ("Warning 2", "visual-studio-code-bin conflicts with code"),
            ("Warning 3", "synapse (zeitgeist) conflicts with catfish"),
            ("Warning 4", "Either choose libreoffice-fresh or libreoffice-still"),
            ("Warning 5", "Either choose virtualbox for linux or linux-lts"),
            ("Warning 6", "midori (zeitgeist) conflicts with catfish")
        ]

        # Iterate through warnings to dynamically add them to the UI
        for title, message in warnings:
            # Create and style header label with markup
            header = Gtk.Label(xalign=0)
            header.set_markup(f"<b><i>{title}</i></b>")
            vbox.pack_start(header, False, False, 0)
            
            # Create message label
            msg_label = Gtk.Label()
            msg_label.set_text(message)
            msg_label.set_xalign(0)  # Align the text to the left
            vbox.pack_start(msg_label, False, False, 0)

        # Add a close button at the bottom of the window
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", self.close)
        vbox.pack_start(close_button, False, False, 0)

    def close(self, widget, event=None):
        # Close the window when the close button is clicked
        self.destroy()

# Run the application
if __name__ == "__main__":
    window = Conflicts()
    window.show_all()
    Gtk.main()
