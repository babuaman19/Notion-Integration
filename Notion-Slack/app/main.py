from fastapi import FastAPI
from app.routes.slackbot_sync_route import router as slackbot_router


app = FastAPI()
app.include_router(slackbot_router)