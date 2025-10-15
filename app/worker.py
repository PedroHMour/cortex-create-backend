import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# URL do nosso broker (Redis), lido das variáveis de ambiente.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Cria a instância da aplicação Celery.
celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL # Usamos Redis também para guardar resultados se necessário
)

celery_app.conf.update(
    task_track_started=True,
)