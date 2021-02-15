from requests import Session
import re, requests
from bs4 import BeautifulSoup
def mp3(url):
    req=Session()
    if (res:=req.post("https://www.y2mate.com/mates/mp3/ajax",data={'url': url, 'q_auto': 1, 'ajax': 1}).json()).get("status") == 'success':
        if (bs:=BeautifulSoup(res["result"], "html.parser").find_all("input", attrs={"type":"hidden"})):
            if (res2:=req.post("https://www.y2mate.com/mates/mp3Convert", data={"type":"youtube", "_id":re.findall('var k__id = "(.*?)"', res["result"])[0], "v_id":bs[0].get("data-id"), "ajax":1, "token":"", "ftype":"mp3", "fquality":128}).json())["status"] == 'success':
                return {"title":BeautifulSoup(res["result"], 'html.parser').div(attrs={"class":"caption text-left"})[0].b.text,"url":BeautifulSoup(res2["result"]).a["href"], "duration":BeautifulSoup(res["result"], "html.parser").div(attrs={"class":"caption text-left"})[0].p.text[10:], "filesize":int(requests.get(BeautifulSoup(res2["result"]).a["href"], stream=True).headers["Content-Length"])}
