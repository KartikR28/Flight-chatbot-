from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError, DBAPIError
import openai

from app.session_manager import get_session, save_session
from app.openai_handler import chat

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str


ERROR_MESSAGES = {
    "auth":       "AI service error: Invalid API key. Please check your configuration.",
    "ratelimit":  "AI service error: Rate limit reached. Please wait a moment and try again.",
    "ai_conn":    "AI service is unreachable right now. Please check your internet connection and try again.",
    "ai_general": "AI service returned an unexpected error. Please try again.",
    "db":         "Database connection issue. Please make sure SQL Server is running and try again.",
    "server":     "An unexpected server error occurred. Please try again.",
}


def _error_reply(key: str) -> ChatResponse:
    return ChatResponse(reply=ERROR_MESSAGES[key], session_id="")


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    messages = get_session(request.session_id)
    messages.append({"role": "user", "content": request.message})

    try:
        reply = chat(messages)

    except openai.AuthenticationError:
        return _error_reply("auth")

    except openai.RateLimitError:
        return _error_reply("ratelimit")

    except openai.APIConnectionError:
        return _error_reply("ai_conn")

    except openai.BadRequestError:
        return _error_reply("ai_general")

    except (OperationalError, DBAPIError):
        return _error_reply("db")

    except Exception:
        return _error_reply("server")

    messages.append({"role": "assistant", "content": reply})
    save_session(request.session_id, messages)

    return ChatResponse(reply=reply, session_id=request.session_id)
