import replicate
from .worker import celery_app
from .database import SessionLocal
from . import crud

@celery_app.task
def create_replicate_generation(job_id: int, prompt: str):
    """
    Esta é a tarefa que corre em segundo plano.
    Ela faz o trabalho pesado de comunicar com a API da Replicate.
    """
    # Um worker Celery é um processo separado, então ele precisa
    # criar a sua própria sessão com o banco de dados.
    db = SessionLocal()
    try:
        # 1. Informa a DB que o trabalho começou.
        crud.update_job(db, job_id=job_id, status="processing")

        # 2. Chama a API da Replicate. Esta é a parte demorada.
        #    Usamos replicate.run que espera até a conclusão.
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535523a55ff1e3b32d86de8a",
            input={"prompt": prompt}
        )
        
        # 3. Se tudo correu bem, atualiza a DB com o estado "succeeded" e o URL da imagem.
        image_url = output[0] if output else None
        crud.update_job(db, job_id=job_id, status="succeeded", output_url=image_url)

    except Exception as e:
        # 4. Se ocorreu um erro, guarda a mensagem de erro na DB.
        error_message = str(e)
        crud.update_job(db, job_id=job_id, status="failed", error_message=error_message)

    finally:
        # 5. É crucial fechar a sessão da DB no final.
        db.close()