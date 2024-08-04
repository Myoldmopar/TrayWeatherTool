from pathlib import Path
from unittest import mock, TestCase

import requests
import gi
gi.require_version('Gdk', '4.0')
from gi.repository import Gdk  # noqa: E402

from tray_weather.storms import StormType, StormManager  # noqa: E402


class TestStormType(TestCase):
    def test_from_string(self):
        self.assertEqual(StormType.from_string("Flood Watch"), StormType.FloodWatch)
        self.assertEqual(StormType.from_string("Flood Warning"), StormType.FloodWarning)
        self.assertEqual(StormType.from_string("ThunderStorm Watch"), StormType.ThunderStormWatch)
        self.assertEqual(StormType.from_string("ThunderStorm Warning"), StormType.ThunderStormWarning)
        self.assertEqual(StormType.from_string("Tornado Watch"), StormType.TornadoWatch)
        self.assertEqual(StormType.from_string("Tornado Warning"), StormType.TornadoWarning)
        self.assertEqual(StormType.from_string("Who?"), StormType.NoStorm)


class TestStormManager(TestCase):
    def test_construction(self):
        sm = StormManager(23.0, -97)
        self.assertEqual(sm.storm_type, StormType.NoStorm)

    def test_icon_color(self):
        rgba = Gdk.RGBA()
        sm = StormManager(23.0, -97)
        for st in StormType.get_all():
            color = sm.icon_color(st)
            self.assertTrue(rgba.parse(color))

    @mock.patch('requests.get')
    def test_watch_warnings(self, mock_get):
        # Configure the mock to return a response with specific text
        mock_response = mock.Mock()
        mock_response.status_code = 200
        this_file = Path(__file__).resolve()
        resource_file = this_file.parent / 'mock_weather_response.txt'
        mock_response_template = resource_file.read_bytes()
        mock_get.return_value = mock_response
        sm = StormManager(23.0, -97)
        checks = [
            (b"Heat Advisory", StormType.NoStorm),
            (b"Flood Watch", StormType.FloodWatch),
            (b"Flood Warning", StormType.FloodWarning),
            (b"Severe Thunderstorm Watch", StormType.ThunderStormWatch),
            (b"Severe Thunderstorm Warning", StormType.ThunderStormWarning),
            (b"Tornado Watch", StormType.TornadoWatch),
            (b"Tornado Warning", StormType.TornadoWarning),
        ]
        for check in checks:
            print("Checking", check)
            mock_response.content = mock_response_template.replace(b'{REPLACE_ME}', check[0])
            sm.get_watch_warnings(mock_get)
            self.assertEqual(sm.storm_type, check[1])

        mock_response.status_code = 404  # TODO: CHeck more exotic failures
        mock_get.side_effect = requests.exceptions.RequestException("An error occurred")
        sm.storm_type = StormType.FloodWarning
        sm.get_watch_warnings(mock_get)
        self.assertEqual(sm.storm_type, StormType.NoStorm)  # TODO: What else should it do?
