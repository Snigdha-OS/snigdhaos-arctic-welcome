import gi

# Required to specify the version of the Gtk library to use
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# Custom class `Stack` inheriting from `Gtk.Stack`
class Stack(Gtk.Stack):
    def __init__(self, transition_type):
        # Call the initializer of the parent class
        super(Stack, self).__init__()

        # Determine the transition type based on the input argument
        # If the input is "ROTATE_LEFT", set it to the corresponding Gtk transition type
        if transition_type == "ROTATE_LEFT":
            transition_type = Gtk.StackTransitionType.ROTATE_LEFT
        
        # If the input is "CROSSFADE", set it to the corresponding Gtk transition type
        if transition_type == "CROSSFADE":
            transition_type = Gtk.StackTransitionType.CROSSFADE

        # Set the stack transition type (animation between stack pages)
        self.set_transition_type(transition_type)
        
        # Allow the widget to expand horizontally to fill available space
        self.set_hexpand(True)
        
        # Allow the widget to expand vertically to fill available space
        self.set_vexpand(True)
        
        # Set the duration of the transition animation in milliseconds
        self.set_transition_duration(500)
        
        # Disable horizontal homogeneity, allowing child widgets to have different widths
        self.set_hhomogeneous(False)
        
        # Disable vertical homogeneity, allowing child widgets to have different heights
        self.set_vhomogeneous(False)
