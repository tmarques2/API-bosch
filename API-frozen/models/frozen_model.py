from core.configs import settings
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Personagem(settings.DBBaseModel):
    __tablename__ = 'personagens'

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    idade: int = Column(Integer())
    genero: str = Column(String(100))
    especie: str = Column(String(100))
    foto: Optional[str] = Column(String(500), nullable=True)

    # relação com histórias
    historias = relationship("Historia", back_populates="personagem", cascade="all, delete")

    __allow_unmapped__ = True


class Historia(settings.DBBaseModel):
    __tablename__ = 'historias'

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    titulo: str = Column(String(100))
    descricao: str = Column(String(500))
    personagem_id: int = Column(Integer, ForeignKey("personagens.id"))

    # relação reversa
    personagem = relationship("Personagem", back_populates="historias")

    __allow_unmapped__ = True
