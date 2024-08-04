from collections import deque

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402

from tray_weather.config import DataPoint, DataPointHistoryProps  # noqa: E402


class DialogTemperaturePlot(Gtk.Dialog):

    def __init__(self, temp_history: deque[DataPoint]):
        title = "Recorded Temperature History"
        Gtk.Dialog.__init__(self, title, None, 0, Gtk.ButtonsType.OK)
        canvas = DataPointHistoryProps.get_history_plot(temp_history)
        box = self.get_content_area()
        box.add(canvas)
        self.show_all()
        self.run()
        self.destroy()
