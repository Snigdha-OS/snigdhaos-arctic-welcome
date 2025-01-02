import gi

# Specify the version of the Gtk library to use
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# Custom class `StackSwitcher` inheriting from `Gtk.StackSwitcher`
class StackSwitcher(Gtk.StackSwitcher):
    def __init__(self, stack):
        # Call the initializer of the parent class
        super(StackSwitcher, self).__init__()
        
        # Set the orientation of the switcher to horizontal
        # This means the buttons to switch between stack pages will be laid out side by side
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        # Link the `StackSwitcher` to a specific `Gtk.Stack` instance
        # This allows the switcher to control and reflect the state of the given stack
        self.set_stack(stack)
        
        # Align the switcher horizontally to the center of its parent container
        self.set_halign(Gtk.Align.CENTER)
