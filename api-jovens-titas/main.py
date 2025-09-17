from fastapi import FastAPI
from routes import personagens

app = FastAPI(
    title="API dos Jovens Titãs em Ação",
    version='0.0.2',
    description="Feita por Thainara Marques"
)

app.include_router(personagens.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)
