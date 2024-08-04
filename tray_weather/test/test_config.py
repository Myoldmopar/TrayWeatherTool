from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase

from tray_weather.config import Configuration
from tray_weather.data_points import DataPointHistoryProps


class TestConfig(TestCase):

    def setUp(self):
        self.temp_dir: Path = Path(mkdtemp())

    def test_construction(self):
        # first construction, config file does not exist yet
        temp_config_file = self.temp_dir / 'tmp.json'
        self.assertFalse(temp_config_file.exists())
        Configuration(temp_config_file)
        self.assertTrue(temp_config_file.exists())
        # next time, file should already exist and be populated with default data
        Configuration(temp_config_file)
        self.assertTrue(temp_config_file.exists())

    def test_temp_history_methods(self):
        temp_config_file = self.temp_dir / 'tmp.json'
        c = Configuration(temp_config_file)
        num_points_to_add = 10
        for i in range(num_points_to_add):
            c.log_data_point(float(i))
        self.assertEqual(len(c.temp_history), num_points_to_add)
        history_data = c.gather_history_properties()
        self.assertIsInstance(history_data, DataPointHistoryProps)
        self.assertEqual(history_data.highest_temp, '9.0')  # 10-1 because of zero based index
        self.assertEqual(history_data.lowest_temp, '0.0')
        self.assertIsInstance(c.temp_history_for_clipboard(), str)
