from typing import Optional
from pydantic import BaseModel

class PersonagensJovensTitas(BaseModel):
    id: Optional[int] = None
    nome: str
    idade: int
    habilidade: str
    foto: Optional[str] = None