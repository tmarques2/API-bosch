from fastapi import APIRouter, HTTPException, status, Response, Depends
from typing import Optional, Dict, Any
from models import PersonagensJovensTitas

router = APIRouter()

def fake_db():
    try:
        print("Conectando com banco")
    finally:
        print("Fechando o banco")

personagens = {
    1: {
        "nome": "Robin",
        "idade": 16,
        "habilidade": "Luta",
        "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaS68URB2vMR0AyugEPfnP3v4X8f0eW6qNeQ&s"
    },
    2: {
        "nome": "Estelar",
        "idade": 17,
        "habilidade": "Voar, lazer",
        "foto": "https://w7.pngwing.com/pngs/201/382/png-transparent-teen-titans-star-fire-illustration-starfire-raven-robin-cyborg-red-x-teen-titans-go.png"
    },
    3: {
        "nome": "Ravena",
        "idade": 17,
        "habilidade": "Magia, telecinese",
        "foto": "https://i.pinimg.com/originals/dd/e3/75/dde375660a9ee944d0596f44b00a175d.jpg"
    },
    4: {
        "nome": "Mutano",
        "idade": 15,
        "habilidade": "Mutação em animais",
        "foto": "https://static.wikia.nocookie.net/teen-titans-go/images/d/d4/2b6b161ef7f2bc36031c6f772fdb9cd7.png/revision/latest?cb=20200124150531&path-prefix=pt-br"
    },
    5: {
        "nome": "Ciborgue",
        "idade": 19,
        "habilidade": "Metade robô",
        "foto": "https://i.pinimg.com/474x/44/20/82/442082b66b0bcef3315c33817476a53b.jpg"
    }
}

@router.get("/")
async def raiz():
    return {"mensagem": "funcionou"}

@router.get("/personagens")
async def get_personagens(db: Any = Depends(fake_db)):
    return personagens

@router.get("/personagens/{personagem_id}", description="Retorna um personagem com um id específico", summary="Retorna um personagem")
async def get_personagem(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

@router.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[PersonagensJovensTitas] = None):
    next_id = len(personagens) + 1
    personagens[next_id] = personagem
    del personagem.id
    return personagem

@router.put("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_personagem(personagem_id:int, personagem: PersonagensJovensTitas):
    if personagem_id in personagens:
        personagens[personagem_id] = personagem
        personagem.id = personagem_id
        del personagem.id
        return personagem
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

@router.delete("/personagens/{personagem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_personagem(personagem_id:int):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

@router.patch("/personagens/{personagem_id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_personagem(personagem_id: int, updates: Dict[str, Any]):
    if personagem_id not in personagens:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")

    for key, value in updates.items():
        if key in personagens[personagem_id]:
            personagens[personagem_id][key] = value

    return personagens[personagem_id]
