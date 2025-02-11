from math import sqrt
from typing import Callable, Optional

from requests import get


class NeighborData:
    def __init__(self):
        self.distance = 10000
        self.index = -1
        self.weight = 0

    def valid(self) -> bool:
        return self.index != -1


class MesonetLocation:
    def __init__(self, name: str, key: str, latitude: float, longitude: float):
        self.name = name
        self.key = key
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def get_temps_by_keys(keys: list[str], unit_test_get: Optional[Callable] = None) -> list[float]:
        csv_url = "https://www.mesonet.org/data/public/mesonet/current/current.csv.txt"
        try:
            if unit_test_get is None:  # pragma: no cover
                csv_response = get(csv_url)  # not unit testing the actual http request
            else:
                csv_response = unit_test_get(csv_url)
            csv_data = csv_response.content.decode('utf-8')
            csv_rows = csv_data.split("\n")
            data: dict[str, list[str]] = {x.split(',')[0]: x.split(',') for x in csv_rows}
            temps = []
            for k in keys:
                tokens = data[k]
                temp_token = tokens[10]
                temps.append(float(temp_token))
            return temps
        except Exception as e:  # pragma: no cover
            # could be a connection problem, content problem, etc.
            print(f"Could not get temperature from Mesonet.  Exception: {e}")
            return [-999] * len(keys)


