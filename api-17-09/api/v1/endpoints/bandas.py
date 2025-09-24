from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.bandas_models import BandasModel
from schemas.bandas_schemas import BandaSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BandaSchema)
async def post_banda(banda: BandaSchema, db: AsyncSession = Depends(get_session)):

    nova_banda = BandasModel(nome=banda.nome, qtd_integrantes=banda.qtd_integrantes, tipo_musical=banda.tipo_musical)

    db.add(nova_banda)

    await db.commit()

    return nova_banda


@router.get("/", response_model=List[BandaSchema])
async def get_bandas(db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(BandasModel)
        result = await session.execute(query)
        bandas: List[BandasModel] = result.scalars().all()

        return bandas
    
@router.get("/{banda_id}", response_model=BandaSchema, status_code=status.HTTP_200_OK)
async def get_banda(banda_id: int, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(BandasModel).filter(BandasModel.id == banda_id)
        result = await session.execute(query)
        banda = result.scalar_one_or_none()

        if banda:
            return banda
        else:
            raise HTTPException(detail="Banda não encontrada", status_code=status.HTTP_404_NOT_FOUND)
        
@router.put("/{banda_id}", response_model=BandaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_banda(banda_id: int, banda: BandaSchema, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(BandasModel).filter(BandasModel.id == banda_id)
        result = await session.execute(query)
        banda_up = result.scalar_one_or_none()

        if banda_up:
            banda_up.nome = banda.nome
            banda_up.qtd_integrantes = banda.qtd_integrantes
            banda_up.tipo_musical = banda.tipo_musical

            await session.commit()
            return banda_up
        else:
            raise HTTPException(detail="Banda não encontrada", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{banda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banda(banda_id: int, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(BandasModel).filter(BandasModel.id == banda_id)
        result = await session.execute(query)
        banda_del = result.scalar_one_or_none()

        if banda_del:
            await session.delete(banda_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Banda não encontrada", status_code=status.HTTP_404_NOT_FOUND)