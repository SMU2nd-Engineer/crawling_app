# melon_crawler/utils.py

def filterValidData(data: dict) -> bool:
    title = data.get('title', '')
    sdate = data.get('sdate', '')
    edate = data.get('edate', '')
    return "정보 없음" not in title and sdate and edate

GRENE = {
    "뮤지컬" : 3002,
    "콘서트" : 3001,
    "클래식": 3005,
    "아동/가족" : 3006,
    "연극" : 3003,
    "전시" : 3004,
    "레저" : 3007,
    "기타" : 3001
}

def greneToCode(grene) :
    try:
      return GRENE[grene]
    except:
      return "" 