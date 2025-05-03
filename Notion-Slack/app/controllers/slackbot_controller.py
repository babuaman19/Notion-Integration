from app.services.slackbot_service import SlackBotService

class SlackBotController:
    def __init__(self):
        self.service = SlackBotService()

    def handle_query(self, query: str):
        return self.service.fetch_and_respond(query)