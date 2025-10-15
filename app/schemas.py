from pydantic import BaseModel
from datetime import datetime

# Esquema base com os campos comuns de um Job.
class JobBase(BaseModel):
    prompt: str
    status: str
    output_url: str | None = None
    error_message: str | None = None

# Esquema para criar um novo Job (só precisamos do prompt).
class PromptRequest(BaseModel):
    prompt: str

# Esquema completo do Job para ser retornado pela API.
# Inclui campos da base de dados como id e timestamps.
class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    # Habilita o modo ORM para que o Pydantic possa ler
    # os dados diretamente de um objeto SQLAlchemy.
    class Config:
        orm_mode = True