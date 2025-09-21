from typing import Optional

import folium
import geopy


class MapGenerator:
    def __init__(self, timeout: int = 10):
        self.geocoder = geopy.Nominatim(user_agent="TheAmateur", timeout=timeout)
        self.line_coordinates = []

    def get_map(self, location1: str, location2: Optional[str] = None, error: Optional[float] = None, direction: Optional[str] = None):
        try:
            l1 = self.geocoder.geocode(location1)
            if not l1:
                print(f"Warning: Location not found: {location1}")
                return None

            if location2:
                l2 = self.geocoder.geocode(location2)
                if not l2:
                    print(f"Warning: Location not found: {location2}")
                    return None

                map_obj = folium.Map(location=[l2.latitude, l2.longitude], zoom_start=7)
                folium.Marker([l1.latitude, l1.longitude], popup='Loc 1', icon=folium.Icon(icon="cloud")).add_to(map_obj)
                folium.Marker([l2.latitude, l2.longitude], popup='Loc 2', icon=folium.Icon(color="green")).add_to(map_obj)

                if error and direction:
                    self.line_coordinates.extend([[l1.latitude, l1.longitude], [l2.latitude, l2.longitude]])
                    text = f"{error}km in {direction}"
                    folium.PolyLine(
                        locations=self.line_coordinates,
                        color='blue',
                        weight=5,
                        opacity=0.8,
                        tooltip=text
                    ).add_to(map_obj)
            else:
                map_obj = folium.Map(location=[l1.latitude, l1.longitude], zoom_start=10)
                folium.Marker([l1.latitude, l1.longitude], popup='Loc', icon=folium.Icon(icon="cloud")).add_to(map_obj)

            return map_obj
        except geopy.exc.GeocoderUnavailable as e:
            print(f"Error: Geocoding service is unavailable. {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred in get_map(): {e}")
            return None