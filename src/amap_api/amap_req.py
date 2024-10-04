import requests
import json


def get_amap_key():
    file = open(r'./src/amap_api/key', 'r')
    key = file.read().strip()
    file.close()
    return key

def get_locations_fromAmap(srcCity):
    key = get_amap_key()
    webReq = f'https://restapi.amap.com/v3/geocode/geo?address={srcCity}&output=json&key={key}'
    webRes = requests.get(webReq)
    print(webRes)
    if webRes.status_code == 200:
        retDict = webRes.json()
        retSrcList = retDict['geocodes'][0]['location'].split(',')
        return (float(retSrcList[1]), float(retSrcList[0]))
    else:
        print(f"请求失败，状态码: {webRes.status_code}")
