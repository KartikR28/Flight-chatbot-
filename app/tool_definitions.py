TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_available_flights",
            "description": (
                "Search for flights between two cities departing after a given time. "
                "Use this when the user asks about available flights, wants to travel from one city to another, "
                "or asks what flights are left today."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Departure city, e.g. 'Mumbai', 'Delhi', 'Bangalore'",
                    },
                    "destination": {
                        "type": "string",
                        "description": "Arrival city, e.g. 'Mumbai', 'Delhi', 'Bangalore'",
                    },
                    "current_time": {
                        "type": "string",
                        "description": (
                            "ISO datetime to filter flights departing after this time. "
                            "Use the current datetime unless the user specifies otherwise. "
                            "Format: 'YYYY-MM-DD HH:MM'"
                        ),
                    },
                },
                "required": ["origin", "destination", "current_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_details",
            "description": (
                "Fetch full details for a specific flight by its flight number. "
                "Use this when the user mentions a flight number like 'AI-202' or asks about "
                "a specific flight's departure time, arrival time, or seat availability."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "type": "string",
                        "description": "The flight number to look up, e.g. 'AI-202', '6E-441', 'UK-985'",
                    },
                },
                "required": ["flight_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_travel_time_to_airport",
            "description": (
                "Get estimated travel time from a Mumbai locality to the airport. "
                "Optionally calculates what time the user should leave home based on a flight's departure time. "
                "Use this when the user asks how long it takes to reach the airport, "
                "or when they ask what time they should leave from a specific location."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "from_location": {
                        "type": "string",
                        "description": (
                            "Mumbai locality the user is travelling from. "
                            "Supported: 'Thane', 'Bandra', 'Andheri', 'Dadar', 'Navi Mumbai'"
                        ),
                    },
                    "flight_departure_time": {
                        "type": "string",
                        "description": (
                            "Optional. The flight's departure time in 'YYYY-MM-DD HH:MM' format. "
                            "Provide this to get a suggested leave-by time."
                        ),
                    },
                },
                "required": ["from_location"],
            },
        },
    },
]
