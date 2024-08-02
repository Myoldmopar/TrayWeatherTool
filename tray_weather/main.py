# Python standard library imports
from signal import signal, SIGINT, SIG_DFL
from tempfile import NamedTemporaryFile

# Pip installed library imports
from PIL import Image, ImageDraw, ImageFont
import pyperclip

# Use these lines to validate the gi library installation prior to importing from gi.repository
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib  # noqa: E402

# Local package imports
from tray_weather.config import Configuration  # noqa: E402
from tray_weather.dialog_custom_location import DialogCustomLocation  # noqa: E402
from tray_weather.dialog_solar_plot import show_solar_plot  # noqa: E402
from tray_weather.dialog_temperature_plot import DialogTemperaturePlot  # noqa: E402
from tray_weather.storms import StormType, StormManager  # noqa: E402
from tray_weather.mesonet import MesonetManager  # noqa: E402
from tray_weather.misc import mesonet_locations, time_step_minute_intervals, storm_tests  # noqa: E402


class TrayWeatherIcon:
    def __init__(self):
        # not sure why but PyCharm seems to think this needs another argument
        # noinspection PyArgumentList
        self.indicator = AppIndicator3.Indicator.new(
            "example-simple-client",
            "indicator-messages",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # the app-indicator seems to ignore if we set the filename the same, so we toggle between two file names
        self.icon_file_path_a = NamedTemporaryFile(suffix='.png').name
        self.icon_file_path_b = NamedTemporaryFile(suffix='.png').name
        self.icon_file_toggle = False

        self.config = Configuration()
        lat, long = self.config.location.get_latitude_longitude()
        self.storms = StormManager(lat, long)
        self.updating = False
        self._build_menu()
        self.update()
        self.timeout_id = GLib.timeout_add(self.config.frequency_minutes * 60 * 1000, self.on_timer_ticked)

    def _build_menu(self):

        menu_main = Gtk.Menu()

        menu_item_action_items = Gtk.MenuItem(label="Action Items")
        submenu_action_items = Gtk.Menu()
        menu_item_action_items_update = Gtk.MenuItem(label="Update Temperature Now")
        menu_item_action_items_update.connect("activate", self.update_now)
        submenu_action_items.append(menu_item_action_items_update)
        menu_item_action_items_plot = Gtk.MenuItem(label="Plot Temperature History")
        menu_item_action_items_plot.connect("activate", self.plot_temps)
        submenu_action_items.append(menu_item_action_items_plot)
        menu_item_action_items_solar = Gtk.MenuItem(label="Plot Solar Path/Position")
        menu_item_action_items_solar.connect("activate", show_solar_plot)
        submenu_action_items.append(menu_item_action_items_solar)
        menu_item_action_items_copy = Gtk.MenuItem(label="Copy Temperature History")
        menu_item_action_items_copy.connect("activate", self.copy_history)
        submenu_action_items.append(menu_item_action_items_copy)
        menu_item_action_items_clear = Gtk.MenuItem(label="Clear Temperature History")
        menu_item_action_items_clear.connect("activate", self.clear_history)
        submenu_action_items.append(menu_item_action_items_clear)
        menu_item_action_items.set_submenu(submenu_action_items)
        menu_main.append(menu_item_action_items)

        menu_main.append(Gtk.SeparatorMenuItem())

        menu_item_storm_tests = Gtk.MenuItem(label="Storm Tests")
        submenu_storm_tests = Gtk.Menu()
        for st in storm_tests:
            item = Gtk.MenuItem(label=st)
            item.connect("activate", self.storm_test, st)
            submenu_storm_tests.append(item)
        menu_item_storm_tests.set_submenu(submenu_storm_tests)
        menu_main.append(menu_item_storm_tests)

        menu_item_temp_tests = Gtk.MenuItem(label="Temperature Tests")
        submenu_temp_tests = Gtk.Menu()
        for tt in [-25, 0, 32, 110]:
            item = Gtk.MenuItem(label=tt)
            item.connect("activate", self.temp_test, tt)
            submenu_temp_tests.append(item)
        menu_item_temp_tests.set_submenu(submenu_temp_tests)
        menu_main.append(menu_item_temp_tests)

        menu_main.append(Gtk.SeparatorMenuItem())

        menu_item_general_information = Gtk.MenuItem(label="General Information")
        submenu_info = Gtk.Menu()
        props = self.config.gather_history_properties()
        self.menu_item_info_oldest = Gtk.MenuItem(label=f"Oldest reading: {props.oldest_time}")
        submenu_info.append(self.menu_item_info_oldest)
        self.menu_item_info_newest = Gtk.MenuItem(label=f"Newest reading: {props.newest_time}")
        submenu_info.append(self.menu_item_info_newest)
        self.menu_item_info_highest = Gtk.MenuItem(label=f"Highest reading: {props.highest_temp}")
        submenu_info.append(self.menu_item_info_highest)
        self.menu_item_info_lowest = Gtk.MenuItem(label=f"Lowest reading: {props.lowest_temp}")
        submenu_info.append(self.menu_item_info_lowest)
        menu_item_general_information.set_submenu(submenu_info)
        menu_main.append(menu_item_general_information)

        menu_item_current_settings = Gtk.MenuItem(label="Current Settings")
        submenu_settings = Gtk.Menu()
        location_name = self.config.location.get_name()
        self.menu_item_settings_location = Gtk.MenuItem(label=f"Location: {location_name}")
        submenu_settings.append(self.menu_item_settings_location)
        pluralize = "minutes" if self.config.frequency_minutes > 1 else "minute"
        menu_item_settings_update_rate = Gtk.MenuItem(
            label=f"Update Frequency: {self.config.frequency_minutes} {pluralize}"
        )
        submenu_settings.append(menu_item_settings_update_rate)
        if self.config.location.is_custom:
            ne, nw, sw, se = self.config.location.get_custom_names_ne_nw_sw_se()
        else:
            ne, nw, sw, se = ["NotCustom", "NotCustom", "NotCustom", "NotCustom"]
        self.menu_item_settings_ne_station = Gtk.MenuItem(label=f"Northeast Station: {ne}")
        submenu_settings.append(self.menu_item_settings_ne_station)
        self.menu_item_settings_se_station = Gtk.MenuItem(label=f"Northwest Station: {nw}")
        submenu_settings.append(self.menu_item_settings_se_station)
        self.menu_item_settings_nw_station = Gtk.MenuItem(label=f"Southwest Station: {sw}")
        submenu_settings.append(self.menu_item_settings_nw_station)
        self.menu_item_settings_sw_station = Gtk.MenuItem(label=f"Southeast Station: {se}")
        submenu_settings.append(self.menu_item_settings_sw_station)
        menu_item_current_settings.set_submenu(submenu_settings)
        menu_main.append(menu_item_current_settings)

        menu_item_adjust_settings = Gtk.MenuItem(label="Adjust Settings")
        submenu_adjust = Gtk.Menu()
        menu_item_adjust_location = Gtk.MenuItem(label="Predefined Location")
        submenu_locations = Gtk.Menu()
        for location_index, location in enumerate(mesonet_locations):
            item = Gtk.MenuItem(label=location.name)
            item.connect("activate", self.on_predefined_location, location_index)
            submenu_locations.append(item)
        menu_item_adjust_location.set_submenu(submenu_locations)
        submenu_adjust.append(menu_item_adjust_location)
        menu_item_adjust_custom = Gtk.MenuItem(label="Custom Location...")
        menu_item_adjust_custom.connect("activate", self.on_custom_location)
        submenu_adjust.append(menu_item_adjust_custom)
        menu_item_adjust_update_rate = Gtk.MenuItem(label="Update Rate")
        submenu_rate = Gtk.Menu()
        for frequency in time_step_minute_intervals:
            label = f"{frequency} minute" if frequency == 1 else f"{frequency} minutes"
            item = Gtk.MenuItem(label=label)
            item.connect("activate", self.update_rate, frequency)
            submenu_rate.append(item)
        menu_item_adjust_update_rate.set_submenu(submenu_rate)
        submenu_adjust.append(menu_item_adjust_update_rate)
        menu_item_adjust_settings.set_submenu(submenu_adjust)
        menu_main.append(menu_item_adjust_settings)

        # menu_main.append(Gtk.SeparatorMenuItem())
        #
        # menu_item_info = Gtk.MenuItem(label="Info...")
        # menu_main.append(menu_item_info)

        menu_main.append(Gtk.SeparatorMenuItem())

        menu_item_exit = Gtk.MenuItem(label="Exit")
        menu_item_exit.connect("activate", self.quit)
        menu_main.append(menu_item_exit)

        # show all....
        menu_main.show_all()

        # but do make a few hidden if needed
        if not self.config.location.is_custom:
            self.menu_item_settings_ne_station.set_visible(False)
            self.menu_item_settings_nw_station.set_visible(False)
            self.menu_item_settings_sw_station.set_visible(False)
            self.menu_item_settings_se_station.set_visible(False)

        self.indicator.set_menu(menu_main)

    def update(self, force_temp: float | None = None, force_storm: int | None = None):
        if self.updating:
            return
        self.updating = True
        icon_color = self.storms.icon_color(force_storm)
        if force_temp:
            temperature = force_temp
        else:
            m = MesonetManager()
            if self.config.location.is_custom:
                pass  # need to call custom location temp getter
                temperature = -99
            else:
                location_key = mesonet_locations[self.config.location.predefined_index].key
                temperature = m.get_temp_by_key(location_key)
        self.config.log_data_point(temperature)
        s_temp = str(int(temperature))
        # toggle the icon file flag, and use b if the toggle is set, otherwise back to a
        self.icon_file_toggle = not self.icon_file_toggle
        file_path = self.icon_file_path_b if self.icon_file_toggle else self.icon_file_path_a
        self.create_text_image(s_temp, file_path, icon_color)
        self.indicator.set_icon_full(file_path, "temperature_icon")
        self.config.save_to_file()
        # update menu items here
        props = self.config.gather_history_properties()
        self.menu_item_info_oldest.set_label(f"Oldest reading: {props.oldest_time}")
        self.menu_item_info_newest.set_label(f"Newest reading: {props.newest_time}")
        self.menu_item_info_highest.set_label(f"Highest reading: {props.highest_temp}")
        self.menu_item_info_lowest.set_label(f"Lowest reading: {props.lowest_temp}")
        self.updating = False

    def update_now(self, _widget):
        self.update()

    def plot_temps(self, _widget):
        if len(self.config.temp_history) == 1:
            self.update()
        DialogTemperaturePlot(self.config.temp_history)

    def copy_history(self, _widget):
        history = self.config.temp_history_for_clipboard()
        pyperclip.copy(history)

    def clear_history(self, _widget):
        self.config.temp_history.clear()
        self.update()

    def storm_test(self, _widget, test_name: str):
        if test_name == "Flood Watch":
            self.update(force_storm=StormType.FloodWatch)
        elif test_name == "Flood Warning":
            self.update(force_storm=StormType.FloodWarning)
        elif test_name == "ThunderStorm Watch":
            self.update(force_storm=StormType.ThunderStormWatch)
        elif test_name == "ThunderStorm Warning":
            self.update(force_storm=StormType.ThunderStormWarning)
        elif test_name == "Tornado Watch":
            self.update(force_storm=StormType.TornadoWatch)
        elif test_name == "Tornado Warning":
            self.update(force_storm=StormType.TornadoWarning)

    def temp_test(self, _widget, temperature: int):
        print(f"Inside temp_test trying to test: {temperature}")
        self.update(force_temp=temperature)

    def on_predefined_location(self, _widget, location_index: int):
        self.config.location.set_from_predefined_index(location_index)
        # update menu label for this location name
        self.menu_item_settings_location.set_label(self.config.location.get_name())
        # make sure to set these to hidden since we selected a predefined location
        self.menu_item_settings_ne_station.set_visible(False)
        self.menu_item_settings_nw_station.set_visible(False)
        self.menu_item_settings_sw_station.set_visible(False)
        self.menu_item_settings_se_station.set_visible(False)
        # rebuild storm manager
        lat, long = self.config.location.get_latitude_longitude()
        self.storms = StormManager(lat, long)
        # and of course do an update to get a fresh temperature
        self.update()

    def on_custom_location(self, _widget):
        DialogCustomLocation()
        # if we selected one, make sure to update these and make them visible:
        # self.menu_item_settings_ne_station
        # self.menu_item_settings_se_station
        # self.menu_item_settings_nw_station
        # self.menu_item_settings_sw_station
        lat, long = self.config.location.get_latitude_longitude()
        self.storms = StormManager(lat, long)
        # and of course do an update to get a fresh temperature
        self.update()

    def update_rate(self, _widget, frequency: int):
        if self.timeout_id is not None:
            GLib.source_remove(self.timeout_id)
        self.config.frequency_minutes = frequency
        self.timeout_id = GLib.timeout_add(frequency * 60 * 1000, self.on_timer_ticked)

    @staticmethod
    def create_text_image(text: str, file_path: str, icon_color: str):
        icon_side_length = 128
        image = Image.new('RGB', (icon_side_length, icon_side_length), icon_color)
        draw = ImageDraw.Draw(image)
        if len(text) > 2:  # either <= -10, or >= 100
            font_size = 72
            height_offset = 16
        else:
            font_size = 96
            height_offset = 20
        font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', font_size)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (icon_side_length - text_width) // 2
        text_y = (icon_side_length - text_height) // 2 - height_offset  # manual offset to get it centered...odd
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
        image.save(file_path, 'PNG')

    def on_timer_ticked(self):
        self.update()
        return True

    def quit(self):
        self.config.save_to_file()
        Gtk.main_quit()


def run_main():
    signal(SIGINT, SIG_DFL)
    TrayWeatherIcon()
    Gtk.main()


if __name__ == "__main__":
    run_main()
