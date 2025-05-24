from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from src.constants import DATABASE_PATH

engine: Engine = create_engine(
    DATABASE_PATH,
    connect_args={"check_same_thread": False}
)

SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)