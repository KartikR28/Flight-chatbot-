import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

from app.tool_definitions import TOOLS
from app.flight_queries import (
    get_available_flights,
    get_flight_details,
    get_travel_time_to_airport,
)

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
_base_url = os.getenv("AI_BASE_URL") or None  # None = OpenAI default
_model = os.getenv("AI_MODEL", "gpt-4o")

client = OpenAI(api_key=_api_key, base_url=_base_url)

FUNCTION_MAP = {
    "get_available_flights": get_available_flights,
    "get_flight_details": get_flight_details,
    "get_travel_time_to_airport": get_travel_time_to_airport,
}

SYSTEM_PROMPT = """You are a helpful flight assistant chatbot. You help users find flights, check flight statuses, and plan travel from Mumbai.

Current date and time: {current_datetime}

Guidelines:
- When the user asks about available flights, use the current time as the filter unless they specify otherwise.
- Present flight info clearly: flight number, departure/arrival times, seats, and status.
- If a flight is cancelled or full, say so clearly and suggest alternatives.
- Be concise and friendly."""


def _execute_tool_call(tool_call) -> dict:
    fn_name = tool_call.function.name
    fn_args = json.loads(tool_call.function.arguments)
    fn = FUNCTION_MAP.get(fn_name)
    if fn is None:
        return {"error": f"Unknown function: {fn_name}"}
    return fn(**fn_args)


def chat(messages: list) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    system_message = {"role": "system", "content": SYSTEM_PROMPT.format(current_datetime=now)}
    full_messages = [system_message] + messages

    # Step 1: Send messages + tools to OpenAI
    response = client.chat.completions.create(
        model=_model,
        messages=full_messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    # Step 2: Check if OpenAI wants to call any tools
    if not message.tool_calls:
        return message.content

    # Step 3 & 4: Execute all tool calls (handles multiple in one turn)
    full_messages.append(message)

    for tool_call in message.tool_calls:
        result = _execute_tool_call(tool_call)
        full_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

    # Step 5: Send tool results back — no tools passed so model just replies
    final_response = client.chat.completions.create(
        model=_model,
        messages=full_messages,
    )

    return final_response.choices[0].message.content
