import tkinter as tk
from tkinter import messagebox
import requests
import json

def get_weather():
    city_dict = {
        "1": "Incheon",
        "경기도": "Incheon",
        "2": "Gangneung",
        "강원도": "Gangneung",
        "3": "Chungju",
        "충청북도": "Chungju",
        "4": "Seosan",
        "충청남도": "Seosan",
        "5": "Jeonju",
        "전라북도": "Jeonju",
        "6": "Gwangju",
        "전라남도": "Gwangju",
        "7": "Pohang",
        "경상북도": "Pohang",
        "8": "Busan",
        "경상남도": "Busan",
        "9": "Haenam",
        "제주도": "Haenam"
    }

    city_name = entry.get()
    if city_name in city_dict:
        city = city_dict[city_name]
        if city_name == "3" or city_name == "충청북도":
            messagebox.showwarning("Warning", "충청북도에는 바다가 없습니다.")
            pass

        try:
            response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=dbf786bcf59e435498d90619241306&q={city}&aqi=yes&lang=ko")
            jsonObj = json.loads(response.text)

            uv_index = jsonObj["current"]["uv"]
            uv_status = ""
            if uv_index < 3:
                uv_status = "낮음"
            elif 3 <= uv_index < 6:
                uv_status = "보통"
            elif 6 <= uv_index < 8:
                uv_status = "높음"
            elif 8 <= uv_index < 11:
                uv_status = "매우높음"
            else:
                uv_status = "위험"

            wind_speed = jsonObj["current"]["wind_kph"]
            wind_danger = wind_speed >= 50.4

            wind_direction = {
                "N": "북", "NNE": "북북동", "NE": "북동", "ENE": "동북동",
                "E": "동", "ESE": "동남동", "SE": "남동", "SSE": "남남동",
                "S": "남", "SSW": "남남서", "SW": "남서", "WSW": "서남서",
                "W": "서", "WNW": "서북서", "NW": "북서", "NNW": "북북서"
            }.get(jsonObj["current"]["wind_dir"], "")

            air_quality_index = jsonObj["current"]["air_quality"]["pm10"]
            air_quality = ""
            if 0 <= air_quality_index <= 30:
                air_quality = "좋음"
            elif 31 <= air_quality_index <= 80:
                air_quality = "보통"
            elif 81 <= air_quality_index <= 150:
                air_quality = "나쁨"
            elif 151 <= air_quality_index <= 250:
                air_quality = "매우나쁨"
            else:
                air_quality = "위험"

            last_updated = jsonObj["current"]["last_updated"]
            temp_c = jsonObj["current"]["temp_c"]
            feelslike_c = jsonObj["current"]["feelslike_c"]
            condition = jsonObj["current"]["condition"]["text"]
            humidity = jsonObj["current"]["humidity"]
            is_day = jsonObj["current"]["is_day"]

            swim_blacklist = ["흐린", "안개", "근처 곳곳에 비", "근처 곳곳에 눈", "근처 곳곳에 진눈깨비", "근처 곳곳에 동결 이슬비", "근처에 천둥 발생", "날리는 눈", "눈보라",
                             "동결 안개", "곳곳에 가벼운 이슬비", "가벼운 이슬비", "동결 이슬비", "심한 동결 이슬비", "곳곳에 가벼운 비", "가벼운 비", "때때로 보통 비", "보통 비",
                             "때때로 폭우", "폭우", "약간의 동결", "보통 또는 심한 동결 비", "가벼운 진눈깨비", "중간 또는 무거운 진눈깨비", "곳곳에 가벼운 눈", "가벼운 눈",
                             "곳곳에 적당한 눈", "보통 눈", "곳곳에 폭설", "폭설", "아이스 펠렛", "가벼운 소나기", "보통 또는 심한 소나기", "호우", "가벼운 진눈깨비 소나기",
                             "보통 또는 심한 진눈깨비 소나기", "가벼운 폭설", "보통 또는 심한 폭설", "가벼운 얼음 알갱이 샤워", "보통 또는 심한 얼음 알갱이 샤워",
                             "천둥을 동반한 지역 곳곳의 가벼운 비", "천둥을 동반한 보통 또는 심한 비", "천둥을 동반한 지역 곳곳의 가벼운 눈", "천둥을 동반한 보통 또는 눈"]

            weather_info = f"\n{last_updated}에 기상 정보 업데이트됨\n\n"
            weather_info += f"{city_name}번 도시의 현재 기온은 {temp_c}°C, 체감 온도는 {feelslike_c}°C 입니다.\n"
            weather_info += f"기상상태: {condition}\n"
            weather_info += f"미세먼지: {air_quality} ({air_quality_index}µg/m³)\n"
            weather_info += f"자외선 지수: {uv_status} ({uv_index} / 11)\n"
            weather_info += f"풍속: {wind_speed}km/h ({wind_direction})\n"
            weather_info += f"습도: {humidity}%\n\n"

            if is_day == 0:
                weather_info += "야간입니다. 해수욕하기 적합하지 않습니다.\n"
            if temp_c <= 25:
                weather_info += "기온이 낮습니다. 해수욕하기 적합하지 않습니다.\n"
            if condition in swim_blacklist:
                weather_info += "기상상태 악화로 해수욕하기 적합하지 않습니다.\n"
            if air_quality_index >= 150:
                weather_info += "미세먼지가 매우 나쁩니다. 해수욕하기 적합하지 않습니다.\n"
            if wind_danger:
                weather_info += "강풍주의보가 발령되었습니다. 해수욕하기 적합하지 않습니다.\n"
            if temp_c >= 25 and condition not in swim_blacklist and is_day == 1 and not wind_danger and air_quality_index <= 151:
                weather_info += "해수욕하기 좋은 날씨입니다.\n"

            result_label.config(text=weather_info)

        except Exception as e:
            messagebox.showerror("Error", f"에러가 발생하였습니다. 다시 시도해 주세요.\n에러 코드: {e}")
    else:
        messagebox.showwarning("Warning", "올바른 번호 또는 지역명을 입력하세요.")

root = tk.Tk()
root.title("해수욕장 기상 정보")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

info_label = tk.Label(frame, text="가고자 하는 해수욕장의 지역을 입력하세요...\n1. 경기도\n2. 강원도\n3. 충청북도\n4. 충청남도\n5. 전라북도\n6. 전라남도\n7. 경상북도\n8. 경상남도\n9. 제주도")
info_label.pack()

entry = tk.Entry(frame, width=20)
entry.pack(pady=10)

get_weather_button = tk.Button(frame, text="확인", command=get_weather)
get_weather_button.pack(pady=5)

result_label = tk.Label(frame, text="", justify="left")
result_label.pack(pady=10)

root.mainloop()
