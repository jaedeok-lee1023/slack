import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-01-01",  # 신정
    "2026-02-16",  # 설 연휴
    "2026-02-17",  # 설날
    "2026-02-18",  # 설 연휴
    "2026-03-02",  # 대체공휴일
    "2026-05-05",  # 어린이날
    "2026-05-25",  # 대체공휴일
    "2026-06-03",  # 지방선거
    "2026-08-17",  # 대체공휴일
    "2026-09-24",  # 추석 연휴
    "2026-09-25",  # 추석
    "2026-10-05",  # 대체공휴일
    "2026-10-09",  # 한글날
    "2026-12-25",  # 크리스마스
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f"*[공지｜클러스터 內 시설물 관리 협조 안내]*\n\n\n"

        notice_msg = (
            f"1. 중요도 : 중\n"
            f"2. 대상 : 평택 클러스터 임직원 전체\n"
            f"3. 주요 내용\n\n"
            f"안녕하세요? 평택 클러스터 구성원 여러분!\n\n"
            f"건강하고 안전한 클러스터 운영을 위해\n"
            f"아래와 같이 구성원 여러분의 협조를 요청드리오니\n"
            f"반드시 확인 후 준수하여 주시기 바랍니다.\n\n"
            f"\n"
            f":k체크: 수도 동파 및 온도 저하 우려로 출입문과 오버헤드도어 는 *꼭 사용 후 폐쇄* 바랍니다.\n"
            f":k체크: 냉기 유출로 인한 상품 변질 등 우려로 냉장 / 냉동 방열도어 (챔버) 는 *꼭 사용 후 폐쇄* 바랍니다.\n"
            f":k체크: 1번 / 7번 게이트 외부 (도로) <-> 복도 출입문 은 *꼭 사용 후 폐쇄* 바랍니다.\n"
            f":k체크: 전열기구는 관리실에서 확인 후 사용, 그 외 *비인가 전열기구는 사용 금지* 바랍니다.\n"
            f":k체크: 각 층 사무실,휴게공간 미 사용 콘센트, 냉난방기기 (에어컨 등) 는 *미 사용 시 OFF* 바랍니다.\n\n"
            f"\n"
            f"관련 시설물 이슈 발생 시 아래 채널 이용 부탁드립니다.\n\n"
            f" *<#C05NVF78M8S|11_시설안전이슈_평택>* \n\n"
            f"\n"
            f"*:slack: 문의사항 : 인사총무팀 총무/시설 담당자*\n\n"
            f"감사합니다.\n"
        )
 
        # 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
