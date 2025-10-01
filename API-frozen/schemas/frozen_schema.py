from typing import Optional, List
from pydantic import BaseModel as SCBaseModel

class FrozenSchema(SCBaseModel):
    id: Optional[int] = None
    nome: str
    idade: int
    genero: str
    especie: str
    foto: Optional[str] = None
    
    class Config:
        orm_mode = True

class HistoriaBase(SCBaseModel):
    titulo: str
    descricao: Optional[str] = None
    personagem_id: int


class HistoriaSchema(HistoriaBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class PersonagemComHistorias(FrozenSchema):
    historias: List[HistoriaSchema] = []
