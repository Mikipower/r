from sqlmodel import Field, SQLModel

class Pelicula(SQLModel, table=True):
    Titulo: str | None = Field(default=None, primary_key=True)
    Duracion: str = Field(index=True, max_length=50)
    Presupuesto: int = Field(gt=0)

