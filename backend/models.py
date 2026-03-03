from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class StudentHistory(Base):
    __tablename__ = "student_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(255), index=True)
    topic = Column(String(255))
    score = Column(Float)
    confidence = Column(Float, default=0.0)
    strategy = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
