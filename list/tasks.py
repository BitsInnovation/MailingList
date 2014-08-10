from __future__ import absolute_import
from datetime import date
from list.models import EmailQueue
from list.utils import send_email
from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)

@shared_task
def send_emails():
  logger.info("Starting task...")
  eq = EmailQueue.objects.filter(send_date=date.today(), sent=False)
  logger.info("Trying to send %d emails..." % (len(eq)))
  count = 0
  for email in eq:
    success = send_email(email)
    if success:
      count += 1
  logger.info("Successfully sent %d emails" % (count))
