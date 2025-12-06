from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from assistance.models import AssistanceRequest, Provider, ServiceAssignment
from assistance.serializers import (AssistanceRequestCreateSerializer,
                                    AssistanceRequestSerializer,
                                    ProviderCreateSerializer,
                                    ProviderSerializer)

from .services import AssistanceService


class ProviderCreateView(APIView):
    @extend_schema(
        summary="Provider oluştur",
        request=ProviderCreateSerializer,
        responses={201: ProviderSerializer},
    )
    def post(self, request):
        serializer = ProviderCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Burada object create e ihtiyaç duyulmaz serializer save() methodu bunu handle eder.
        provider = serializer.save(is_available=True)

        return Response(
            ProviderSerializer(provider).data,
            status=status.HTTP_201_CREATED,
        )


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
        summary="Assistance request oluştur",
        request=AssistanceRequestCreateSerializer,
        responses={201: AssistanceRequestSerializer},
    )
    def post(self, request):
        serializer = AssistanceRequestCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        assistance_req = AssistanceService.create_request(serializer.validated_data)
        AssistanceService.assign_provider_atomic(assistance_req.id)

        return Response(
            AssistanceRequestSerializer(assistance_req).data,
            status=status.HTTP_201_CREATED,
        )


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
