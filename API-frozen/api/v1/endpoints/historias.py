from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.frozen_model import Historia
from schemas.frozen_schema import HistoriaSchema, HistoriaBase
from core.deps import get_session

router = APIRouter()

# ------------------- POST -------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=HistoriaSchema)
async def post_historia(historia: HistoriaBase, db: AsyncSession = Depends(get_session)):

    nova_historia = Historia(
        titulo=historia.titulo,
        descricao=historia.descricao,
        personagem_id=historia.personagem_id
    )

    db.add(nova_historia)
    await db.commit()
    await db.refresh(nova_historia)

    return nova_historia


# ------------------- GET ALL -------------------
@router.get("/", response_model=List[HistoriaSchema])
async def get_historias(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Historia)
        result = await session.execute(query)
        historias: List[Historia] = result.scalars().all()

        return historias


# ------------------- GET BY ID -------------------
@router.get("/{historia_id}", response_model=HistoriaSchema, status_code=status.HTTP_200_OK)
async def get_historia(historia_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Historia).filter(Historia.id == historia_id)
        result = await session.execute(query)
        historia = result.scalar_one_or_none()

        if historia:
            return historia
        else:
            raise HTTPException(detail="História não encontrada", status_code=status.HTTP_404_NOT_FOUND)


# ------------------- PUT -------------------
@router.put("/{historia_id}", response_model=HistoriaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_historia(historia_id: int, historia: HistoriaBase, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Historia).filter(Historia.id == historia_id)
        result = await session.execute(query)
        historia_up = result.scalar_one_or_none()

        if historia_up:
            historia_up.titulo = historia.titulo
            historia_up.descricao = historia.descricao
            historia_up.personagem_id = historia.personagem_id

            await session.commit()
            return historia_up
        else:
            raise HTTPException(detail="História não encontrada", status_code=status.HTTP_404_NOT_FOUND)


# ------------------- DELETE -------------------
@router.delete("/{historia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_historia(historia_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Historia).filter(Historia.id == historia_id)
        result = await session.execute(query)
        historia_del = result.scalar_one_or_none()

        if historia_del:
            await session.delete(historia_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="História não encontrada", status_code=status.HTTP_404_NOT_FOUND)
