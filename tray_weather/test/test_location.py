from pathlib import Path
from unittest import mock, TestCase

from tray_weather.location import MesonetLocation, LocationManager


class TestLocation(TestCase):

    @mock.patch('requests.get')
    def test_get_current_mesonet_data(self, mock_get):
        # Configure the mock to return a response with specific text
        mock_response = mock.Mock()
        mock_response.status_code = 200
        this_file = Path(__file__).resolve()
        resource_file = this_file.parent / 'mock_mesonet_response.csv'
        mock_response.content = resource_file.read_bytes()
        mock_get.return_value = mock_response
        t = MesonetLocation.get_temps_by_keys(['ACME'], mock_get)[0]
        mock_get.assert_called_once()
        self.assertAlmostEqual(t, 97.0)  # TODO: Test invalid response, internet down, etc.


class TestLocationManager(TestCase):
    def test_predefined_location_setup(self):
        lm = LocationManager()
        lm.set_from_predefined_index(0)
        self.assertFalse(lm.is_custom)
        self.assertIn("Acme", lm.get_name())
        lat, long = lm.get_latitude_longitude()
        self.assertIsInstance(lat, (float, int))  # TODO: Just check numeric
        self.assertIsInstance(long, (float, int))  # TODO: Just check numeric

    def test_custom_location_setup(self):
        lm = LocationManager()
        lm.set_from_custom_location(-97.790, 35.784)
        self.assertTrue(lm.is_custom)
        self.assertIn("Custom", lm.get_name())
        lat, long = lm.get_latitude_longitude()
        self.assertIsInstance(lat, (float, int))  # TODO: Just check numeric
        self.assertIsInstance(long, (float, int))  # TODO: Just check numeric

    def test_custom_location_invalid_coordinates(self):
        lm = LocationManager()
        self.assertFalse(lm.set_from_custom_location(3.14, 2.718))
