import folium

class TravelMemo:
    def __init__(self, loc=[31.2304, 121.4737]):
        self.map = folium.Map(
            location=[loc[0], loc[1]],
            zoom_start=12,
        )
    
    def add_marker(self, lat, lon, popup):
        folium.Marker([lat, lon], popup=popup).add_to(self.map)
    
    def save(self, marker, path):
        self.map.save(path)



class Destination:
    def __init__(self) -> None:
        self.marker = DestMarker()
        self.raw_info = RawInfo()



class DestMarker:
    def __init__(self) -> None:
        pass


class RawInfo:
    def __init__(self) -> None:
        pass

