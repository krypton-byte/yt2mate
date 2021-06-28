from io import BytesIO
from requests import Session
import re, requests
from bs4 import BeautifulSoup
k__id = lambda text:re.search("var k__id = \"([0-9a-zA-Z]{1,})\"",text).group(1)
k_data_id = lambda text:re.search("data\-id\=\"(.*?)\"", text).group(1)
class video:
    def __init__(self, format, reso, v__id, size, k_data) -> None:
        self.format = format
        self.reso = reso
        self.v_id = v__id
        self.size = size
        self.k_data_id = k_data
    @property
    def get_json(self):
        data = {
            "type": "youtube",
            "_id": self.v_id,
            "v_id": self.k_data_id,
            "ajax": 1,
            "token": None,
            "ftype": self.format,
            "fquality": self.reso
            }
        res= requests.post("https://www.y2mate.com/mates/en68/convert", data = data).json()
        return {"url":re.search("\"(https?:.*?)\"",res['result']).group(1).replace("\\", ""), "size":self.size, "reso":self.reso, "format":self.format}
    def download(self, file):
        if isinstance(str, file):
            open(file, "wb").write(requests.get(self.get_json["url"]).content)
        else:
            return BytesIO(requests.get(self.get_json["url"]).content)
    def __repr__(self) -> str:
        return f"<[Format: {self.format} Reso: {self.reso}]>"
    def __str__(self) -> str:
        return self.__repr__()
def videos(url):
    req = Session()
    res=req.post("https://www.y2mate.com/mates/en68/analyze/ajax", data={"url": url,"q_auto": 0,"ajax": 1})
    id_ = k__id(res.json()["result"])
    return [ video(y,z,id_,x, k_data_id(res.json()["result"])) for x, y, z in re.findall("\>([0-9]{1,}.?[0-9]? MB).*?data-ftype=\"(.*?)\" data-fquality\=\"(.*?)\"", res.json()["result"])]
def mp3(url):
    req=Session()
    if (res:=req.post("https://www.y2mate.com/mates/mp3/ajax",data={'url': url, 'q_auto': 1, 'ajax': 1}).json()).get("status") == 'success':
        if (bs:=BeautifulSoup(res["result"], "html.parser").find_all("input", attrs={"type":"hidden"})):
            if (res2:=req.post("https://www.y2mate.com/mates/mp3Convert", data={"type":"youtube", "_id":re.findall('var k__id = "(.*?)"', res["result"])[0], "v_id":bs[0].get("data-id"), "ajax":1, "token":"", "ftype":"mp3", "fquality":128}).json())["status"] == 'success':
                return {"thumbnail":BeautifulSoup(res["result"], "html.parser").div(attrs={"class":"video-thumbnail"})[0].img["src"],"title":BeautifulSoup(res["result"], 'html.parser').div(attrs={"class":"caption text-left"})[0].b.text,"url":BeautifulSoup(res2["result"]).a["href"], "duration":BeautifulSoup(res["result"], "html.parser").div(attrs={"class":"caption text-left"})[0].p.text[10:], "filesize":int(requests.get(BeautifulSoup(res2["result"]).a["href"], stream=True).headers["Content-Length"])}
