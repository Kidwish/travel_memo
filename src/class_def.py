import folium

class TravelMemo:
    def __init__(self, loc=[31.2304, 121.4737]):
        self.map = folium.Map(
            location=[loc[0], loc[1]],
            zoom_start=12,
        )
    
    def add_marker(self, lat, lon, popup_content):
        folium.Marker(
            location=[lat, lon], 
            popup=folium.Popup(popup_content, width=300)
            ).add_to(self.map)
    
    def fit_bounds(self, bounds):
        self.map.fit_bounds(bounds)
    
    def save(self, path):
        self.map.save(path)



# class Destination:
#     def __init__(self) -> None:
#         self.marker = DestMarker()
#         self.raw_info = RawInfo()
    
#     def __str__(self):
#         return f"marker: {self.marker}\nraw_info: {self.raw_info}"



class DestMarker:
    def __init__(self) -> None:
        self.lat = None
        self.lon = None
        self.popup = None
        self.tooltip = None


class RawInfoDetail:
    def __init__(self, label) -> None:
        self.content = None
        self.label = label
    
    def __str__(self):
        return f"{self.label} : {self.content}"


class RawInfo:
    def __init__(self) -> None:
        self.city = RawInfoDetail("去哪里")
        self.trip_time = RawInfoDetail("什么时候去")
        self.ticket_book_time = RawInfoDetail("什么时候订票")
        self.hotel_book_time = RawInfoDetail("什么时候订酒店")
        self.food = RawInfoDetail("什么东西好吃")
        self.scenery = RawInfoDetail("什么景色好看")
        self.score = RawInfoDetail("感兴趣的程度(1-10)")
        self.note = RawInfoDetail("备注")
    
    def __str__(self):
        return f"city: {self.city}\ntrip_time: {self.trip_time}\nticket_book_time: {self.ticket_book_time}\nhotel_book_time: {self.hotel_book_time}\nfood: {self.food}\nscenery: {self.scenery}\nscore: {self.score}\nnote: {self.note}"



