import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# URL de conexão com o banco de dados, lido das variáveis de ambiente.
# Exemplo: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv("DATABASE_URL")

# O 'engine' é o ponto de entrada para o banco de dados.
engine = create_engine(DATABASE_URL)

# Cada instância de SessionLocal será uma sessão com o banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usaremos esta Base para criar os nossos modelos de DB (ORM).
Base = declarative_base()

# Função de dependência para o FastAPI: garante que a sessão
# com o banco de dados seja aberta no início do request e fechada no final.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()