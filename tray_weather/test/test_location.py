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
        t = MesonetLocation.get_temp_by_key('ACME', mock_get)
        mock_get.assert_called_once()
        self.assertAlmostEqual(t, 97.0)  # TODO: Test invalid response, internet down, etc.


class TestLocationManager(TestCase):
    def test_predefined_location_setup(self):
        lm = LocationManager()
        lm.set_from_predefined_index(0)
        self.assertFalse(lm.is_custom)
        self.assertIn("Acme", lm.get_name())
        with self.assertRaises(RuntimeError):
            lm.get_custom_names_ne_nw_sw_se()  # predefined locations shouldn't call this function
        lat, long = lm.get_latitude_longitude()
        self.assertIsInstance(lat, (float, int))  # TODO: Just check numeric
        self.assertIsInstance(long, (float, int))  # TODO: Just check numeric

    def test_custom_location_setup(self):
        lm = LocationManager()
        lm.set_from_custom_location(23, 23)
        self.assertTrue(lm.is_custom)
        self.assertIn("Custom", lm.get_name())
        lm.north_east_index = 0  # TODO: this won't be needed once set_from_custom_location works properly
        lm.north_west_index = 0  # TODO: this won't be needed once set_from_custom_location works properly
        lm.south_east_index = 0  # TODO: this won't be needed once set_from_custom_location works properly
        lm.south_west_index = 0  # TODO: this won't be needed once set_from_custom_location works properly
        lm.get_custom_names_ne_nw_sw_se()  # just make sure it passes fine
        lat, long = lm.get_latitude_longitude()
        self.assertIsInstance(lat, (float, int))  # TODO: Just check numeric
        self.assertIsInstance(long, (float, int))  # TODO: Just check numeric
