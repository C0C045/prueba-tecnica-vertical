from sqlalchemy import Column, Integer, String, Numeric
from .database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    budget = Column(Numeric, nullable=False)
