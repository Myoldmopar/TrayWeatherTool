from collections import deque
from datetime import datetime
from unittest import TestCase

from tray_weather.data_points import DataPoint, DataPointHistoryProps


class TestDataPoints(TestCase):
    def test_default_construction(self):
        # default construction should yield None
        d = DataPoint()
        self.assertIsNone(d.time_stamp)
        self.assertIsNone(d.temperature)

    def test_proper_construction(self):
        d = DataPoint()
        d.from_values(datetime.now(), 23)
        self.assertIsInstance(d.time_stamp, datetime)
        self.assertIsInstance(d.temperature, (float, int))  # can we just check if it is "numeric"?
        d2 = DataPoint()
        d2.from_dict({'time_stamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'temperature': 23})
        self.assertEqual(d.temperature, d2.temperature)

    def test_export_to_dict(self):
        d = DataPoint()
        d.from_values(datetime.now(), 23)
        out = d.to_dict()
        self.assertIsInstance(out, dict)
        self.assertIn('time_stamp', out)
        self.assertIn('temperature', out)


class TestDataPointHistory(TestCase):
    def test_empty_data(self):
        fake_data = deque()
        dph_empty = DataPointHistoryProps(fake_data)
        self.assertIn('*', dph_empty.highest_temp)

    def test_populated_data(self):
        fake_data = deque()
        hours = [1, 2, 3, 4, 4, 5]
        minutes = [0, 0, 0, 0, 30, 0]
        temps = [23, 28, 41, 102, -10, 87]
        for h, m, t in zip(hours, minutes, temps):
            fake_data.append(DataPoint().from_values(datetime(2024, 8, 2, h, m, 0), t))
        dph = DataPointHistoryProps(fake_data)
        self.assertIn('102', dph.highest_temp)
