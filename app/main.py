from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from .tasks import create_replicate_generation

# Cria as tabelas no banco de dados (se não existirem) quando a aplicação inicia.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CortexCreate API")

# Lembre-se, o CORS já está no ficheiro de exemplo anterior,
# se não copiou, adicione o middleware aqui.
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate", response_model=schemas.Job)
async def start_generation(prompt_request: schemas.PromptRequest, db: Session = Depends(get_db)):
    """
    Endpoint de geração. Agora ele é super rápido:
    1. Cria o job na DB.
    2. Enfileira a tarefa no Celery.
    3. Retorna o job criado.
    """
    db_job = crud.create_job(db=db, prompt=prompt_request.prompt)
    
    # .delay() é como enviamos a tarefa para a fila do Celery.
    create_replicate_generation.delay(job_id=db_job.id, prompt=db_job.prompt)
    
    return db_job

@app.get("/status/{job_id}", response_model=schemas.Job)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """
    Endpoint de status. Apenas consulta o nosso banco de dados,
    o que é muito mais rápido e fiável.
    """
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job