from sqlalchemy import Column, Integer, String, Text
from database import Base

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    issue = Column(Text )
    context = Column(Text)
    analysis = Column(Text)
    created_at = Column(String)