from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import date
from list.models import EmailQueue
from list.utils import send_email

logger = get_task_logger(__name__)

@periodic_task(run_every=(crontab(hour="3", minute="5")), ignore_result=True)
def send_emails():
  logger.info("Start send_emails() task...")
  eq = EmailQueue.objects.filter(send_date=date.today(), sent=False)
  count = 0
  for email in eq:
    success = send_email(email)
    if success:
      count += 1
  logger.info("Sent %d emails successfully!" % (count))
