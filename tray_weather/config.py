from collections import deque
from datetime import datetime
from json import dumps, loads
from pathlib import Path
from tray_weather.misc import mesonet_locations


class DataPoint:
    def __init__(self, time_stamp: datetime, temperature: float):
        self.time_stamp = time_stamp
        self.temperature = temperature

    def from_dict(self, dictionary: dict):
        self.time_stamp = dictionary['time_stamp'].strptime('%Y-%m-%d %H:%M:%S')
        self.temperature = dictionary['temperature']

    def to_dict(self) -> dict:
        return {
            'time_stamp': self.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': self.temperature
        }

    def to_csv(self) -> str:
        return f'{self.time_stamp.strftime('%Y-%m-%d %H:%M:%S')},{self.temperature}'


class Location:
    def __init__(self):
        self.is_custom = False
        self.predefined_index = 99
        self.custom_latitude = -99.99
        self.custom_longitude = -99.99
        self.north_east_index = -1
        self.north_west_index = -1
        self.south_west_index = -1
        self.south_east_index = -1

    def set_from_config(self, config: dict):
        self.is_custom = config.get('is_custom', False)
        self.predefined_index = config.get('predefined_index', 99)
        self.custom_latitude = config.get('custom_latitude', -99.99)
        self.custom_longitude = config.get('custom_longitude', -99.99)
        self.north_east_index = config.get('north_east_index', -1)
        self.north_west_index = config.get('north_west_index', -1)
        self.south_west_index = config.get('south_west_index', -1)
        self.south_east_index = config.get('south_east_index', -1)

    def set_from_predefined_index(self, index: int):
        self.is_custom = False
        self.predefined_index = index

    def set_from_custom_location(self, longitude: float, latitude: float):
        self.is_custom = True
        self.custom_latitude = latitude
        self.custom_longitude = longitude
        # set neighboring location indices

    def to_dict(self):
        config = dict()
        config['is_custom'] = self.is_custom
        config['predefined_index'] = self.predefined_index
        config['custom_latitude'] = self.custom_latitude
        config['custom_longitude'] = self.custom_longitude
        config['north_east_index'] = self.north_east_index
        config['north_west_index'] = self.north_west_index
        config['south_west_index'] = self.south_west_index
        config['south_east_index'] = self.south_east_index
        return config

    def get_name(self) -> str:
        if self.is_custom:
            return f"Custom Location ({self.custom_longitude}°W, {self.custom_latitude}°N)"
        else:
            return mesonet_locations[self.predefined_index].name

    def get_custom_names_ne_nw_sw_se(self) -> tuple[str, str, str, str]:
        if not self.is_custom:
            raise RuntimeError("Why did you call get_custom_names for a non custom location!?")
        return (
            mesonet_locations[self.north_east_index].name,
            mesonet_locations[self.north_west_index].name,
            mesonet_locations[self.south_west_index].name,
            mesonet_locations[self.south_east_index].name
        )

    def get_latitude_longitude(self) -> tuple[float, float]:
        if self.is_custom:
            return self.custom_latitude, self.custom_longitude
        else:
            location_item = mesonet_locations[self.predefined_index]
            return location_item.latitude, location_item.longitude


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


class Configuration:
    def __init__(self):
        # set defaults here
        self.location = Location()
        self.temp_history: deque[DataPoint] = deque(maxlen=1000)
        self.frequency_minutes = 1
        self.config_file = Path.home() / ".tray_weather.json"
        if self.config_file.exists():
            with self.config_file.open() as f:
                contents = loads(f.read())
            self.location.set_from_config(contents['location'])
        else:
            self.save_to_file()

    def save_to_file(self):
        config = dict()
        config['location'] = self.location.to_dict()
        config['temp_history'] = [x.to_dict() for x in self.temp_history]
        config['frequency_minutes'] = self.frequency_minutes
        with self.config_file.open('w') as f:
            f.write(dumps(config))

    def log_data_point(self, temperature: float):
        self.temp_history.append(DataPoint(datetime.now(), temperature))

    def gather_history_properties(self) -> DataPointHistoryProps:
        return DataPointHistoryProps(self.temp_history)

    def temp_history_for_clipboard(self) -> str:
        return '\n'.join(t.to_csv() for t in self.temp_history)
