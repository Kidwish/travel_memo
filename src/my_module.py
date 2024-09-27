import folium
import pandas as pd


LOC_PATH = r"./data/loc_source.csv"
MAP_PATH = r"./output/map.html"
MARKER_PATH = r"./data/marker.csv"


class Map:
    def __init__(self, locations):
        self.locations = locations
        self.map = folium.Map(
            location=[locations["纬度"].mean(), locations["经度"].mean()],
            zoom_start=12,
        )
    
    def add_marker(self, lat, lon, popup):
        folium.Marker([lat, lon], popup=popup).add_to(self.map)

    def save(self, marker=MARKER_PATH, path=MAP_PATH):
        #read marker

        #add marker

        #save
        self.map.save(path)


class TravelMemo:
    def __init__(self) -> None:
        pass



def get_locations():
    df = pd.read_csv(LOC_PATH)
    return df


def add_marker(map, lat, lon, popup):
    map.add_marker(lat, lon, popup)




def test():
    dfLocations = get_locations()

    map = Map(dfLocations)
    add_marker(map, 31.2304, 121.4737, "Shanghai")

    map.save(MAP_PATH)








