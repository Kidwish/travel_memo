from src.class_def import *
from src.amap_api.amap_req import *
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk


DATA_PATH = r"./data/dest_raw_info.csv"
LOC_PATH = r"./data/loc_source.csv"
MARKER_PATH = r"./data/marker.csv"
MAP_OUTPUT_PATH = r"./output/map.html"

CITY_COL = "地级市"
LAT_COL = "纬度"
LON_COL = "经度"


def load_dest_info():
    # get column info
    colDetail = []
    for _, value in vars(RawInfo()).items():
        colDetail.append(value.label)
    colCity = RawInfo().city.label

    # get data
    if os.path.isfile(DATA_PATH):
        dfDestRawInfo = pd.read_csv(DATA_PATH)
        # todo: check column info
    else:
        dfDestRawInfo = pd.DataFrame(columns=colDetail)
    
    return (dfDestRawInfo, colDetail, colCity)

def add_dest_info(dfDestRawInfo: pd.DataFrame, raw: RawInfo):
    rawDict = {}
    for _, value in vars(raw).items():
        rawDict[value.label] = value.content
    dfDestRawInfo.loc[len(dfDestRawInfo)] = rawDict

def get_locations(srcCity, dfLoc='amap'):
    if isinstance(dfLoc, pd.DataFrame):
        mask = dfLoc[CITY_COL].str.contains(srcCity)
        if mask.any():
            return (float(dfLoc[mask][LAT_COL].iloc[0]), float(dfLoc[mask][LON_COL].iloc[0]))
        else:
            return get_locations_fromAmap(srcCity)
    else:        
        return get_locations_fromAmap(srcCity)



def tk_win_submit(dfDestRawInfo, entries):
    raw = RawInfo()
    for _, value in vars(raw).items():
        if value.label == raw.city.label and entries[value.label].get().strip() == "":
            messagebox.showwarning("警告", f"{raw.city.label} 不能为空！")
            return
        value.content = entries[value.label].get()

    for entry in entries.values():
        entry.delete(0, tk.END)

    add_dest_info(dfDestRawInfo, raw)
    messagebox.showinfo("成功", "目的地已成功添加！")


def tk_win_close(win):
    win.destroy()

def tk_win_open_delete_window(windows, df, col, delList):
    dataList = df[col].tolist()
    delete_window = tk.Toplevel(windows)
    delete_window.title("删除目的地")

    # 创建下拉选项
    selected_value = tk.StringVar()
    dropdown = ttk.Combobox(delete_window, textvariable=selected_value)
    dropdown['values'] = dataList  # 设置下拉选项
    dropdown.pack(pady=20)

    def tk_win_delete_selection(delList):
        selected = selected_value.get()
        if selected in dataList:
            delList.append(selected)
            dataList.remove(selected)
            dropdown['values'] = dataList  # 更新下拉选项
            dropdown.set('')  # 清空下拉框
            messagebox.showinfo("成功", f"{selected} 已成功删除！")
        else:
            messagebox.showwarning("警告", "请选择有效的目的地！")
        delete_window.destroy()

    delete_button = tk.Button(delete_window, text="删除", command=lambda: tk_win_delete_selection(delList))
    delete_button.pack(pady=20)

def gen_marker_htmltxt(row, columns):
    ret = ''
    for col in columns:
        ret += f"{col} ： {'/' if str(getattr(row, col)) == 'nan' else getattr(row, col)}<br>"
    
    CSStext = f'''<div style="width: 200px; height: auto; background-color: white; white-space: normal;">
    <h4 style="margin: 0;">标题</h4>
    <p style="margin: 5px 0;">{ret}</p>
</div>
'''
    return CSStext


def test():

    (dfDestRawInfo, colDetail, colCity) = load_dest_info()

    dfLocations = pd.read_csv(LOC_PATH)
    loc = get_locations('北京', dfLocations)

    memo = TravelMemo(loc)
    marker = DestMarker()
    mapBounds = []
    delList = []


    ## POPUP WINDOW
    windows = tk.Tk()
    windows.geometry("500x400")
    windows.title("添加一个感兴趣的目的地")
    entries = {}

    for colLabel in colDetail:
        frame = tk.Frame(windows)
        frame.pack(anchor='w', pady=5)

        lbl = tk.Label(frame, text=colLabel)
        lbl.pack(side=tk.LEFT)

        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        entries[colLabel] = entry


    closeButton = tk.Button(windows, text="关闭", command=lambda: tk_win_close(windows))
    closeButton.pack(side=tk.RIGHT, padx=20, pady=20)
    submitButton = tk.Button(windows, text="提交", command=lambda: tk_win_submit(dfDestRawInfo, entries))
    submitButton.pack(side=tk.RIGHT, padx=20, pady=20)
    deleteButton = tk.Button(windows, text="删除目的地", command=lambda: tk_win_open_delete_window(windows, dfDestRawInfo, colCity, delList))
    deleteButton.pack(side=tk.RIGHT, padx=20, pady=20)

    windows.mainloop()

    ## UPDATE BY DELETE LIST
    for city in delList:
        dfDestRawInfo = dfDestRawInfo[dfDestRawInfo[colCity] != city]

    ## ADD MARKER
    for _, row in dfDestRawInfo.iterrows():
        newCityLoc = get_locations(row[colCity], dfLocations)
        marker.lat = newCityLoc[0]
        marker.lon = newCityLoc[1]
        marker.popup = gen_marker_htmltxt(row, colDetail)
        memo.add_marker(marker.lat, marker.lon, marker.popup)
        mapBounds.append([marker.lat, marker.lon])

    ## SAVE MAP TO HTML
    dfDestRawInfo.to_csv(DATA_PATH, index=False)
    memo.fit_bounds(mapBounds)
    memo.save(MAP_OUTPUT_PATH)







