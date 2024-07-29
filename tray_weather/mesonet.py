import requests


class MesonetManager:
    def __init__(self):
        csv_url = "https://www.mesonet.org/data/public/mesonet/current/current.csv.txt"
        csv_response = requests.get(csv_url)
        csv_data = csv_response.content.decode('utf-8')
        csv_rows = csv_data.split("\n")
        self.data: dict[str, list[str]] = {x.split(',')[0]: x.split(',') for x in csv_rows}

    def get_temp_by_key(self, key: str) -> float:
        tokens = self.data[key]
        return float(tokens[10])
