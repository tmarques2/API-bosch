from core.configs import settings
from typing import Optional
from sqlalchemy import Column, Integer, String

class FrozenModel(settings.DBBaseModel):
    __tablename__ = 'personagens'

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    idade: int = Column(Integer())
    genero: str = Column(String(100))
    especie: str = Column(String(100))
    foto: Optional[str] = Column(String(500), nullable=True)

    __allow_unmapped__ = True
