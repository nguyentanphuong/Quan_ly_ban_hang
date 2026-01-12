from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src_sales_manager_models_Version2 import Base
import os

DATABASE_URL = os.getenv("SALES_DB_URL", "sqlite:///sales.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False, future=True)
Session = scoped_session(SessionFactory)

def init_db():
    Base.metadata.create_all(engine)