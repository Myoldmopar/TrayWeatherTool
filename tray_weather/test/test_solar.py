from datetime import datetime
from unittest import TestCase

from tray_weather.solar import SolarDataManager


class TestSolar(TestCase):
    def test_solar_plot_data(self):
        sdm = SolarDataManager()
        self.assertIsInstance(sdm.time_stamps[0], datetime)
        self.assertIsInstance(sdm.alphas[0], float)
