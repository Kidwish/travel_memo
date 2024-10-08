from src.class_def import *
from src.amap_api.amap_req import *
import pandas as pd
import tkinter as tk
from tkinter import messagebox


LOC_PATH = r"./data/loc_source.csv"
MARKER_PATH = r"./data/marker.csv"
MAP_OUTPUT_PATH = r"./output/map.html"

CITY_COL = "地级市"
LAT_COL = "纬度"
LON_COL = "经度"


def get_locations(srcCity, dfLoc='amap'):
    if isinstance(dfLoc, pd.DataFrame):
        mask = dfLoc[CITY_COL].str.contains(srcCity)
        if mask.any():
            return (float(dfLoc[mask][LAT_COL].iloc[0]), float(dfLoc[mask][LON_COL].iloc[0]))
        else:
            return get_locations_fromAmap(srcCity)
    else:        
        return get_locations_fromAmap(srcCity)



def tk_win_submit(dest, entries):
    raw = RawInfo()
    for _, value in vars(raw).items():
        value.content = entries[value.label].get()

    for entry in entries.values():
        entry.delete(0, tk.END)

    dest.append(raw)


def tk_win_close(win):
    win.destroy()


def gen_marker_htmltxt(raw):
    ret = ''
    for _, value in vars(raw).items():
        ret += f"{value.label}  {value.content}<br>"
    CSStext = f'''<div style="width: 200px; height: auto; background-color: lightblue; padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); white-space: normal;">
    <h4 style="margin: 0;">标题</h4>
    <p style="margin: 5px 0;">{ret}</p>
</div>
'''
    return CSStext


def test():
    dfLocations = pd.read_csv(LOC_PATH)
    loc = get_locations('北京', dfLocations)

    memo = TravelMemo(loc)
    dest = []
    marker = DestMarker()
    mapBounds = []


    ## POPUP WINDOW
    windows = tk.Tk()
    windows.geometry("500x400")
    windows.title("添加一个感兴趣的目的地")
    entries = {}

    for _, value in vars(RawInfo()).items():
        frame = tk.Frame(windows)
        frame.pack(anchor='w', pady=5)

        lbl = tk.Label(frame, text=value.label)
        lbl.pack(side=tk.LEFT)

        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        entries[value.label] = entry


    closeButton = tk.Button(windows, text="关闭", command=lambda: tk_win_close(windows))
    closeButton.pack(side=tk.RIGHT, padx=20, pady=20)
    submitButton = tk.Button(windows, text="提交", command=lambda: tk_win_submit(dest, entries))
    submitButton.pack(side=tk.RIGHT, padx=20, pady=20)

    windows.mainloop()


    ## ADD MARKER
    for raw_info in dest:
        newCityLoc = get_locations(raw_info.city.content, dfLocations)
        marker.lat = newCityLoc[0]
        marker.lon = newCityLoc[1]
        marker.popup = gen_marker_htmltxt(raw_info)
        print(marker.popup)
        memo.add_marker(marker.lat, marker.lon, marker.popup)
        mapBounds.append([marker.lat, marker.lon])

    ## SAVE MAP TO HTML
    memo.fit_bounds(mapBounds)
    memo.save(MAP_OUTPUT_PATH)







