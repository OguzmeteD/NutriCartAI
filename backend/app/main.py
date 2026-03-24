from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents import configure_langfuse_tracing
from app.routers import auth, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_langfuse_tracing()  # wire OTel → Langfuse once at startup
    yield


app = FastAPI(title="NutriCartAI", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(chat.router)
