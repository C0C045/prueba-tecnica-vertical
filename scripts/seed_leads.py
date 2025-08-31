from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    budget = Column(Numeric, nullable=False)

# Datos de ejemplo
leads = [
    {"name": "Ana Salcedo", "location": "Medellín", "budget": 200000000},
    {"name": "Santiago Gallo", "location": "Medellín", "budget": 500000000},
    {"name": "Nicolle Rodríguez", "location": "Medellín", "budget": 650000000},
    {"name": "Pablo Sánchez", "location": "Bogotá", "budget": 350000000},
    {"name": "Andrés Arias", "location": "Bogotá", "budget": 150000000},
    {"name": "Andrés Limas", "location": "Bogotá", "budget": 450000000},
]

def main():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    for lead_data in leads:
        lead = Lead(**lead_data)
        session.merge(lead)
    session.commit()

    print("Leads insertados correctamente")

if __name__ == "__main__":
    main()
