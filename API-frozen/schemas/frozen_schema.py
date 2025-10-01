from typing import Optional
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

    