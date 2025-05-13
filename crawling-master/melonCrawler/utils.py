# melon_crawler/utils.py

def filterValidData(data: dict) -> bool:
    title = data.get('title', '')
    sdate = data.get('sdate', '')
    edate = data.get('edate', '')
    return "정보 없음" not in title and sdate and edate
