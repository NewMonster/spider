#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : spider_test.py
@Time    : 2019-7-16 下午6:10
@version : v1.0
"""

import requests
import json


data={
    "airportParams":[
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

headers = {
    'content-type': "application/json",
    "content-type": "application/json",
    "origin": "https://flights.ctrip.com",
    "referer": "https://flights.ctrip.com/itinerary/roundtrip/sia-sha?date=2019-07-16,2019-07-17",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
proxies = {
    "http": "http://212.64.51.13:8888",
    "https": "https://212.64.51.13:8888"
}
import csv

url="https://flights.ctrip.com/itinerary/api/12808/products"
html=requests.post(url,data=json.dumps(data),headers=headers)
print(html.status_code)

trip_info=html.json()

print(len(trip_info['data']['routeList']))

with open('/home/tarena/1902chenning/mouth05/spider/Airtiket/trip.txt', 'w') as f:
    for item in trip_info['data']['routeList']:
        airline_info = item['legs'][0]['flight']
        print(airline_info)
        writer = csv.writer(f)
        writer.writerow([airline_info])
        print("保存一个")







a={
    'sharedFlightNumber': 'HO1214',
    'arrivalDate': '2019-07-17 17:00:00',
    'departureDate': '2019-07-17 14:30:00',
    'craftTypeKindDisplayName': '中型',
    'flightNumber': 'MU4750',
     'airlineCode': 'MU',
     'sharedFlightName': '吉祥航空',
     'craftTypeCode': '320',
     'airlineName': '东方航空',
     'craftTypeName': '空客320',
     'id': '107145458',
     'durationDays': 0,
}

























