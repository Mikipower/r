from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func
from src.models.pelicula import Pelicula
from src.data.db import init_db, get_session


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/peliculas", response_model=list[Pelicula])
def lista_coches(session: SessionDep):
    peliculas = session.exec(select(Pelicula)).all()
    return peliculas

@app.post("/peliculas", response_model=Pelicula)
def nueva_pelicula(pelicula: Pelicula, session: SessionDep):
    pelicula_encontrada = session.get(Pelicula, pelicula.Titulo)
    if pelicula_encontrada:
        raise HTTPException(status_code=400, detail="Esa Pelicula ya existe")
    session.add(pelicula)
    session.commit()
    session.refresh(pelicula)
    return pelicula

@app.delete("/peliculas/{pelicula_Titulo}")
def borrar_pelicula(pelicula_Titulo: str, session: SessionDep):
    pelicula_encontrada = session.get(Pelicula, pelicula_Titulo)
    if not pelicula_Titulo:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    session.delete(pelicula_Titulo)
    session.commit()
    return {"mensaje": "Pelicula eliminada"}


@app.patch("/peliculas/{pelicula_Titulo}", response_model=Pelicula)
def actualiza_pelicula(pelicula_Titulo: str, pelicula: Pelicula, session: SessionDep):
    pelicula_Titulo = session.get(Pelicula, pelicula_Titulo)
    if not pelicula_Titulo:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    pelicula_data = pelicula.model_dump(exclude_unset=True)
    pelicula_Titulo.sqlmodel_update(pelicula_data)
    session.add(pelicula_Titulo)
    session.commit()
    session.refresh(pelicula_Titulo)
    return pelicula_Titulo

@app.put("/peliculas", response_model=Pelicula)
def reemplaza_pelicula(pelicula: Pelicula, session: SessionDep):
    pelicula_encontrada = session.get(Pelicula, pelicula.Titulo)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    pelicula_data = pelicula.model_dump()
    pelicula_encontrada.sqlmodel_update(pelicula_data)
    session.add(pelicula_encontrada)
    session.commit()
    session.refresh(pelicula_encontrada)
    return pelicula_encontrada
