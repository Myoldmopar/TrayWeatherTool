import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402

from tray_weather.solar import SolarDataManager  # noqa: E402


class DialogSolarPlot(Gtk.Dialog):

    def __init__(self, *_):
        sdm = SolarDataManager()
        title = f"Solar Position Throughout the Day on {sdm.now.strftime('%Y-%m-%d')}"
        Gtk.Dialog.__init__(self, title, None, 0, Gtk.ButtonsType.OK)
        box = self.get_content_area()
        box.add(sdm.get_canvas())
        self.show_all()
        self.run()
        self.destroy()


def show_solar_plot(*_):
    DialogSolarPlot()
