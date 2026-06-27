from typing import List

_sessions: dict[str, List[dict]] = {}

MAX_MESSAGES = 20


def get_session(session_id: str) -> List[dict]:
    return _sessions.get(session_id, [])


def save_session(session_id: str, messages: List[dict]) -> None:
    # Keep only the last MAX_MESSAGES to control token usage
    _sessions[session_id] = messages[-MAX_MESSAGES:]


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
