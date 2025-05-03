import os
import json
import time
import schedule
from slack_sdk import WebClient
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = "last_timestamp.json"

class SlackBotService:
    def __init__(self):
        self.slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.pinecone_index = pc.Index(os.getenv("PINECONE_INDEX", "unified-search"))
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")

    def _load_last_timestamp(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f).get("last_ts", "0")
        return "0"

    def _save_last_timestamp(self, ts):
        with open(STATE_FILE, "w") as f:
            json.dump({"last_ts": ts}, f)

    def _embed_text(self, text):
        response = self.openai_client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def _fetch_new_messages(self, latest_ts):
        try:
            response = self.slack_client.conversations_history(
                channel=self.channel_id,
                oldest=latest_ts,
                limit=100
            )
            return response.get("messages", [])
        except Exception as e:
            print(f"Slack API error: {e}")
            return []

    def _upsert_to_pinecone(self, messages):
        vectors = []
        for msg in messages:
            if "text" not in msg:
                continue
            embedding = self._embed_text(msg["text"])
            vectors.append({
                "id": msg["ts"],
                "values": embedding,
                "metadata": {"text": msg["text"]}
            })
        if vectors:
            self.pinecone_index.upsert(vectors)

    def process_and_upsert(self):
        latest_ts = self._load_last_timestamp()
        messages = self._fetch_new_messages(latest_ts)
        messages_to_insert = [msg for msg in messages if msg["ts"] > latest_ts]

        if not messages_to_insert:
            return {
                "status": "no_new_messages",
                "message_count": 0,
                "message": "No new messages to upsert.",
                "upserted_messages": []
            }

        self._upsert_to_pinecone(messages_to_insert)
        new_latest_ts = max(msg["ts"] for msg in messages_to_insert)
        self._save_last_timestamp(new_latest_ts)

        return {
            "status": "success",
            "message_count": len(messages_to_insert),
            "message": "Upserted messages to Pinecone.",
            "latest_ts": new_latest_ts,
            "upserted_messages": [
                {
                    "text": msg.get("text", "")[:200],
                    "timestamp": msg.get("ts"),
                    "user": msg.get("user", "unknown")
                }
                for msg in messages_to_insert
            ]
        }

# ----------------------------
# Scheduler appended below
# ----------------------------

def job():
    bot_service = SlackBotService()
    result = bot_service.process_and_upsert()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {result['message']} ({result['message_count']} messages)")

if __name__ == "__main__":
    schedule.every(30).minutes.do(job)
    print("SlackBotService scheduler started. Running every 30 minutes.")
    job()  # Optional: run immediately once
    while True:
        schedule.run_pending()
        time.sleep(1)
