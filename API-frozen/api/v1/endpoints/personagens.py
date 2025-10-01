from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.frozen_model import FrozenModel
from schemas.frozen_schema import FrozenSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FrozenSchema)
async def post_personagens(personagens: FrozenSchema, db: AsyncSession = Depends(get_session)):

    novo_personagens = FrozenModel(nome=personagens.nome, idade=personagens.idade, genero=personagens.genero, especie=personagens.especie, foto=personagens.foto)

    db.add(novo_personagens)

    await db.commit()

    return novo_personagens


@router.get("/", response_model=List[FrozenSchema])
async def get_personagens(db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(FrozenModel)
        result = await session.execute(query)
        personagens: List[FrozenModel] = result.scalars().all()

        return personagens
    
@router.get("/{personagens_id}", response_model=FrozenSchema, status_code=status.HTTP_200_OK)
async def get_personagens(personagens_id: int, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(FrozenModel).filter(FrozenModel.id == personagens_id)
        result = await session.execute(query)
        personagens = result.scalar_one_or_none()

        if personagens:
            return personagens
        else:
            raise HTTPException(detail="personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
@router.put("/{personagens_id}", response_model=FrozenSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_personagens(personagens_id: int, personagens: FrozenSchema, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(FrozenModel).filter(FrozenModel.id == personagens_id)
        result = await session.execute(query)
        personagens_up = result.scalar_one_or_none()

        if personagens_up:
            personagens_up.nome = personagens.nome
            personagens_up.idade = personagens.idade
            personagens_up.genero = personagens.genero
            personagens_up.especie = personagens.especie
            personagens_up.foto = personagens.foto

            await session.commit()
            return personagens_up
        else:
            raise HTTPException(detail="personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{personagens_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagens(personagens_id: int, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(FrozenModel).filter(FrozenModel.id == personagens_id)
        result = await session.execute(query)
        personagens_del = result.scalar_one_or_none()

        if personagens_del:
            await session.delete(personagens_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="personagem não encontrado", status_code=status.HTTP_404_NOT_FOUND)