mesonet_locations = [
    MesonetLocation("Acme", "ACME", 34.81, -98.02),
    MesonetLocation("Ada", "ADAX", 34.80, -96.67),
    MesonetLocation("Altus", "ALTU", 34.59, -99.34),
    MesonetLocation("Alva", "ALV2", 36.71, -98.71),
    MesonetLocation("Antlers", "ANT2", 34.25, -95.67),
    MesonetLocation("Apache", "APAC", 34.91, -98.29),
    MesonetLocation("Ardmore", "ARD2", 34.19, -97.09),
    MesonetLocation("Arnett", "ARNE", 36.07, -99.90),
    MesonetLocation("Beaver", "BEAV", 36.80, -100.53),
    MesonetLocation("Bessie", "BESS", 35.40, -99.06),
    MesonetLocation("Bixby", "BIXB", 35.96, -95.87),
    MesonetLocation("Blackwell", "BLAC", 36.75, -97.25),
    MesonetLocation("BoiseCity", "BOIS", 36.69, -102.50),
    MesonetLocation("Breckinridge", "BREC", 36.41, -97.69),
    MesonetLocation("Bristow", "BRIS", 35.78, -96.35),
    MesonetLocation("BrokenBow", "BROK", 34.04, -94.62),
    MesonetLocation("Buffalo", "BUFF", 36.83, -99.64),
    MesonetLocation("Burbank", "BURB", 36.63, -96.81),
    MesonetLocation("Burneyville", "BURN", 33.89, -97.27),
    MesonetLocation("Butler", "BUTL", 35.59, -99.27),
    MesonetLocation("Byars", "BYAR", 34.85, -97.00),
    MesonetLocation("Camargo", "CAMA", 36.03, -99.35),
    MesonetLocation("LakeCarlBlackwell", "CARL", 36.15, -97.29),
    MesonetLocation("Centrahoma", "CENT", 34.61, -96.33),
    MesonetLocation("Chandler", "CHAN", 35.65, -96.80),
    MesonetLocation("Cherokee", "CHER", 36.75, -98.36),
    MesonetLocation("Cheyenne", "CHEY", 35.55, -99.73),
    MesonetLocation("Chickasha", "CHIC", 35.03, -97.91),
    MesonetLocation("Clayton", "CLAY", 34.66, -95.33),
    MesonetLocation("Cloudy", "CLOU", 34.22, -95.25),
    MesonetLocation("Cookson", "COOK", 35.68, -94.85),
    MesonetLocation("Copan", "COPA", 36.91, -95.89),
    MesonetLocation("Durant", "DURA", 33.92, -96.32),
    MesonetLocation("ElkCity", "ELKC", 35.33, -99.39),
    MesonetLocation("ElReno", "ELRE", 35.55, -98.04),
    MesonetLocation("Erick", "ERIC", 35.20, -99.80),
    MesonetLocation("Eufaula", "EUFA", 35.30, -95.66),
    MesonetLocation("Eva", "EVAX", 36.92, -101.78),
    MesonetLocation("Fairview", "FAI2", 36.32, -98.55),
    MesonetLocation("Fittstown", "FITT", 34.55, -96.72),
    MesonetLocation("Foraker", "FORA", 36.84, -96.43),
    MesonetLocation("Freedom", "FREE", 36.73, -99.14),
    MesonetLocation("FortCobb", "FTCB", 35.15, -98.47),
    MesonetLocation("Goodwell", "GOOD", 36.60, -101.60),
    MesonetLocation("Grandfield", "GRA2", 34.24, -98.74),
    MesonetLocation("Guthrie", "GUTH", 35.85, -97.48),
    MesonetLocation("Haskell", "HASK", 35.75, -95.64),
    MesonetLocation("Hectorville", "HECT", 35.84, -96.00),
    MesonetLocation("Hinton", "HINT", 35.48, -98.48),
    MesonetLocation("Hobart", "HOBA", 34.99, -99.05),
    MesonetLocation("Holdenville", "HOLD", 35.07, -96.36),
    MesonetLocation("Hollis", "HOLL", 34.69, -99.83),
    MesonetLocation("Hooker", "HOOK", 36.86, -101.23),
    MesonetLocation("Hugo", "HUGO", 34.03, -95.54),
    MesonetLocation("Idabel", "IDAB", 33.83, -94.88),
    MesonetLocation("Inola", "INOL", 36.14, -95.45),
    MesonetLocation("Jay", "JAYX", 36.48, -94.78),
    MesonetLocation("Kenton", "KENT", 36.83, -102.88),
    MesonetLocation("KetchumRanch", "KETC", 34.53, -97.76),
    MesonetLocation("Kingfisher", "KIN2", 35.85, -97.95),
    MesonetLocation("Lahoma", "LAHO", 36.38, -98.11),
    MesonetLocation("Lane", "LANE", 34.31, -96.00),
    MesonetLocation("Madill", "MADI", 34.04, -96.94),
    MesonetLocation("Mangum", "MANG", 34.84, -99.42),
    MesonetLocation("Marena", "MARE", 36.06, -97.21),
    MesonetLocation("MayRanch", "MAYR", 36.99, -99.01),
    MesonetLocation("McAlester", "MCAL", 34.88, -95.78),
    MesonetLocation("Medford", "MEDF", 36.79, -97.75),
    MesonetLocation("MedicinePark", "MEDI", 34.73, -98.57),
    MesonetLocation("Miami", "MIAM", 36.89, -94.84),
    MesonetLocation("Minco", "MINC", 35.27, -97.96),
    MesonetLocation("Marshall", "MRSH", 36.12, -97.61),
    MesonetLocation("MtHerman", "MTHE", 34.31, -94.82),
    MesonetLocation("Newkirk", "NEWK", 36.90, -96.91),
    MesonetLocation("Newport", "NEWP", 34.23, -97.20),
    MesonetLocation("Nowata", "NOWA", 36.74, -95.61),
    MesonetLocation("Norman", "NRMN", 35.24, -97.46),
    MesonetLocation("Oilton", "OILT", 36.03, -96.50),
    MesonetLocation("OklahomaCityEast", "OKCE", 35.47, -97.46),
    MesonetLocation("Okemah", "OKEM", 35.43, -96.26),
    MesonetLocation("Okmulgee", "OKMU", 35.58, -95.91),
    MesonetLocation("PaulsValley", "PAUL", 34.72, -97.23),
    MesonetLocation("Pawnee", "PAWN", 36.36, -96.77),
    MesonetLocation("Perkins", "PERK", 36.00, -97.05),
    MesonetLocation("Porter", "PORT", 35.83, -95.56),
    MesonetLocation("Pryor", "PRYO", 36.37, -95.27),
    MesonetLocation("Putnam", "PUTN", 35.90, -98.96),
    MesonetLocation("RedRock", "REDR", 36.36, -97.15),
    MesonetLocation("Ringling", "RING", 34.19, -97.59),
    MesonetLocation("Sallisaw", "SALL", 35.44, -94.80),
    MesonetLocation("Seiling", "SEIL", 36.19, -99.04),
    MesonetLocation("Seminole", "SEMI", 35.18, -96.70),
    MesonetLocation("Shawnee", "SHAW", 35.36, -96.95),
    MesonetLocation("Skiatook", "SKIA", 36.42, -96.04),
    MesonetLocation("Slapout", "SLAP", 36.60, -100.26),
    MesonetLocation("Spencer", "SPEN", 35.54, -97.34),
    MesonetLocation("Stigler", "STIG", 35.27, -95.18),
    MesonetLocation("Stillwater", "STIL", 36.12, -97.10),
    MesonetLocation("Stuart", "STUA", 34.88, -96.07),
    MesonetLocation("Sulphur", "SULP", 34.57, -96.95),
    MesonetLocation("Tahlequah", "TAHL", 35.97, -94.99),
    MesonetLocation("Talala", "TALA", 36.57, -95.75),
    MesonetLocation("Talihina", "TALI", 34.71, -95.01),
    MesonetLocation("Tipton", "TIPT", 34.44, -99.14),
    MesonetLocation("Tishomingo", "TISH", 34.33, -96.68),
    MesonetLocation("Tulsa", "TULN", 36.20, -95.94),
    MesonetLocation("Valliant", "VALL", 33.94, -95.11),
    MesonetLocation("Vinita", "VINI", 36.78, -95.22),
    MesonetLocation("Walters", "WAL2", 34.40, -98.35),
    MesonetLocation("Washington", "WASH", 34.98, -97.52),
    MesonetLocation("Watonga", "WATO", 35.84, -98.53),
    MesonetLocation("Waurika", "WAUR", 34.17, -97.99),
    MesonetLocation("Weatherford", "WEAT", 35.51, -98.78),
    MesonetLocation("WebbersFalls", "WEB3", 35.52, -95.15),
    MesonetLocation("Westville", "WEST", 36.01, -94.64),
    MesonetLocation("Wilburton", "WILB", 34.90, -95.35),
    MesonetLocation("Wister", "WIST", 34.98, -94.69),
    MesonetLocation("Woodward", "WOOD", 36.42, -99.42),
    MesonetLocation("Wynona", "WYNO", 36.52, -96.34),
    MesonetLocation("Yukon", "YUKO", 35.56, -97.76),
]


