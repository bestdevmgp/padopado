import requests, json, os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, ttk

load_dotenv()

api_key = os.getenv('API_KEY')

def get_weather_data(city):
    try:
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes&lang=ko")
        jsonObj = json.loads(response.text)
        return jsonObj
    except Exception as e:
        messagebox.showerror("Error", f"에러가 발생하였습니다. 다시 시도해 주세요.\n에러 코드: {e}")
        return None

def update_weather():
    inputVal = region_var.get()
    city_map = {
        "경기도": "Incheon",
        "강원도": "Gangneung",
        "충청북도": "Chungju",
        "충청남도": "Seosan",
        "전라북도": "Jeonju",
        "전라남도": "Gwangju",
        "경상북도": "Pohang",
        "경상남도": "Busan",
        "제주도": "Haenam"  # 제주도의 경우 Haenam으로 대체
    }

    if inputVal not in city_map:
        messagebox.showwarning("Warning", "잘못된 지역입니다.")
        return

    city = city_map[inputVal]
    weather_data = get_weather_data(city)

    if weather_data:
        display_weather(weather_data, inputVal)

def display_weather(data, region_name):
    uv_index = data["current"]["uv"]
    wind_speed = data["current"]["wind_kph"]
    wind_dir = data["current"]["wind_dir"]
    air_quality = data["current"]["air_quality"]["pm10"]
    temp = data["current"]["temp_c"]
    feels_like = data["current"]["feelslike_c"]
    condition = data["current"]["condition"]["text"]
    last_updated = data["current"]["last_updated"]
    humidity = data["current"]["humidity"]
    is_day = data["current"]["is_day"]

    uv_status = "낮음" if uv_index < 3 else "보통" if uv_index < 6 else "높음" if uv_index < 8 else "매우높음" if uv_index < 11 else "위험"
    wind_directions = {
        "N": "북", "NNE": "북북동", "NE": "북동", "ENE": "동북동", "E": "동", "ESE": "동남동", "SE": "남동", "SSE": "남남동",
        "S": "남", "SSW": "남남서", "SW": "남서", "WSW": "서남서", "W": "서", "WNW": "서북서", "NW": "북서", "NNW": "북북서"
    }
    wind_direction = wind_directions.get(wind_dir, wind_dir)
    air_quality_status = "좋음" if air_quality <= 30 else "보통" if air_quality <= 80 else "나쁨" if air_quality <= 150 else "매우나쁨" if air_quality <= 250 else "위험"

    result_text = f"""
    {last_updated}에 기상 정보 업데이트됨

    {region_name}의 현재 기온은 {temp}°C, 체감 온도는 {feels_like}°C 입니다.
    기상상태: {condition}
    미세먼지: {air_quality_status} ({air_quality}µg/m³)
    자외선 지수: {uv_status} ({uv_index} / 11)
    풍속: {wind_speed} km/h ({wind_direction})
    습도: {humidity}%
    """

    swimBlackList = ["흐린", "안개", "근처 곳곳에 비", "근처 곳곳에 눈", "근처 곳곳에 진눈깨비", "근처 곳곳에 동결 이슬비", "근처에 천둥 발생", "날리는 눈", "눈보라",
                     "동결 안개", "곳곳에 가벼운 이슬비", "가벼운 이슬비", "동결 이슬비", "심한 동결 이슬비", "곳곳에 가벼운 비", "가벼운 비", "때때로 보통 비", "보통 비",
                     "때때로 폭우", "폭우", "약간의 동결", "보통 또는 심한 동결 비", "가벼운 진눈깨비", "중간 또는 무거운 진눈깨비", "곳곳에 가벼운 눈", "가벼운 눈",
                     "곳곳에 적당한 눈", "보통 눈", "곳곳에 폭설", "폭설", "아이스 펠렛", "가벼운 소나기", "보통 또는 심한 소나기", "호우", "가벼운 진눈깨비 소나기",
                     "보통 또는 심한 진눈깨비 소나기", "가벼운 폭설", "보통 또는 심한 폭설", "가벼운 얼음 알갱이 샤워", "보통 또는 심한 얼음 알갱이 샤워",
                     "천둥을 동반한 지역 곳곳의 가벼운 비", "천둥을 동반한 보통 또는 심한 비", "천둥을 동반한 지역 곳곳의 가벼운 눈", "천둥을 동반한 보통 또는 눈"]

    if is_day == 0:
        result_text += "\n야간입니다. 해수욕하기 적합하지 않습니다."
    if temp <= 25:
        result_text += "\n기온이 낮습니다. 해수욕하기 적합하지 않습니다."
    if condition in swimBlackList:
        result_text += "\n기상상태 악화로 해수욕하기 적합하지 않습니다."
    if air_quality >= 150:
        result_text += "\n미세먼지가 매우 나쁩니다. 해수욕하기 적합하지 않습니다."
    if wind_speed >= 50.4:
        result_text += "\n강풍주의보가 발령되었습니다. 해수욕하기 적합하지 않습니다."
    if temp >= 25 and condition not in swimBlackList and is_day == 1 and wind_speed < 50.4 and air_quality < 150:
        result_text += "\n해수욕하기 좋은 날씨입니다."

    result_label.config(text=result_text, font=("Arial", 14))

# GUI 설정
root = tk.Tk()
root.title("해수욕장 날씨 정보")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="가고자 하는 해수욕장의 지역을 선택하세요:", font=("Arial", 14))
label.pack(pady=10)

regions = ["경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]
region_var = tk.StringVar()
region_combo = ttk.Combobox(frame, textvariable=region_var, values=regions, state="readonly", font=("Arial", 14))
region_combo.pack(pady=10)

button = ttk.Button(frame, text="날씨 정보 조회", command=update_weather)
button.pack(pady=10)

result_label = ttk.Label(frame, text="", font=("Arial", 14), background="#ffffff", relief=tk.SOLID, anchor="nw", justify="left")
result_label.pack(fill=tk.BOTH, expand=True, pady=10)

root.mainloop()
