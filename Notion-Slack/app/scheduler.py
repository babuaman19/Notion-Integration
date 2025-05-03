import time
import schedule
from services.slackbot_service import SlackBotService


def job():
    try:
        print("[INFO] Running scheduled job...")
        bot_service = SlackBotService()
        result = bot_service.process_and_upsert()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {result['message']} ({result['message_count']} messages)")
    except Exception as e:
        print(f"[ERROR] Scheduled job failed: {e}")


def main():
    schedule.every(30).minutes.do(job)
    print("[INFO] SlackBotService scheduler started. Running every 30 minutes.")
    job()  # Optional: run immediately once

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
