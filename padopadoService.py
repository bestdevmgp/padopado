#API 제공: https://www.weatherapi.com
import requests, json, os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
succeed = bool()  # 프로그램 정상 실행 확인
while True:  # 에러 발생 시 재시작
    if succeed:  # 정상 종료 시 break
        break
    info = """
    가고자 하는 해수욕장의 지역을 입력하세요...
    1. 경기도
    2. 강원도
    3. 충청북도
    4. 충청남도
    5. 전라북도
    6. 전라남도
    7. 경상북도
    8. 경상남도
    9. 제주도
    """

    print(info)
    inputVal = input("번호 또는 지역명을 입력하세요 >>> ")
    isOk = True  # 예외 처리 관련 변수
    cityName = ""  # API로 전달할 도시 이름(영문)
    cityName2 = ""  # 출력할 도시 이름(한글)

    try:  # 발생하는 모든 에러 예외 처리
        if inputVal == "1" or inputVal == "경기도":  # API로 불러올 지역 - 인천
            cityName = "Incheon"
            cityName2 = "경기도"
        elif inputVal == "2" or inputVal == "강원도":  # API로 불러올 지역 - 강릉
            cityName = "Gangneung"
            cityName2 = "강원도"
        elif inputVal == "3" or inputVal == "충청북도":  # API로 불러올 지역 - 충주
            cityName = "Chungju"
            cityName2 = "충청북도"
            print("충청북도에는 바다가 없습니다.\n")
        elif inputVal == "4" or inputVal == "충청남도":  # API로 불러올 지역 - 서산
            cityName = "Seosan"
            cityName2 = "충청남도"
        elif inputVal == "5" or inputVal == "전라남도":  # API로 불러올 지역 - 전주
            cityName = "Jeonju"
            cityName2 = "전라북도"
        elif inputVal == "6" or inputVal == "전라남도":  # API로 불러올 지역 - 광주
            cityName = "Gwangju"
            cityName2 = "전라남도"
        elif inputVal == "7" or inputVal == "경상북도":  # API로 불러올 지역 - 포항
            cityName = "Pohang"
            cityName2 = "경상북도"
        elif inputVal == "8" or inputVal == "경상남도":  # API로 불러올 지역 - 부산
            cityName = "Busan"
            cityName2 = "경상남도"
        elif inputVal == "9" or inputVal == "제주도":  # API로 불러올 지역 - 해남
            cityName = "Haenam"  # API에 제주도 날씨 정보가 없어 해남으로 대체
            cityName2 = "제주도"

        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q=" + cityName + "&aqi=yes&lang=ko")
        jsonObj = json.loads(response.text)

        # 자외선 지수 확인
        uv_status = ""
        if jsonObj["current"]["uv"] < 3:
            uv_status = "낮음"
        elif 3 <= jsonObj["current"]["uv"] < 6:
            uv_status = "보통"
        elif 6 <= jsonObj["current"]["uv"] < 8:
            uv_status = "높음"
        elif 8 <= jsonObj["current"]["uv"] < 11:
            uv_status = "매우높음"
        elif 11 <= jsonObj["current"]["uv"]:
            uv_status = "위험"

        # 풍속 확인
        wind_danger = 0  # 풍속 주의보 발령 시 1
        if jsonObj["current"]["wind_kph"] >= 50.4:
            wind_danger = 1

        # 풍향 확인
        wind_direction = ""
        if jsonObj["current"]["wind_dir"] == "N":
            wind_direction = "북"
        elif jsonObj["current"]["wind_dir"] == "NNE":
            wind_direction = "북북동"
        elif jsonObj["current"]["wind_dir"] == "NE":
            wind_direction = "북동"
        elif jsonObj["current"]["wind_dir"] == "ENE":
            wind_direction = "동북동"
        elif jsonObj["current"]["wind_dir"] == "E":
            wind_direction = "동"
        elif jsonObj["current"]["wind_dir"] == "ESE":
            wind_direction = "동남동"
        elif jsonObj["current"]["wind_dir"] == "SE":
            wind_direction = "남동"
        elif jsonObj["current"]["wind_dir"] == "SSE":
            wind_direction = "남남동"
        elif jsonObj["current"]["wind_dir"] == "S":
            wind_direction = "남"
        elif jsonObj["current"]["wind_dir"] == "SSW":
            wind_direction = "남남서"
        elif jsonObj["current"]["wind_dir"] == "SW":
            wind_direction = "남서"
        elif jsonObj["current"]["wind_dir"] == "WSW":
            wind_direction = "서남서"
        elif jsonObj["current"]["wind_dir"] == "W":
            wind_direction = "서"
        elif jsonObj["current"]["wind_dir"] == "WNW":
            wind_direction = "서북서"
        elif jsonObj["current"]["wind_dir"] == "NW":
            wind_direction = "북서"
        elif jsonObj["current"]["wind_dir"] == "NNW":
            wind_direction = "북북서"

        # 미세먼지 지수 확인
        air_quality = ""
        if 0 <= jsonObj["current"]["air_quality"]["pm10"] <= 30:
            air_quality = "좋음"
        elif 31 <= jsonObj["current"]["air_quality"]["pm10"] <= 80:
            air_quality = "보통"
        elif 81 <= jsonObj["current"]["air_quality"]["pm10"] <= 150:
            air_quality = "나쁨"
        elif 151 <= jsonObj["current"]["air_quality"]["pm10"] <= 250:
            air_quality = "매우나쁨"
        elif 251 <= jsonObj["current"]["air_quality"]["pm10"]:
            air_quality = "위험"

        # 출력
        print(f"\n\033[97m{jsonObj["current"]["last_updated"]}\033[0m에 기상 정보 업데이트됨\n")
        print(f"{cityName2}의 현재 기온은 \033[97m{jsonObj["current"]["temp_c"]}\033[0m°C, 체감 온도는 \033[97m{jsonObj["current"]["feelslike_c"]}\033[0m°C 입니다.")
        print(f"기상상태: \033[97m{jsonObj["current"]["condition"]["text"]}\033[0m")
        print(f"미세먼지: \033[97m{air_quality}\033[0m ({jsonObj["current"]["air_quality"]["pm10"]}µg/m³)")
        print(f"자외선 지수: \033[97m{uv_status}\033[0m ({jsonObj["current"]["uv"]} / 11)")
        print(f"풍속: \033[97m{jsonObj["current"]["wind_kph"]}\033[0mkm/h ({wind_direction})")
        print(f"습도: \033[97m{jsonObj["current"]["humidity"]}\033[0m%\n")

        # 해수욕이 불가한 기상 상태
        swimBlackList = ["흐린", "안개", "근처 곳곳에 비", "근처 곳곳에 눈", "근처 곳곳에 진눈깨비", "근처 곳곳에 동결 이슬비", "근처에 천둥 발생", "날리는 눈", "눈보라",
                         "동결 안개", "곳곳에 가벼운 이슬비", "가벼운 이슬비", "동결 이슬비", "심한 동결 이슬비", "곳곳에 가벼운 비", "가벼운 비", "때때로 보통 비", "보통 비",
                         "때때로 폭우", "폭우", "약간의 동결", "보통 또는 심한 동결 비", "가벼운 진눈깨비", "중간 또는 무거운 진눈깨비", "곳곳에 가벼운 눈", "가벼운 눈",
                         "곳곳에 적당한 눈", "보통 눈", "곳곳에 폭설", "폭설", "아이스 펠렛", "가벼운 소나기", "보통 또는 심한 소나기", "호우", "가벼운 진눈깨비 소나기",
                         "보통 또는 심한 진눈깨비 소나기", "가벼운 폭설", "보통 또는 심한 폭설", "가벼운 얼음 알갱이 샤워", "보통 또는 심한 얼음 알갱이 샤워",
                         "천둥을 동반한 지역 곳곳의 가벼운 비", "천둥을 동반한 보통 또는 심한 비", "천둥을 동반한 지역 곳곳의 가벼운 눈", "천둥을 동반한 보통 또는 눈"]

        # 야간인지 확인 후 출력
        if jsonObj["current"]["is_day"] == 0:
            print("\033[91m" + "야간입니다. 해수욕하기 적합하지 않습니다." + "\033[0m")

        # 저기온 확인 후 출력
        if jsonObj["current"]["temp_c"] <= 25:
            print("\033[91m" + "기온이 낮습니다. 해수욕하기 적합하지 않습니다." + "\033[0m")

        # 기상상태 확인 후 출력
        if jsonObj["current"]["condition"]["text"] in swimBlackList:
            print("\033[91m" + "기상상태 악화로 해수욕하기 적합하지 않습니다." + "\033[0m")

        # 미세먼지 지수 확인 후 출력
        if jsonObj["current"]["air_quality"]["pm10"] >= 150:
            print("\033[91m" + "미세먼지가 매우 나쁩니다. 해수욕하기 적합하지 않습니다." + "\033[0m")

        # 강풍 주의보 발령 확인 후 출력
        if wind_danger == 1:
            print("\033[91m" + "강풍주의보가 발령되었습니다. 해수욕하기 적합하지 않습니다." + "\033[0m")

        # 위험요소 없을 때
        if jsonObj["current"]["temp_c"] >= 25 and jsonObj["current"]["condition"]["text"] not in swimBlackList and jsonObj["current"]["is_day"] == 1 and wind_danger == 0 and jsonObj["current"]["air_quality"]["pm10"] <= 151:
            print("\033[94m해수욕하기 좋은 날씨입니다.\033[0m")

        succeed = True  # 정상 실행됨

    # 예외 처리
    except Exception as e:
        errorCode = str(e)
        print(f"\033[90m에러가 발생하였습니다. 다시 시도해 주세요.\n에러 코드: {errorCode}\033[0m")  # 에러 코드 출력
        isOk = False
