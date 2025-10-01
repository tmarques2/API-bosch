from fastapi import APIRouter

from api.v1.endpoints import personagens, historias

api_router = APIRouter()

api_router.include_router(personagens.router, prefix='/personagens', tags=["Personagens"])
api_router.include_router(historias.router, prefix="/historias", tags=["Histórias"])