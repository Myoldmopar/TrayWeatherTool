from collections import deque
from datetime import datetime
from json import dumps, loads
from pathlib import Path

from tray_weather.data_points import DataPoint, DataPointHistoryProps
from tray_weather.location import LocationManager


class Configuration:
    def __init__(self, override_config_file_path: Path | None = None):
        # set defaults here
        self.location = LocationManager()
        self.temp_history: deque[DataPoint] = deque(maxlen=1000)
        self.frequency_minutes = 1
        if override_config_file_path is not None:
            self.config_file = override_config_file_path
        else:  # pragma: no cover
            # not touching the actual home dir file in unit tests, so skipping coverage here
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
        self.temp_history.append(DataPoint().from_values(datetime.now(), temperature))

    def gather_history_properties(self) -> DataPointHistoryProps:
        return DataPointHistoryProps(self.temp_history)

    def temp_history_for_clipboard(self) -> str:
        return '\n'.join(t.to_csv() for t in self.temp_history)
