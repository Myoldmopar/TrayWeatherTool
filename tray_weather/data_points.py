from collections import deque
from datetime import datetime

from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


class DataPoint:
    def __init__(self):
        self.time_stamp: datetime | None = None
        self.temperature: float | None = None

    def from_values(self, time_stamp: datetime, temperature: float) -> 'DataPoint':
        self.time_stamp = time_stamp
        self.temperature = temperature
        return self

    def from_dict(self, dictionary: dict) -> 'DataPoint':
        self.time_stamp = datetime.strptime(dictionary['time_stamp'], '%Y-%m-%d %H:%M:%S')
        self.temperature = dictionary['temperature']
        return self

    def to_dict(self) -> dict:
        return {
            'time_stamp': self.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': self.temperature
        }

    def to_csv(self) -> str:
        s_time_stamp = self.time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'{s_time_stamp},{self.temperature}'


class DataPointHistoryProps:
    def __init__(self, temp_history: deque[DataPoint]):
        if len(temp_history) == 0:
            self.oldest_time = "*Oldest*"
            self.newest_time = "*Newest*"
            self.lowest_temp = "*Lowest*"
            self.highest_temp = "*Highest*"
            return
        self.oldest_time = temp_history[0].time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        self.newest_time = temp_history[-1].time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        lowest_temp = 9999
        highest_temp = -9999
        for t in temp_history:
            if t.temperature < lowest_temp:
                lowest_temp = t.temperature
            if t.temperature > highest_temp:
                highest_temp = t.temperature
        self.lowest_temp = str(round(lowest_temp, 2))
        self.highest_temp = str(round(highest_temp, 2))

    @staticmethod
    def get_history_plot_data(temp_history: deque[DataPoint]) -> tuple:
        time_stamps = []
        temperatures = []
        for x in temp_history:
            if x.temperature > -50:  # only take valid data points
                time_stamps.append(x.time_stamp)
                temperatures.append(x.temperature)
        min_temp, max_temp = None, None
        if len(temp_history) > 1:
            min_temp = min(temperatures)
            max_temp = max(temperatures)
        return time_stamps, temperatures, min_temp, max_temp

    @staticmethod
    def get_history_plot(temp_history: deque[DataPoint]) -> FigureCanvas:  # pragma: no cover
        # build out a matplotlib Figure instance to store the plotting
        figure = Figure(figsize=(5, 4), dpi=100)
        figure.subplots_adjust(top=0.96, right=0.96)
        figure.set_facecolor('orange')
        ax = figure.add_subplot(111)
        time_stamps, temperatures, min_temp, max_temp = DataPointHistoryProps.get_history_plot_data(temp_history)
        # noinspection PyTypeChecker
        ax.plot(time_stamps, temperatures, linestyle='-', color='orange', lw=2)
        figure.autofmt_xdate()
        ax.grid()
        ax.set_xlim([time_stamps[0], time_stamps[-1]])
        ax.set_ylim([-15, 115])
        ax.xaxis.set_major_formatter(DateFormatter('%y-%m-%d %H:%M'))
        ax.set_ylabel('Recorded Temperature (°F)')
        if min_temp and max_temp:
            s_min_temp = str(round(min_temp, 2))
            s_max_temp = str(round(max_temp, 2))
            time_range = time_stamps[-1] - time_stamps[0]
            x_label_offset = time_range / 40
            x_label_point = time_stamps[0] + x_label_offset
            # noinspection PyTypeChecker
            ax.text(x_label_point, 2, f"Max Temp: {s_max_temp} °F", fontsize=14, color='black')
            # noinspection PyTypeChecker
            ax.text(x_label_point, -7, f"Min Temp: {s_min_temp} °F", fontsize=14, color='black')
        canvas = FigureCanvas(figure)
        canvas.set_size_request(780, 450)
        return canvas
