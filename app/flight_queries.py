from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Flight

AIRPORT_TRAVEL_TIMES = {
    "thane": 120,
    "bandra": 45,
    "andheri": 30,
    "dadar": 60,
    "navi mumbai": 90,
}


def get_available_flights(origin: str, destination: str, current_time: str) -> list:
    db = SessionLocal()
    try:
        cutoff = datetime.fromisoformat(current_time)
        flights = (
            db.query(Flight)
            .filter(
                Flight.origin.ilike(origin),
                Flight.destination.ilike(destination),
                Flight.departure_time > cutoff,
            )
            .order_by(Flight.departure_time)
            .all()
        )
        return [
            {
                "flight_number": f.flight_number,
                "origin": f.origin,
                "destination": f.destination,
                "departure_time": f.departure_time.strftime("%Y-%m-%d %H:%M"),
                "arrival_time": f.arrival_time.strftime("%Y-%m-%d %H:%M"),
                "seats_available": f.seats_available,
                "status": f.status,
            }
            for f in flights
        ]
    finally:
        db.close()


def get_flight_details(flight_number: str) -> dict:
    db = SessionLocal()
    try:
        flight = (
            db.query(Flight)
            .filter(Flight.flight_number.ilike(flight_number))
            .first()
        )
        if not flight:
            return {"error": f"No flight found with number '{flight_number}'"}
        return {
            "flight_number": flight.flight_number,
            "origin": flight.origin,
            "destination": flight.destination,
            "departure_time": flight.departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": flight.arrival_time.strftime("%Y-%m-%d %H:%M"),
            "seats_available": flight.seats_available,
            "status": flight.status,
        }
    finally:
        db.close()


def get_travel_time_to_airport(from_location: str, flight_departure_time: str = None) -> dict:
    key = from_location.strip().lower()
    travel_minutes = AIRPORT_TRAVEL_TIMES.get(key)

    if travel_minutes is None:
        known = ", ".join(AIRPORT_TRAVEL_TIMES.keys())
        return {"error": f"Unknown location '{from_location}'. Known locations: {known}"}

    result = {
        "from_location": from_location,
        "travel_minutes": travel_minutes,
    }

    if flight_departure_time:
        departure = datetime.fromisoformat(flight_departure_time)
        # 60-minute buffer for check-in and security
        leave_by = departure - timedelta(minutes=travel_minutes + 60)
        result["suggested_leave_by"] = leave_by.strftime("%Y-%m-%d %H:%M")
        result["buffer_minutes"] = 60

    return result
