from sqlalchemy import Column, Integer, String
from database import Base

class Clima(Base):
    __tablename__ = "climas"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)  # EX: "Joinville 18°"
