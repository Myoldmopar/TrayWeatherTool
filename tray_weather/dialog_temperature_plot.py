from collections import deque
from datetime import datetime

from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402

from tray_weather.config import DataPoint  # noqa: E402


class DialogTemperaturePlot(Gtk.Dialog):

    def __init__(self, temp_history: deque[DataPoint]):
        title = "Recorded Temperature History"
        Gtk.Dialog.__init__(self, title, None, 0, Gtk.ButtonsType.OK)

        # build out a matplotlib Figure instance to store the plotting
        figure = Figure(figsize=(5, 4), dpi=100)
        figure.subplots_adjust(top=0.96, right=0.96)
        figure.set_facecolor('orange')
        ax = figure.add_subplot(111)
        # For some reason, PyCharm does not like the datetime args passed as x values, but they work, so ignoring...
        time_stamps = [x.time_stamp for x in temp_history]
        temperatures = [x.temperature for x in temp_history]
        # noinspection PyTypeChecker
        ax.plot(time_stamps, temperatures, linestyle='-', color='orange', lw=2)
        figure.autofmt_xdate()
        ax.grid()
        ax.set_xlim([time_stamps[0], time_stamps[-1]])
        ax.set_ylim([-15, 115])
        ax.xaxis.set_major_formatter(DateFormatter('%y-%m-%d %H:%M'))
        ax.set_ylabel('Recorded Temperature (F)')
        if len(temp_history) > 1:
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            time_range = time_stamps[-1] - time_stamps[0]
            x_label_offset = time_range / 40
            x_label_point = time_stamps[0] + x_label_offset
            # noinspection PyTypeChecker
            ax.text(x_label_point, 2, f"Max Temp: {max_temp}", fontsize=14, color='black')
            # noinspection PyTypeChecker
            ax.text(x_label_point, -7, f"Min at {min_temp}", fontsize=14, color='black')
        canvas = FigureCanvas(figure)
        canvas.set_size_request(780, 450)

        # get our content box and add the figure
        box = self.get_content_area()
        box.add(canvas)
        self.show_all()
        self.run()
        self.destroy()


if __name__ == "__main__":
    fake_data = deque()
    fake_data.append(DataPoint(datetime(2024, 8, 2, 1, 0, 0), 23))
    fake_data.append(DataPoint(datetime(2024, 8, 2, 2, 0, 0), 28))
    fake_data.append(DataPoint(datetime(2024, 8, 2, 3, 0, 0), 41))
    fake_data.append(DataPoint(datetime(2024, 8, 2, 4, 0, 0), 102))
    fake_data.append(DataPoint(datetime(2024, 8, 2, 4, 30, 0), -10))
    fake_data.append(DataPoint(datetime(2024, 8, 2, 5, 0, 0), 87))
    DialogTemperaturePlot(fake_data)
