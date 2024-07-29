from datetime import datetime, timedelta
from time import localtime

from matplotlib.dates import HourLocator, DateFormatter, MinuteLocator
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402

from solar_angles.solar import Angular, altitude_angle  # noqa: E402


class DialogSolarPlot(Gtk.Dialog):

    def __init__(self):
        self.now = datetime.now()
        title = f"Solar Position Throughout the Day on {self.now.strftime('%Y-%m-%d')}"
        Gtk.Dialog.__init__(self, title, None, 0, Gtk.ButtonsType.OK)

        # get the current time and find today at midnight as well
        this_morning_midnight = datetime(self.now.year, self.now.month, self.now.day, 0, 0, 0)
        this_morning_1210 = datetime(self.now.year, self.now.month, self.now.day, 0, 10, 0)
        tomorrow_midnight = datetime(self.now.year, self.now.month, self.now.day + 1, 0, 0, 0)

        # loop over the day gathering altitudes and finding sunrise/sunset
        alphas: list[float] = []
        time_stamps: list[datetime] = []
        longitude = Angular(degrees=-97.6787)
        standard_meridian = Angular(degrees=-105)
        latitude = Angular(degrees=35.7981)
        sunrise_time: str = ''
        sunset_time: str = ''
        time_step_minutes = 10
        this_time_stamp = this_morning_midnight
        dst = localtime().tm_isdst != 0
        while this_time_stamp.day == this_morning_midnight.day:
            time_stamps.append(this_time_stamp)
            alpha = altitude_angle(this_time_stamp, dst, longitude, standard_meridian, latitude)
            alphas.append(alpha.degrees)
            if not sunrise_time and alpha.degrees > 0:
                slope_deg_per_minute = (alphas[-1] - alphas[-2]) / time_step_minutes
                minutes_to_zero_since_time_stamp = - alphas[-2] / slope_deg_per_minute
                previous_time_stamp = this_time_stamp - timedelta(minutes=time_step_minutes)
                sunrise_time_stamp = previous_time_stamp + timedelta(minutes=minutes_to_zero_since_time_stamp)
                sunrise_time = sunrise_time_stamp.strftime('%H:%M')
            elif sunrise_time and not sunset_time and alpha.degrees < 0:
                slope_deg_per_minute = (alphas[-1] - alphas[-2]) / time_step_minutes
                minutes_to_zero_since_time_stamp = - alphas[-2] / slope_deg_per_minute
                previous_time_stamp = this_time_stamp - timedelta(minutes=time_step_minutes)
                sunset_time_stamp = previous_time_stamp + timedelta(minutes=minutes_to_zero_since_time_stamp)
                sunset_time = sunset_time_stamp.strftime('%H:%M')
            this_time_stamp += timedelta(minutes=time_step_minutes)

        # get the current altitude angle as of right now as well
        now_altitude = altitude_angle(self.now, dst, longitude, standard_meridian, latitude)

        # build out a matplotlib Figure instance to store the plotting
        figure = Figure(figsize=(5, 4), dpi=100)
        figure.subplots_adjust(top=0.96, right=0.96)
        figure.set_facecolor('orange')
        ax = figure.add_subplot(111)
        # For some reason, PyCharm does not like the datetime args passed as x values, but they work, so ignoring...
        # noinspection PyTypeChecker
        ax.plot(time_stamps, alphas, linestyle='-', color='orange', lw=2)
        # noinspection PyTypeChecker
        ax.plot([self.now], [now_altitude.degrees], marker='o', color='black', label="Current Position")
        figure.autofmt_xdate()
        ax.grid()
        ax.xaxis.set_major_locator(HourLocator(interval=2))
        ax.xaxis.set_minor_locator(MinuteLocator(interval=30))  # Minor ticks every 15 minutes
        ax.set_xlim([this_morning_midnight, tomorrow_midnight])
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax.set_ylabel('Solar Altitude Angle (deg)')
        # noinspection PyTypeChecker
        ax.hlines(y=0, xmin=this_morning_midnight, xmax=tomorrow_midnight, colors='black', linestyles='-', lw=2)
        # noinspection PyTypeChecker
        ax.text(this_morning_1210, 2, f"Sunrise at {sunrise_time}", fontsize=14, color='black')
        # noinspection PyTypeChecker
        ax.text(this_morning_1210, -7, f"Sunset at {sunset_time}", fontsize=14, color='black')
        ax.legend()
        canvas = FigureCanvas(figure)
        canvas.set_size_request(780, 450)

        # get our content box and add the figure
        box = self.get_content_area()
        box.add(canvas)
        self.show_all()
        self.run()
        self.destroy()


def show_solar_plot(*_):
    DialogSolarPlot()
