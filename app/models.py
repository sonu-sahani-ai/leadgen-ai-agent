from sqlalchemy import Column, Integer, String
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    website = Column(String)
    email = Column(String)
    score = Column(Integer)
