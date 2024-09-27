import folium

class TravelMemo:
    def __init__(self, loc=[31.2304, 121.4737]):
        self.map = folium.Map(
            location=[loc[0], loc[1]],
            zoom_start=12,
        )
    
    def add_marker(self, lat, lon, popup):
        folium.Marker([lat, lon], popup=popup).add_to(self.map)
    
    def save(self, path):
        self.map.save(path)



class Destination:
    def __init__(self) -> None:
        self.marker = DestMarker()
        self.raw_info = RawInfo()
    
    def __str__(self):
        return f"marker: {self.marker}\nraw_info: {self.raw_info}"



class DestMarker:
    def __init__(self) -> None:
        pass


class RawInfo():
    def __init__(self) -> None:
        self.trip_time = None
        self.ticket_book_time = None
        self.hotel_book_time = None
        self.food = []
        self.scenery = []
        self.score = None
        self.note = None
    
    def __str__(self):
        return f"trip_time: {self.trip_time}\nticket_book_time: {self.ticket_book_time}\nhotel_book_time: {self.hotel_book_time}\nfood: {self.food}\nscenery: {self.scenery}\nscore: {self.score}\nnote: {self.note}"



