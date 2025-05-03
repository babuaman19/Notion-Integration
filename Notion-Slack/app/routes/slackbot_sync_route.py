from fastapi import APIRouter
from app.services.slackbot_service import SlackBotService

router = APIRouter()
service = SlackBotService()

@router.post("/slackbot/sync")
def sync_slack_to_pinecone():
    return service.process_and_upsert()