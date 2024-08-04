import requests
from typing import Callable, Optional
import xml.etree.ElementTree as ElementT


class StormType:
    NoStorm = 0
    FloodWatch = 1
    FloodWarning = 2
    ThunderStormWatch = 3
    TornadoWatch = 4
    ThunderStormWarning = 5
    TornadoWarning = 6

    @staticmethod
    def get_all() -> list[int]:
        return [
            StormType.NoStorm,
            StormType.FloodWatch, StormType.FloodWarning,
            StormType.ThunderStormWatch, StormType.ThunderStormWarning,
            StormType.TornadoWatch, StormType.TornadoWarning
        ]


class StormManager:
    def __init__(self, latitude: float, longitude: float):
        self.storm_type = StormType.NoStorm
        self.latitude = latitude
        self.longitude = longitude

    def icon_color(self, test_type: int | None = None):
        type_to_check = test_type if test_type else self.storm_type
        if type_to_check == StormType.FloodWatch:
            return 'powderblue'
        elif type_to_check == StormType.FloodWarning:
            return 'whitesmoke'  # or deepskyblue
        elif type_to_check == StormType.ThunderStormWatch:
            return 'silver'  # or palegreen
        elif type_to_check == StormType.TornadoWatch:
            return 'lime'
        elif type_to_check == StormType.ThunderStormWarning:
            return 'yellow'
        elif type_to_check == StormType.TornadoWarning:
            # TODO: Issue a one-time message somewhere that gets cleared after one day
            return 'red'
        else:
            return 'orange'

    def get_watch_warnings(self, unit_test_get: Optional[Callable] = None):
        self.storm_type = StormType.NoStorm
        url = f"https://api.weather.gov/alerts/active.atom?point={self.latitude}%2C{self.longitude}"
        try:
            if unit_test_get is None:  # pragma: no cover
                response = requests.get(url)  # not unit testing the actual http request
            else:
                response = unit_test_get(url)
        except requests.exceptions.RequestException as e:
            print("Request failed: {}".format(e))
            return
        root = ElementT.fromstring(response.content.decode("utf-8"))
        found_events = set()
        found_events.add(StormType.NoStorm)
        for item in root:
            if item.tag.endswith('entry'):
                entry = item
                for attribute in entry:
                    if attribute.tag.endswith('event'):
                        if 'Flood Watch' in attribute.text:
                            found_events.add(StormType.FloodWatch)
                        elif 'Flood Warning' in attribute.text:
                            found_events.add(StormType.FloodWarning)
                        elif 'Severe Thunderstorm Watch' in attribute.text:
                            found_events.add(StormType.ThunderStormWatch)
                        elif 'Severe Thunderstorm Warning' in attribute.text:
                            found_events.add(StormType.ThunderStormWarning)
                        elif 'Tornado Watch' in attribute.text:
                            found_events.add(StormType.TornadoWatch)
                        elif 'Tornado Warning' in attribute.text:
                            found_events.add(StormType.TornadoWarning)
                        break
        self.storm_type = max(found_events)
