from src.class_def import *
import pandas as pd
import tkinter as tk
from tkinter import messagebox


LOC_PATH = r"./data/loc_source.csv"
MARKER_PATH = r"./data/marker.csv"
MAP_OUTPUT_PATH = r"./output/map.html"

CITY_COL = "地级市"
LAT_COL = "纬度"
LON_COL = "经度"


def get_locations(srcCity, dfLoc):
    mask = dfLoc[CITY_COL].str.contains(srcCity)
    return (float(dfLoc[mask][LAT_COL].iloc[0]), float(dfLoc[mask][LON_COL].iloc[0]))

def tk_win_submit(raw, dest, entries, lbls):
    raw.trip_time = entries["什么时候去:"].get()
    raw.ticket_book_time = entries["什么时候订票:"].get()
    raw.hotel_book_time = entries["什么时候订酒店:"].get()
    raw.food = entries["什么东西好吃:"].get()
    raw.scenery = entries["什么景色好看:"].get()
    raw.score = entries["感兴趣的程度(1-10):"].get()
    raw.note = entries["备注:"].get()

    for entry in entries.values():
        entry.delete(0, tk.END)
    
    tmpDest = Destination()
    tmpDest.raw_info = raw
    dest.append(tmpDest)

def tk_win_close(win):
    win.destroy()


def test():
    dfLocations = pd.read_csv(LOC_PATH)
    loc = get_locations('北京', dfLocations)

    memo = TravelMemo(loc)
    dest = []
    marker = DestMarker()
    raw = RawInfo()


    ## POPUP WINDOW
    windows = tk.Tk()
    windows.geometry("500x300")
    windows.title("添加一个感兴趣的目的地")

    labels = ["什么时候去:",
              "什么时候订票:",
              "什么时候订酒店:",
              "什么东西好吃:",
              "什么景色好看:",
              "感兴趣的程度(1-10):",
              "备注:",
              ]
    entries = {}

    for label in labels:
        frame = tk.Frame(windows)
        frame.pack(anchor='w', pady=5)

        lbl = tk.Label(frame, text=label)
        lbl.pack(side=tk.LEFT)

        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        entries[label] = entry

    close_button = tk.Button(windows, text="关闭", command=lambda: tk_win_close(windows))
    close_button.pack(side=tk.RIGHT, padx=20, pady=20)
    submit_button = tk.Button(windows, text="提交", command=lambda: tk_win_submit(raw, dest, entries, labels))
    submit_button.pack(side=tk.RIGHT, padx=20, pady=20)

    windows.mainloop()

    print(dest)

    ## SAVE MAP TO HTML
    memo.save(MAP_OUTPUT_PATH)

    print(raw)






