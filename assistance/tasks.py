from celery import shared_task
import logging
import time
import random

logger = logging.getLogger(__name__)


class InsuranceAPIError(Exception):
    """Sigorta API'si hatası"""
    pass


@shared_task(bind=True, max_retries=3)
def notify_insurance_company_task(self, request_id):
    """TODO: Retry mekanizması ekle"""
    logger.info(f"Sigorta bildirimi yapılıyor: Request ID {request_id}")
    
    # Mock API call
    time.sleep(1)
    
    # %30 ihtimalle hata fırlat
    if random.random() < 0.3:
        raise InsuranceAPIError("Connection timeout")
    
    logger.info(f"Bildirim Başarılı: Request ID {request_id}")
    return {"status": "success", "request_id": request_id}
