from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

_server = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
_database = os.getenv("DB_NAME", "FlightDB")

_odbc = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={_server};"
    f"DATABASE={_database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(_odbc)}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
