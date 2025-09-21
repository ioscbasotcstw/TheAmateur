import math
from typing import Optional, Tuple, Dict

R = 6371e3
N = 1e3


class GeoInfo:
    def __init__(self, response: Dict[str, str], url: Optional[str] = None, coordinates: Optional[str] = None):
        self.response = response
         
        if self.response['coordinates'] == "":
            raise ValueError(f"The coordinates from the model are empty: {self.response['coordinates']}")
         
        if url:
            coords_string = url.split("@")[1]
            lat_str, lon_str, _ = coords_string.split(',', 2)
        else:
            coords_string = coordinates
            lat_str, lon_str = coords_string.split(",", 1)
        self.lat_1 = float(lat_str.strip())
        self.lon_1 = float(lon_str.strip())
        if response['coordinates'].split(",")[0].endswith('N') or response['coordinates'].split(",")[0].endswith('S') or response['coordinates'].split(",")[1].endswith('E') or response['coordinates'].split(",")[0].endswith('W'):
            self.lat_2 = float(response['coordinates'].split(",")[0].split(" ")[0].strip())
            self.lon_2 = float(response['coordinates'].split(",")[1].split(" ")[1].strip())
        else:
            self.lat_2 = float(response['coordinates'].split(",")[0].strip())
            self.lon_2 = float(response['coordinates'].split(",")[1].strip())

        self.phi_1 = self.lat_1 * math.pi / 180
        self.phi_2 = self.lat_2 * math.pi / 180
        self.delta_gamma = (self.lon_2 - self.lon_1) * math.pi / 180

    def calculate_error(self) -> Tuple[float, float, float, float, float]:
        delta_phi = (self.lat_2 - self.lat_1) * math.pi / 180
        a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(self.phi_1) * math.cos(self.phi_2) * math.sin(self.delta_gamma / 2) * math.sin(self.delta_gamma / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        error = (R * c) / N
        return error, self.lat_1, self.lon_1, self.lat_2, self.lon_2

    def calculate_bearing(self) -> float:
        y = math.sin(self.delta_gamma) * math.cos(self.phi_2)
        x = math.cos(self.phi_1) * math.sin(self.phi_2) - math.sin(self.phi_1) * math.cos(self.phi_2) * math.cos(self.delta_gamma)

        theta = math.atan2(y, x)
        bearing = (theta * 180 / math.pi + 360) % 360
        return bearing

    def get_direction(self, angle: float) -> str:
        directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West'];
        return directions[round(angle / 45) % 8]

    def combine_info(self, error: float, direction: str) -> str:
        return f"Point 1 is approximately {error} km away from Point 2 in the {direction} direction"