import requests
import xml.etree.ElementTree as ElementT


class StormType:
    NoStorm = 0
    FloodWatch = 1
    FloodWarning = 2
    ThunderStormWatch = 3
    TornadoWatch = 4
    ThunderStormWarning = 5
    TornadoWarning = 6


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

    def get_watch_warnings(self):
        self.storm_type = StormType.NoStorm
        url = f"https://api.weather.gov/alerts/active.atom?point={self.latitude}%2C{self.longitude}"
        try:
            response = requests.get(url)
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
                        elif 'Thunderstorm Warning' in attribute.text:
                            found_events.add(StormType.TornadoWarning)
                        break
        self.storm_type = max(found_events)


if __name__ == '__main__':
    lat = 35.15
    long = -98.47
    s = StormManager(lat, long)
    s.get_watch_warnings()
