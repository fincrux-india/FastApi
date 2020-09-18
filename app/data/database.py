from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Create a database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Create a SessionLocal class. Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
# But once we create an instance of the SessionLocal class, this instance will be the actual database session.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a Base class
Base = declarative_base()