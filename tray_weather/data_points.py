from collections import deque
from datetime import datetime


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
