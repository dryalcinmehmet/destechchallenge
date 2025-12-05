from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assistance.models import AssistanceRequest, Provider, ServiceAssignment

from drf_spectacular.utils import extend_schema, OpenApiExample

from .services import AssistanceService


class ProviderCreateView(APIView):
    """
    Yeni bir provider eklemek için kullanılcak POST endpoint.
    """

    @extend_schema(
        summary="Provider oluştur",
        description="Sisteme yeni bir provider ekler.",
        request={
            "application/json": {
                "name": "Ahmet",
                "phone": "5554443322",
                "lat": 41.01,
                "lon": 29.02,
            }
        },
        responses={
            201: dict,
            400: dict,
        },
    )
    def post(self, request):
        data = request.data

        try:
            provider = Provider.objects.create(
                name=data.get("name"),
                phone=data.get("phone"),
                lat=data.get("lat"),
                lon=data.get("lon"),
                is_available=True,
            )

            return Response(
                {
                    "status": "Provider created",
                    "id": provider.id,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProviderListView(APIView):
    """
    Sistemdeki tüm provider'ları listelemek için kullanıcak GET endpoint.
    """

    @extend_schema(
        summary="Provider listesini getir",
        description="Sistemdeki tüm provider kayıtlarını döndürür.",
        responses={200: list},
    )
    def get(self, request):
        providers = Provider.objects.all().values()
        return Response(list(providers), status=status.HTTP_200_OK)


class AssistanceRequestListView(APIView):
    """
    Assistance requestlerini listelemek için kullanıcak GET endpoint.
    """

    @extend_schema(
        summary="Assistance request listesini getir",
        description="Tüm assistance request kayıtlarını döndürür.",
        responses={200: list},
    )
    def get(self, request):
        requests = AssistanceRequest.objects.all().values()
        return Response(list(requests), status=status.HTTP_200_OK)


class AssistanceRequestCreateView(APIView):

    @extend_schema(
        summary="Yeni assistance request oluştur",
        description=(
            "Yeni bir assistance talebi oluşturur ve uygun provider'ı otomatik olarak atar."
        ),
        request={
            "application/json": {
                "customer_name": "Mehmet",
                "policy_number": "PL123456",
                "lat": 41.01,
                "lon": 29.02,
                "issue_desc": "Araç arızalandı",
            }
        },
        responses={
            201: dict,
            400: dict,
        },
    )
    def post(self, request):
        data = request.data
        try:
            assistance_req = AssistanceService.create_request(data)
            AssistanceService.assign_provider_atomic(assistance_req.id)

            return Response(
                {
                    "status": "Created",
                    "id": assistance_req.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AssistanceRequestCompleteView(APIView):

    @extend_schema(
        summary="Assistance request'i tamamla",
        description="Belirtilen assistance request'in durumunu COMPLETED yapar.",
        responses={200: dict, 400: dict, 501: dict},
    )
    def post(self, request, request_id):
        try:
            AssistanceService.complete_request(request_id)
            return Response({"status": "Completed"}, status=status.HTTP_200_OK)
        except NotImplementedError:
            return Response(
                {"error": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AssistanceRequestCancelView(APIView):

    @extend_schema(
        summary="Assistance request'i iptal et",
        description="Belirtilen assistance request'in durumunu CANCELLED yapar.",
        responses={200: dict, 400: dict, 501: dict},
    )
    def post(self, request, request_id):
        try:
            AssistanceService.cancel_request(request_id)
            return Response({"status": "Cancelled"}, status=status.HTTP_200_OK)
        except NotImplementedError:
            return Response(
                {"error": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
