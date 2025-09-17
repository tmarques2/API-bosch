from core.configs import settings
from sqlalchemy import Column, Integer, String, Float, Boolean

class BandasModel(settings.DBBaseModel):
    __tablename__ = "bandas"

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    nome: str = Column(String(256))
    qtd_integrantes: int = Column(Integer())
    tipo_musical: str = Column(String(256))