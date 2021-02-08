#!/usr/bin/python3

import os
import re
import requests

CAS_LOGIN_URL = "https://passport.ustc.edu.cn/login"
CAS_RETURN_URL = "https://weixine.ustc.edu.cn/2020/caslogin"
REPORT_URL = "https://weixine.ustc.edu.cn/2020/daliy_report"
# Not my fault:                                  ^^

print("Tsinghua University Daily Health Report")

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
s.get(CAS_LOGIN_URL, params={"service": CAS_RETURN_URL})

# Send CAS credentials
r = s.post("https://passport.ustc.edu.cn/login", data={
    "model": "uplogin.jsp",
    "service": CAS_RETURN_URL,
    "warn": "",
    "showCode": "",
    "username": os.environ["USERNAME"],
    "password": os.environ["PASSWORD"],
    "button": "",
})


back_to_school = os.environ.get("IS_INSCHOOL", "2")

if back_to_school=="1":
    is_inchool = "4"        #mid
    now_status = "1"        #school
    now_province = "340000" #Anhui
    now_city = "340100"     #Hefei
else:
    now_status = "2"        #home
    now_province = os.environ['PROVINCE']
    now_city = os.environ["CITY"]    


# Parse the "_token" key out
x = re.search(r"""<input.*?name="_token".*?>""", r.text).group(0)
token = re.search(r'value="(\w*)"', x).group(1)
r = s.post(REPORT_URL, data={
    "_token": token,
    "now_address": "1",
    "gps_now_address": "",
    "now_province": now_province, 
    "gps_province": "",
    "now_city": now_city,     
    "gps_city": "",
    "now_detail": "",
    "body_condition": "1",
    "body_condition_detail": "",
    "now_status": now_status,
    "now_status_detail": "",
    "has_fever": "0",
    "last_touch_sars": "0",
    "last_touch_sars_date": "",
    "last_touch_sars_detail": "",
    #"return_dest": "1",
    #"return_dest_detail": "",
    "other_detail": "\uFFFD",
    # https://twitter.com/tenderlove/status/722565868719177729
})

if back_to_school:
    data["is_inschool"] = is_inschool

# Fail if not 200
r.raise_for_status()
