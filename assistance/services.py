import math
from django.db import transaction
from .models import AssistanceRequest, Provider, ServiceAssignment
from .tasks import notify_insurance_company_task


class AssistanceService:
    
    @classmethod
    def create_request(cls, data: dict) -> AssistanceRequest:
        return AssistanceRequest.objects.create(**data)

    @classmethod
    def find_nearest_available_provider(cls, lat: float, lon: float) -> Provider:
        """TODO: En yakın müsait provider'ı döndür"""
        raise NotImplementedError()

    @classmethod
    def assign_provider_atomic(cls, request_id: int, provider_id: int = None):
        """TODO: Bu metodu düzelt - mevcut haliyle sorunlar var"""
        req = AssistanceRequest.objects.get(id=request_id)
        
        if provider_id:
            provider = Provider.objects.get(id=provider_id)
        else:
            provider = cls.find_nearest_available_provider(req.lat, req.lon)
        
        if provider.is_available:
            provider.is_available = False
            provider.save()
            
            ServiceAssignment.objects.create(request=req, provider=provider)
            req.status = 'DISPATCHED'
            req.save()
            
            notify_insurance_company_task.delay(req.id)
        else:
            raise Exception("Provider is busy!")
    
    @classmethod
    def complete_request(cls, request_id: int):
        """TODO: Talebi tamamla"""
        raise NotImplementedError()
    
    @classmethod  
    def cancel_request(cls, request_id: int):
        """TODO: Talebi iptal et"""
        raise NotImplementedError()
