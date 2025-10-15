from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_job(db: Session, job_id: int):
    """Busca um job pelo seu ID."""
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def create_job(db: Session, prompt: str):
    """Cria um novo registo de job no banco de dados."""
    db_job = models.Job(prompt=prompt, status="pending")
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, status: str, output_url: str = None, error_message: str = None):
    """Atualiza o estado de um job existente."""
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = status
        db_job.output_url = output_url
        db_job.error_message = error_message
        db_job.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_job)
    return db_job