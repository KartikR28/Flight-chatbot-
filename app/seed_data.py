import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, date, timedelta
from app.database import SessionLocal, engine
from app.models import Base, Flight


def dt(base_date, hour, minute):
    return datetime(base_date.year, base_date.month, base_date.day, hour, minute)


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    db.query(Flight).delete()

    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)

    flights = [
        # ── TODAY ──────────────────────────────────────────────────────────────

        # Mumbai → Delhi (~2h 15m)
        Flight(flight_number="AI-202", origin="Mumbai",    destination="Delhi",     departure_time=dt(today,  6,  0), arrival_time=dt(today,  8, 15), seats_available=45, status="on_time"),
        Flight(flight_number="6E-441", origin="Mumbai",    destination="Delhi",     departure_time=dt(today,  8, 30), arrival_time=dt(today, 10, 45), seats_available=12, status="on_time"),
        Flight(flight_number="SG-119", origin="Mumbai",    destination="Delhi",     departure_time=dt(today, 11,  0), arrival_time=dt(today, 13, 15), seats_available=0,  status="on_time"),
        Flight(flight_number="UK-985", origin="Mumbai",    destination="Delhi",     departure_time=dt(today, 14, 30), arrival_time=dt(today, 16, 45), seats_available=33, status="delayed"),
        Flight(flight_number="AI-806", origin="Mumbai",    destination="Delhi",     departure_time=dt(today, 18,  0), arrival_time=dt(today, 20, 15), seats_available=60, status="on_time"),

        # Delhi → Bangalore (~2h 45m)
        Flight(flight_number="AI-504", origin="Delhi",     destination="Bangalore", departure_time=dt(today,  7,  0), arrival_time=dt(today,  9, 45), seats_available=22, status="on_time"),
        Flight(flight_number="6E-316", origin="Delhi",     destination="Bangalore", departure_time=dt(today,  9, 30), arrival_time=dt(today, 12, 15), seats_available=8,  status="delayed"),
        Flight(flight_number="SG-221", origin="Delhi",     destination="Bangalore", departure_time=dt(today, 13,  0), arrival_time=dt(today, 15, 45), seats_available=41, status="on_time"),
        Flight(flight_number="UK-878", origin="Delhi",     destination="Bangalore", departure_time=dt(today, 16, 30), arrival_time=dt(today, 19, 15), seats_available=0,  status="cancelled"),
        Flight(flight_number="AI-912", origin="Delhi",     destination="Bangalore", departure_time=dt(today, 20,  0), arrival_time=dt(today, 22, 45), seats_available=55, status="on_time"),

        # Mumbai → Bangalore (~1h 45m)
        Flight(flight_number="AI-632", origin="Mumbai",    destination="Bangalore", departure_time=dt(today,  6, 30), arrival_time=dt(today,  8, 15), seats_available=18, status="on_time"),
        Flight(flight_number="6E-551", origin="Mumbai",    destination="Bangalore", departure_time=dt(today,  9,  0), arrival_time=dt(today, 10, 45), seats_available=30, status="on_time"),
        Flight(flight_number="SG-333", origin="Mumbai",    destination="Bangalore", departure_time=dt(today, 12,  0), arrival_time=dt(today, 13, 45), seats_available=5,  status="delayed"),
        Flight(flight_number="UK-763", origin="Mumbai",    destination="Bangalore", departure_time=dt(today, 15,  0), arrival_time=dt(today, 16, 45), seats_available=47, status="on_time"),
        Flight(flight_number="AI-717", origin="Mumbai",    destination="Bangalore", departure_time=dt(today, 19,  0), arrival_time=dt(today, 20, 45), seats_available=25, status="on_time"),

        # Delhi → Mumbai (~2h 15m)  [return route]
        Flight(flight_number="AI-303", origin="Delhi",     destination="Mumbai",    departure_time=dt(today,  7, 30), arrival_time=dt(today,  9, 45), seats_available=38, status="on_time"),
        Flight(flight_number="6E-712", origin="Delhi",     destination="Mumbai",    departure_time=dt(today, 15,  0), arrival_time=dt(today, 17, 15), seats_available=22, status="on_time"),

        # Bangalore → Delhi (~2h 45m)  [return route]
        Flight(flight_number="SG-445", origin="Bangalore", destination="Delhi",     departure_time=dt(today,  9,  0), arrival_time=dt(today, 11, 45), seats_available=15, status="delayed"),
        Flight(flight_number="AI-619", origin="Bangalore", destination="Delhi",     departure_time=dt(today, 17, 30), arrival_time=dt(today, 20, 15), seats_available=50, status="on_time"),

        # Bangalore → Mumbai (~1h 45m)  [return route]
        Flight(flight_number="UK-234", origin="Bangalore", destination="Mumbai",    departure_time=dt(today, 11,  0), arrival_time=dt(today, 12, 45), seats_available=0,  status="on_time"),

        # ── TOMORROW ───────────────────────────────────────────────────────────

        Flight(flight_number="AI-204", origin="Mumbai",    destination="Delhi",     departure_time=dt(tomorrow,  7,  0), arrival_time=dt(tomorrow,  9, 15), seats_available=60, status="on_time"),
        Flight(flight_number="6E-318", origin="Delhi",     destination="Bangalore", departure_time=dt(tomorrow, 10,  0), arrival_time=dt(tomorrow, 12, 45), seats_available=45, status="on_time"),
        Flight(flight_number="SG-505", origin="Delhi",     destination="Mumbai",    departure_time=dt(tomorrow, 13,  0), arrival_time=dt(tomorrow, 15, 15), seats_available=30, status="on_time"),
        Flight(flight_number="AI-720", origin="Bangalore", destination="Mumbai",    departure_time=dt(tomorrow, 16,  0), arrival_time=dt(tomorrow, 17, 45), seats_available=25, status="on_time"),
        Flight(flight_number="6E-553", origin="Mumbai",    destination="Bangalore", departure_time=dt(tomorrow,  8,  0), arrival_time=dt(tomorrow,  9, 45), seats_available=40, status="on_time"),

        # ── DAY AFTER TOMORROW ─────────────────────────────────────────────────

        Flight(flight_number="UK-987", origin="Mumbai",    destination="Delhi",     departure_time=dt(day_after,  9,  0), arrival_time=dt(day_after, 11, 15), seats_available=55, status="on_time"),
        Flight(flight_number="AI-305", origin="Delhi",     destination="Mumbai",    departure_time=dt(day_after, 14,  0), arrival_time=dt(day_after, 16, 15), seats_available=42, status="on_time"),
        Flight(flight_number="6E-620", origin="Bangalore", destination="Delhi",     departure_time=dt(day_after,  8, 30), arrival_time=dt(day_after, 11, 15), seats_available=18, status="on_time"),
        Flight(flight_number="SG-335", origin="Mumbai",    destination="Bangalore", departure_time=dt(day_after, 13,  0), arrival_time=dt(day_after, 14, 45), seats_available=35, status="on_time"),
        Flight(flight_number="QP-101", origin="Delhi",     destination="Bangalore", departure_time=dt(day_after, 16,  0), arrival_time=dt(day_after, 18, 45), seats_available=28, status="on_time"),
    ]

    db.add_all(flights)
    db.commit()
    db.close()
    print(f"Seeded {len(flights)} flights ({today} / {tomorrow} / {day_after}).")


if __name__ == "__main__":
    seed()