class LocationManager:
    def __init__(self):
        self.is_custom = False
        self.predefined_index = 99
        self.custom_latitude = -99.99
        self.custom_longitude = -99.99
        self.north_east_index = -1
        self.north_west_index = -1
        self.south_west_index = -1
        self.south_east_index = -1
        self.north_east_weight = 0
        self.north_west_weight = 0
        self.south_west_weight = 0
        self.south_east_weight = 0

    def set_from_config(self, config: dict):
        self.is_custom = config.get('is_custom', False)
        self.predefined_index = config.get('predefined_index', 99)
        self.custom_latitude = config.get('custom_latitude', -99.99)
        self.custom_longitude = config.get('custom_longitude', -99.99)
        self.north_east_index = config.get('north_east_index', -1)
        self.north_west_index = config.get('north_west_index', -1)
        self.south_west_index = config.get('south_west_index', -1)
        self.south_east_index = config.get('south_east_index', -1)
        self.north_east_weight = config.get('north_east_weight', 0.0)
        self.north_west_weight = config.get('north_west_weight', 0.0)
        self.south_west_weight = config.get('south_west_weight', 0.0)
        self.south_east_weight = config.get('south_east_weight', 0.0)

    def set_from_predefined_index(self, index: int):
        self.is_custom = False
        self.predefined_index = index

    def set_from_custom_location(self, longitude: float, latitude: float) -> bool:
        valid_neighbors = self.get_neighbors(longitude, latitude)
        if not valid_neighbors:
            return False
        self.is_custom = True
        self.predefined_index = -1
        self.custom_latitude = latitude
        self.custom_longitude = longitude
        # set neighboring location index
        self.south_west_index = valid_neighbors[0].index
        self.south_west_weight = valid_neighbors[0].weight
        self.north_west_index = valid_neighbors[1].index
        self.north_west_weight = valid_neighbors[1].weight
        self.south_east_index = valid_neighbors[2].index
        self.south_east_weight = valid_neighbors[2].weight
        self.north_east_index = valid_neighbors[3].index
        self.north_east_weight = valid_neighbors[3].weight
        return True  # if successful

    @staticmethod
    def get_neighbors(longitude: float, latitude: float) -> tuple | None:
        # Find distances to the closest stations
        sw_data = NeighborData()
        nw_data = NeighborData()
        se_data = NeighborData()
        ne_data = NeighborData()
        for i, ml in enumerate(mesonet_locations):
            # Southwest Locations
            if ml.longitude < longitude:
                if ml.latitude < latitude:
                    temp_sw_dist = sqrt(((ml.longitude - longitude) ** 2) + ((ml.latitude - latitude) ** 2))
                    if temp_sw_dist < sw_data.distance:
                        sw_data.distance = temp_sw_dist
                        sw_data.index = i
            # NorthWest Locations
            if ml.longitude < longitude:
                if ml.latitude > latitude:
                    temp_nw_dist = sqrt(((ml.longitude - longitude) ** 2) + ((ml.latitude - latitude) ** 2))
                    if temp_nw_dist < nw_data.distance:
                        nw_data.distance = temp_nw_dist
                        nw_data.index = i
            # SouthEast Locations
            if ml.longitude > longitude:
                if ml.latitude < latitude:
                    temp_se_dist = sqrt(((ml.longitude - longitude) ** 2) + ((ml.latitude - latitude) ** 2))
                    if temp_se_dist < se_data.distance:
                        se_data.distance = temp_se_dist
                        se_data.index = i
            # NorthEast Locations
            if ml.longitude > longitude:
                if ml.latitude > latitude:
                    temp_ne_dist = sqrt(((ml.longitude - longitude) ** 2) + ((ml.latitude - latitude) ** 2))
                    if temp_ne_dist < ne_data.distance:
                        ne_data.distance = temp_ne_dist
                        ne_data.index = i
        # check for unable to match neighbors
        if not all([x.valid() for x in [sw_data, nw_data, se_data, ne_data]]):
            return None

        # Need to invert distances because shorter distances should have larger influence
        length_sum = (1 / sw_data.distance) + (1 / nw_data.distance) + (1 / se_data.distance) + (1 / ne_data.distance)
        sw_data.weight = (1 / sw_data.distance) / length_sum
        # print(f"Got SW site as: {mesonet_locations[sw_data.index].name}")
        nw_data.weight = (1 / nw_data.distance) / length_sum
        # print(f"Got NW site as: {mesonet_locations[nw_data.index].name}")
        se_data.weight = (1 / se_data.distance) / length_sum
        # print(f"Got SE site as: {mesonet_locations[se_data.index].name}")
        ne_data.weight = (1 / ne_data.distance) / length_sum
        # print(f"Got NE site as: {mesonet_locations[ne_data.index].name}")

        return sw_data, nw_data, se_data, ne_data

    def to_dict(self):
        config = dict()
        config['is_custom'] = self.is_custom
        config['predefined_index'] = self.predefined_index
        config['custom_latitude'] = self.custom_latitude
        config['custom_longitude'] = self.custom_longitude
        config['north_east_index'] = self.north_east_index
        config['north_west_index'] = self.north_west_index
        config['south_west_index'] = self.south_west_index
        config['south_east_index'] = self.south_east_index
        config['north_east_weight'] = self.north_east_weight
        config['north_west_weight'] = self.north_west_weight
        config['south_west_weight'] = self.south_west_weight
        config['south_east_weight'] = self.south_east_weight
        return config

    def get_name(self) -> str:
        if self.is_custom:
            return f"Custom Location ({round(self.custom_longitude, 4)}°W, {round(self.custom_latitude, 4)}°N)"
        else:
            return mesonet_locations[self.predefined_index].name

    def get_latitude_longitude(self) -> tuple[float, float]:
        if self.is_custom:
            return self.custom_latitude, self.custom_longitude
        else:
            location_item = mesonet_locations[self.predefined_index]
            return location_item.latitude, location_item.longitude
