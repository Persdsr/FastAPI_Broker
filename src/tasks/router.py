from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_config import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")
# celery - celery -A tasks.tasks:celery worker --loglevel=INFO --pool=solo
# flower - celery -A tasks.tasks:celery flower
@router.get("/dashboard")
def get_dashboard_report():
    # 1400 ms - Клиент ждет
    # send_email_report_dashboard('persdsr')
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    # background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    send_email_report_dashboard.delay('Persdsr')
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }