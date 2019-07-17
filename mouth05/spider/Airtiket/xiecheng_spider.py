"""
    携程测试
"""
import random
import re

import requests
import json
import csv

from tools import BS_LIST,CITY_CODE
from db_helper import DB_Connection

class XieChengSpider(object):
    # 初始化变量
    def __init__(self,dcity,acity,start_time,flightWay,return_time=None):
        """
            构造函数,初始化变量
        :param dcity: 始发地,str, e.g. 西安
        :param acity: 目的地,str, e.g. 上海
        :param time: 触发时间,data, e.g. 2019-07-18
        :param flightWay: 行程类型, str,单程 OneTrip 往返 Roundtrip
        """
        self.dcity=dcity
        self.acity=acity
        self.stime=start_time
        self.rtime=return_time
        self.flightWay=flightWay
        self.db = DB_Connection()
        self.headers = {
            'content-type': "application/json",
            # "cookie":'_RGUID=f6352a17-5b3b-4a3a-99a7-5c2df14a7d8a; _RSG=weqERTXArOFAsdInt2Ndc9; _RDG=2899759fc2affe201f09dbbc9ae8adb3ad; _abtest_userid=f008a055-0ed9-4503-b1ab-a8850a558476;',
            "content-type": "application/json",
            "origin": "https://flights.ctrip.com",
            "referer": "https://flights.ctrip.com/itinerary/roundtrip/sia-sha?date=2019-07-16,2019-07-17",
            "user-agent": random.choice(BS_LIST),
        }
        self.proxies = {
            "http": "http://212.64.51.13:8888",
            "https": "https://212.64.51.13:8888"
        }


    # 判断时间
    def _judge_time(self,date):
        # 判断输入时间格式
        if not re.match(r'\d{4}[-/.]\d{1,2}[-/.]\d{1,2}', date):
            raise NotImplementedError('日期输入错误')
        date = re.findall(r'\d+', date)
        # 判断时间
        if not (0 < int(date[1]) <= 12 and 0 < int(date[2]) <= 31):
            raise NotImplementedError('日期输入错误')
        ret_date = '-'.join(date)
        return ret_date


    # 读取城市信息
    def _get_city_info(self,city_name):
        city_data = self.db.get_city(city_name)
        if not city_data:
            raise NotImplementedError("城市输入错误")
        return city_data[2], city_data[3]



    # 设置提交POST的data数据
    def prepare_data(self):
        dcity_code, dcity_sign=self._get_city_info(self.dcity)
        acity_code, acity_sign=self._get_city_info(self.acity)
        strip_date=self._judge_time(self.stime)
        # 判断行程类型
        if self.flightWay not in ["Roundtrip","Onetrip"]:
            raise NotImplementedError('行程类型输入错误')
        # 往返程
        if self.flightWay == "Roundtrip":
            rtrip_date = self._judge_time(self.rtime)
            self.data = {
                "airportParams": [
                    {
                        "acity": "SHA",
                        "acityid": 2,
                        "acityname": "上海",
                        "date": "2019-07-17",
                        "dcity": "SIA",
                        "dcityid": 10,
                        "dcityname": "西安"
                    },
                    {
                        "acity": "SIA",
                        "acityid": 10,
                        "acityname": "西安",
                        "date": "2019-07-22",
                        "dcity": "SHA",
                        "dcityid": 2,
                        "dcityname": "上海"
                    }
                ],
                "classType": "ALL",
                "flightWay": "Roundtrip",
                "hasBaby": "false",
                "hasChild": "false",
                "searchIndex": 1
            }
        else:
            self.data = {
                "classType": "ALL",
                "flightWay": "Oneway",
                "hasBaby": "false",
                "hasChild": "false",
                "searchIndex": 1,
                "airportParams": [
                    {
                        "acity": "%s"%acity_sign,
                        "acityid": acity_code,
                        "acityname": "%s"%self.acity,
                        "date": "%s"%strip_date,
                        "dcity": "%s"%dcity_sign,
                        "dcityid": dcity_code,
                        "dcityname": "%s"%self.dcity,
                    }
                ]
            }


    # 保存城市信息
    def get_city_code(self):
        url = 'https://flights.ctrip.com/itinerary/api/poi/get'
        html = requests.get(url,headers=self.headers).json()
        print(html)
        for item in html['data'].values():
            try:
                for info in item.values():
                    for c_info in info:
                        print(c_info)
                        city = c_info["display"]
                        code = int(c_info['data'].split("|")[-2])
                        sign = c_info['data'].split("|")[-1]
                        try:
                            self.db.add_city(city, code, sign)
                        except Exception as e:
                            print(e)
            except Exception:
                continue


    # 获取航班信息
    def get_data(self):
        url="https://flights.ctrip.com/itinerary/api/12808/products"
        try:
            html=requests.post(url,data=json.dumps(self.data),headers=self.headers)
            print(html.status_code)
            html.raise_for_status()
        except Exception as e:
            print(e)
            raise NotImplementedError('爬取信息失败')
        else:
            trip_info = html.json()
            print(len(trip_info['data']['routeList']))
            with open('/home/tarena/1902chenning/mouth05/spider/Airtiket/trip.txt','w') as f:
                for item in trip_info['data']['routeList']:
                    airline_info=item['legs'][0]['flight']
                    print(airline_info)
                    writer=csv.writer(f)
                    writer.writerow([airline_info])
                    print("保存一个")


    def main(self):
        self.prepare_data()
        self.get_data()



if __name__ == '__main__':
    spider=XieChengSpider("西安",'北京','2019-07-17',"Roundtrip",return_time="2019-07-22")
    spider.main()







# airline_info={
#     'craftTypeKindDisplayName': '中型',
#     'arrivalAirportInfo': {
#         'airportName': '首都国际机场',
#         'terminal': {
#             'shortName': 'T3',
#             'id': 3,
#             'name': 'T3'
#         },
#         'cityName': '北京',
#         'airportTlc': 'PEK',
#         'cityTlc': 'BJS'
#     },
#     'sharedFlightName': None,
#     'durationDays': 0,
#     'departureAirportInfo': {
#         'airportName': '咸阳国际机场',
#         'terminal': {
#             'shortName': 'T2',
#             'id': 5,
#             'name': 'T2'
#         },
#         'cityName': '西安',
#         'airportTlc': 'XIY',
#         'cityTlc': 'SIA'
#     },
#     'specialCraft': False,
#     'oilFee': None,
#     'craftTypeName': '波音738',
#     'airlineName': '中国国航',
#     'punctualityRate': '',
#     'mealFlag': True,
#     'id': '620043474',
#     'tax': None,
#     'stopInfo': None,
#     'mealType': 'None',
#     'delayedTime': None,
#     'airlineCode': 'CA',
#     'stopTimes': 0,
#     'comfort': None,
#     'craftKind': 'M',
#     'sharedFlightNumber': '',
#     'craftTypeCode': '738',
#     'flightNumber': 'CA1224',
#     'arrivalDate': '2019-07-18 17:25:00',
#     'departureDate': '2019-07-18 15:30:00'
# }












