from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, Gdk, AppIndicator3, GdkPixbuf  # noqa:  E402 import not at top of file

from tray_weather.location import mesonet_locations  # noqa: E402


class DialogCustomLocation(Gtk.Dialog):

    def __init__(self):
        self.clicked_x = None
        self.clicked_y = None

        self.image_width = 800
        self.image_height = 464
        self.top_left_longitude = -103.0896
        self.top_left_latitude = 37.38407
        self.bottom_right_longitude = -94.218457
        self.bottom_right_latitude = 33.44352
        self.delta_longitude = self.bottom_right_longitude - self.top_left_longitude
        self.delta_latitude = self.bottom_right_latitude - self.top_left_latitude
        self.boundary_color = (255, 101, 0)
        self.custom_location: tuple[float, float] | None = None

        # Create a new dialog
        Gtk.Dialog.__init__(self, "Choose a Custom Location", modal=True)

        # Create a box to add to the dialog
        box = self.get_content_area()

        # Load an image from file (replace 'path_to_image.png' with your image file path)
        # not sure why but PyCharm seems to think the new_from_file needs a second argument
        package_root = Path(__file__).resolve().parent
        oklahoma_image = str(package_root / 'oklahoma.png')
        # noinspection PyArgumentList

        # image = Gtk.Image.new_from_file(oklahoma_image)
        self.pixel_buffer = GdkPixbuf.Pixbuf.new_from_file(oklahoma_image)
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(self.pixel_buffer.get_width(), self.pixel_buffer.get_height())
        self.drawing_area.connect("draw", self.on_draw)

        # not sure why but PyCharm thinks that an EventBox is not callable
        # noinspection PyCallingNonCallable
        event_box = Gtk.EventBox()
        event_box.add(self.drawing_area)

        # Connect the EventBox to the button-press-event signal
        event_box.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        event_box.connect("button-press-event", self.on_image_click)

        # Add the EventBox (with the image) to the box
        box.add(event_box)

        # Add a label below the image
        self.label = Gtk.Label(label="Click at a custom location!")
        box.add(self.label)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_ok = Gtk.Button().new_with_label("OK")
        self.button_ok.set_sensitive(False)
        button_cancel = Gtk.Button().new_with_label("Cancel")
        button_box.add(self.button_ok)
        button_box.add(button_cancel)
        box.pack_start(button_box, True, True, 0)

        # Connect the buttons to their respective actions
        self.button_ok.connect("clicked", self.on_ok)
        button_cancel.connect("clicked", self.on_cancel)

        # Show all widgets in the dialog
        self.show_all()

        # Run the dialog and capture the response
        self.run()

    def on_ok(self, _button):
        self.close()  # nothing to do now, I think

    def on_cancel(self, _button):
        self.custom_location = None
        self.close()

    def on_draw(self, _widget, cr):
        Gdk.cairo_set_source_pixbuf(cr, self.pixel_buffer, 0, 0)
        cr.paint()
        cr.set_source_rgb(0, 0, 0)
        for location in mesonet_locations:
            long = location.longitude
            lat = location.latitude
            x_pixel, y_pixel = self.pixel_x_y_from_long_lat(long, lat)
            # print(f"Drawing mesonet location at {x_pixel}, {y_pixel}")
            cr.arc(x_pixel, y_pixel, 3, 0, 2 * 3.14)  # Draw a dot with radius 5
            cr.fill()

    def long_lat_from_pixel_x_y(self, x: int, y: int) -> tuple[float, float]:
        longitude_slope = self.delta_longitude / self.image_width
        latitude_slope = self.delta_latitude / self.image_height
        longitude = longitude_slope * x + self.top_left_longitude
        latitude = latitude_slope * y + self.top_left_latitude
        return longitude, latitude

    def pixel_x_y_from_long_lat(self, longitude: int, latitude: int) -> tuple[int, int]:
        x_value_slope = self.image_width / self.delta_longitude
        y_value_slope = self.image_height / self.delta_latitude
        x = int(x_value_slope * (longitude - self.top_left_longitude) + 0)
        y = int(y_value_slope * (latitude - self.top_left_latitude) + 0)
        return x, y

    def on_image_click(self, _widget, event):
        self.clicked_x = event.x
        self.clicked_y = event.y
        longitude, latitude = self.long_lat_from_pixel_x_y(event.x, event.y)
        color = self.get_pixel_color(event.x, event.y)
        if color == self.boundary_color:
            self.label.set_label("Clicked outside the boundary, no can do!")
            self.button_ok.set_sensitive(False)
            self.custom_location = None
        else:
            self.label.set_label(f"Custom Location: longitude/latitude: ({round(longitude, 4)}, {round(latitude, 4)})")
            self.button_ok.set_sensitive(True)
            self.custom_location = (longitude, latitude)

    def get_pixel_color(self, x, y):
        # Ensure the coordinates are within the image boundaries
        if x < 0 or x >= self.pixel_buffer.get_width() or y < 0 or y >= self.pixel_buffer.get_height():
            raise ValueError("Coordinates are out of image bounds")

        # Get pixel data
        pixels = self.pixel_buffer.get_pixels()
        row_stride = self.pixel_buffer.get_rowstride()
        n_channels = self.pixel_buffer.get_n_channels()

        # Calculate the offset for the specified pixel
        int_x = int(x)
        int_y = int(y)
        offset = int_y * row_stride + int_x * n_channels

        # Extract color values
        red = pixels[offset]
        green = pixels[offset + 1]
        blue = pixels[offset + 2]

        return red, green, blue
