import re
import requests
from lxml import etree
from loginer import Loginer

class SeatGetter:
    def __init__(self,student_id):
        self.student_id = student_id
        self.session = None 
        self.headers = {
            'Proxy-Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
            }
        self.room_urls = {
            '2s': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=1&fid=1',
            '2n': '',
            '3s': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=6&fid=3',
            '3n': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=5&fid=4',
            '4s': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=3&fid=5',
            '4n': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=4&fid=6',
            '3g1': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=13&fid=9',
            '3g2': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=14&fid=9',
            '4g1': 'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=15&fid=10',
            '4g2':'http://libzwxt.ahnu.edu.cn/SeatWx/Room.aspx?rid=16&fid=10',
            }

   
    def _get_session(self):
        loginer = Loginer(self.student_id, self.student_id)
        self.session = loginer.login()

    def choose_seat(self,room_code):
        self._get_session()
        try:
            room_url = self.room_urls[room_code]
            response = self.session.get(url=room_url, headers=self.headers)
            html = etree.HTML(response.text)
            lxml_pattern = "//div[@class='seat']//li"
            seats_list = []
            seats = html.xpath(lxml_pattern)
            for seat in seats:
                seat_state = ''.join(seat.xpath("@data-state"))
                if seat_state == '0':
                    seat_url = ''.join(seat.xpath("./a/@href"))
                    seat_code = re.search(r'sid=(\d*)\b', seat_url).group(1)
                    seats_list.append(seat_code)

        except:
            return False
        return room_url, seats_list