import logging
import random
import time

from celery import shared_task

logger = logging.getLogger(__name__)


class InsuranceAPIError(Exception):
    """Sigorta API'si hatası"""

    pass


@shared_task(bind=True, max_retries=3)
def notify_insurance_company_task(self, request_id):
    """
    - Mock hata durumlarında celery nin retry methodunu kullanabiliriz..
    - Exponential backoff uygulayarak bekleme süresinin logaritmik olarak
      artmasını sağlıyoruz.
    """

    logger.info(f"Sigorta bildirimi yapılıyor: Request ID={request_id}")

    try:
        # Mock API call
        # Gerçek bir HTTP isteği yerine kısa bir gecikme veriyoruz..
        time.sleep(1)

        # %30 ihtimalle hata fırlat
        if random.random() < 0.3:
            raise InsuranceAPIError("Connection timeout")

        # İşlem başarılıysa normal akış devam eder.
        logger.info(f"Sigorta bildirimi başarılı: Request ID={request_id}")
        return {"status": "success", "request_id": request_id}

    except Exception as exc:
        # Üstel bekleme süresi (örn: 2 - 4 - 8 saniye)
        retry_delay = 2 ** (self.request.retries + 1)

        logger.warning(
            f"Sigorta bildirimi başarısız oldu. "
            f"Request ID={request_id}, Deneme={self.request.retries + 1}, "
            f"{retry_delay} saniye sonra tekrar denenecek..."
        )

        raise self.retry(exc=exc, countdown=retry_delay)
