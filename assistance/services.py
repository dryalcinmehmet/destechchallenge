from django.db import transaction

from assistance.utils import NearestDistance

from .models import AssistanceRequest, Provider, ServiceAssignment
from .tasks import notify_insurance_company_task


class AssistanceService:

    @classmethod
    def create_request(cls, data: dict) -> AssistanceRequest:
        return AssistanceRequest.objects.create(**data)

    @classmethod
    def find_nearest_available_provider(cls, lat: float, lon: float) -> Provider:
        """
        Sistem üzerindeki tüm müsait (is_available=True) provider'lar arasından
        kullanıcının bulunduğu konuma en yakın olan provider'ı döndürür.
        """
        providers = Provider.objects.filter(is_available=True)

        # Provider mevcutmu kontrolü yapılır.
        if not providers.exists():
            raise Exception("Müsait provider bulunamadı.")

        def distance(provider: Provider) -> float:
            """
            Her provider için müşterinin konumu ile provider'n konumu
            arasındaki gerçek km cinsinden uzaklığı hesaplar. Ayrı bir class olarak
            yazılmıştır. Solid prensiplere daha uygundur.
            """
            d = NearestDistance(
                lat1=lat, lon1=lon, lat2=provider.lat, lon2=provider.lon
            )
            return round(d.haversine_distance(), 2)

        # En küçük mesafeye sahip provider'ı seçiyoruz.
        return min(providers, key=distance)

    @classmethod
    def assign_provider_atomic(cls, request_id: int, provider_id: int = None):
        """
        Bu fonksiyonun orijinal halinde ki problemler:

        -  Race condition: Aynı anda iki işlem çalıştığında aynı provider iki kişiye atanabiliyordu.
        -  İşlem atomic değildi; yarıda hata olursa provider yanlışlıkla busy kalıyordu.
        -  Provider kaydı üzerinde select_for_update ile kilit yoktu. Bu fonksiyn veritabannda satırı kilitler.
           Yani aynı anda başka bir işlem bu satırı okuyabilir ancak güncelleymez. Böylece iki farklı işlem aynı
           provider'ı aynı anda müsait görüp çift atama yapamaz.
        -  Task, transaction commit olmadan tetikleniyordu. Buda başka bir problem.
        """
        with transaction.atomic():

            # Request'i kilitliyoruz --> başka bir işlem bu request üzerinde değişiklik yapamasın.
            req = AssistanceRequest.objects.select_for_update().get(id=request_id)

            # Provider elle verilmişse önce onu seçiyoruz.
            if provider_id:
                # Provider kaydını da select_for_update ile kilitliyoruz.
                provider = Provider.objects.select_for_update().get(id=provider_id)
            else:
                # Orijinal yapı korunarak en yakın provider seçimi devam ediyor.
                nearest = cls.find_nearest_available_provider(req.lat, req.lon)

                # Ancak atomic işlem içinde mutlaka FOR UPDATE ile kontrol edilmesi gerekir.
                provider = Provider.objects.select_for_update().get(id=nearest.id)
            """
                Orijinal kodda burada race condition oluyordu.
                provider tam bu satıra gelmeden başka bir işlem tarafından kullanılmaya başlamış olabiliyordu.
            """
            #
            if not provider.is_available:
                raise Exception("Provider is busy!")

            # Provider'ı müsait değile set ediyoruz. (artık müsait değil).
            provider.is_available = False
            provider.save(update_fields=["is_available"])

            # Atama kaydı oluşturuluyor.
            assignment = ServiceAssignment.objects.create(
                request=req, provider=provider
            )

            # Request'in durumu güncelleniyor.
            req.status = "DISPATCHED"
            req.save(update_fields=["status"])

            """
            Orijinal kodda sorun: Task transaction commit olmadan tetikleniyordu.
             İşlem rollback olursa task yine de çalışıyordu --> veri tutarsızlığı.
            """
            transaction.on_commit(lambda: notify_insurance_company_task.delay(req.id))

        return assignment

    @classmethod
    def complete_request(cls, request_id: int):
        """TODO: Talebi tamamla"""
        raise NotImplementedError()

    @classmethod
    def cancel_request(cls, request_id: int):
        """TODO: Talebi iptal et"""
        raise NotImplementedError()
