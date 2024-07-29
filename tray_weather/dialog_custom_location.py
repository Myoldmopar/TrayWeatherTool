import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, AppIndicator3, GdkPixbuf  # noqa  E402 import not at top of file


class DialogCustomLocation(Gtk.Dialog):

    def __init__(self):
        self.clicked_x = None
        self.clicked_y = None

        # Create a new dialog
        Gtk.Dialog.__init__(self, "Choose a Custom Location", None, 0, Gtk.ButtonsType.OK)

        # Create a box to add to the dialog
        box = self.get_content_area()

        # Load an image from file (replace 'path_to_image.png' with your image file path)
        # not sure why but PyCharm seems to think the new_from_file needs a second argument
        # noinspection PyArgumentList
        image = Gtk.Image.new_from_file("/home/edwin/Pictures/EPlusLogos/original-3d.png")

        # not sure why but PyCharm thinks that an EventBox is not callable
        # noinspection PyCallingNonCallable
        event_box = Gtk.EventBox()
        event_box.add(image)

        # Connect the EventBox to the button-press-event signal
        event_box.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        event_box.connect("button-press-event", self.on_image_click)

        # Add the EventBox (with the image) to the box
        box.add(event_box)

        # Add a label below the image
        label = Gtk.Label(label="This is an image dialog!")
        box.add(label)

        # Show all widgets in the dialog
        self.show_all()

        # Run the dialog and capture the response
        self.run()

        # Destroy the dialog after response
        # TODO: Won't actually want to do this inside here because we'll need to get data from the object
        self.destroy()

    def on_image_click(self, _widget, event):
        self.clicked_x = event.x
        self.clicked_y = event.y
        print(f"Image clicked at coordinates: ({event.x}, {event.y})")
