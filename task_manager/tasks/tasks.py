# tasks.py
from celery import shared_task
from .models import Subscription
from .utils import generate_report
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)

@shared_task
def send_periodic_reports():
    logger.info("Starting to generate the reports.")
    current_time = timezone.now()

    subscriptions = Subscription.objects.filter(report_time=current_time.hour)

    for subscription in subscriptions:
        generate_report(subscription)
        logger.info(f"Report generated successfully for user: {subscription.user.email}")

    if not subscriptions:
        logger.info("No subscriptions to process at this hour.")
