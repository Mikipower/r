from sqlmodel import create_engine, SQLModel, Session
from src.models.pelicula import Pelicula

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "peliculasdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Pelicula(Titulo="E.T", Duracion="1 hora y 50 minutos", Presupuesto=60000000))
        session.add(Pelicula(Titulo="Australia", Duracion="3 horas y 5 minutos", Presupuesto=100000000))
        session.add(Pelicula(Titulo="Avatar", Duracion="2 horas y media", Presupuesto=150000000))
        session.commit()
        #session.refresh_all()