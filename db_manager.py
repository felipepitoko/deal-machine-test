from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv('POSTGRES_USER', 'example')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'example')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'example')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    message = Column(String, nullable=False)
    keywords = Column(String, nullable=True)
    feeling = Column(String, nullable=True)
    intention = Column(String, nullable=True)    
    created_at = Column(DateTime, nullable=False)

def get_engine():
    return engine

def get_session():
    return SessionLocal()

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Table 'messages' created successfully.")
