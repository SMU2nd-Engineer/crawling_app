from interparkCrawler.interparkCrawler import save_interpark_to_excel
from melonCrawler.melonCrawler import melonCrawler
from ticketlinkCrawler.ticketlinkCrawler import ticketlinkCrawler
import traceback

def main():
    try:
        print("Interpark 크롤링을 진행 합니다.")
        save_interpark_to_excel()
        print("Interpark 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Interpark 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

    try:
        print("Melon 크롤링을 진행 합니다.")
        melonCrawler()
        print("Melon 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Melon 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

    try:
        print("Ticketlink 크롤링을 진행 합니다.")
        ticketlinkCrawler()
        print("Ticketlink 크롤링이 완료 되었습니다.\n")
    except Exception as e:
        print("Ticketlink 크롤링 중 오류가 발생했습니다.")
        print(f"에러: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()