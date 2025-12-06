import re

from rest_framework import serializers

from .models import AssistanceRequest, Provider, ServiceAssignment


class ProviderCreateSerializer(serializers.ModelSerializer):
    """
    Validasyonlu serializer methodu.
    """

    name = serializers.CharField(
        max_length=100, required=True, help_text="Provider'ın adı"
    )
    phone = serializers.CharField(
        required=True, help_text="10 haneli telefon numarası (örn: 5554443322)"
    )
    lat = serializers.FloatField(
        required=True, help_text="Enlem değeri (-90 ile 90 arası)"
    )
    lon = serializers.FloatField(
        required=True, help_text="Boylam değeri (-180 ile 180 arası)"
    )

    class Meta:
        model = Provider
        fields = ["name", "phone", "lat", "lon"]

    def validate_phone(self, value):
        if not re.fullmatch(r"^\d{10}$", value):
            raise serializers.ValidationError(
                "Telefon numarası 10 haneli ve rakamlardan oluşmalıdır."
            )
        return value

    def validate_lat(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Enlem -90 ile 90 arasında olmalıdır.")
        return value

    def validate_lon(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Boylam -180 ile 180 arasında olmalıdır.")
        return value


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
            "phone",
            "lat",
            "lon",
            "is_available",
            "created_at",
        ]
        read_only_fields = ["id", "is_available", "created_at"]


class AssistanceRequestCreateSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        required=True, max_length=100, help_text="Müşterinin adı"
    )
    policy_number = serializers.CharField(
        required=True, max_length=50, help_text="Poliçe numarası"
    )
    lat = serializers.FloatField(required=True, help_text="Konum enlemi")
    lon = serializers.FloatField(required=True, help_text="Konum boylamı")
    issue_desc = serializers.CharField(required=True, help_text="Arıza açıklaması")

    class Meta:
        model = AssistanceRequest
        fields = ["customer_name", "policy_number", "lat", "lon", "issue_desc"]

    def validate_customer_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Müşteri adı en az 2 karakter olmalıdır.")
        if not re.fullmatch(r"[A-Za-zığüşöçİĞÜŞÖÇ\s]+", value):
            raise serializers.ValidationError("Müşteri adı sadece harf içerebilir.")
        return value

    def validate_policy_number(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Poliçe numarası en az 6 karakter olmalıdır."
            )
        if not re.fullmatch(r"[A-Za-z0-9]+", value):
            raise serializers.ValidationError("Poliçe numarası alfanumerik olmalıdır.")
        return value

    def validate_lat(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError(
                "Geçersiz enlem değeri (-90 ile 90 arası)."
            )
        return value

    def validate_lon(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError(
                "Geçersiz boylam değeri (-180 ile 180 arası)."
            )
        return value

    def validate_issue_desc(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Sorun açıklaması en az 5 karakter olmalıdır."
            )
        return value


class AssistanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistanceRequest
        fields = [
            "id",
            "customer_name",
            "policy_number",
            "lat",
            "lon",
            "issue_desc",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]


class ServiceAssignmentSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer()

    class Meta:
        model = ServiceAssignment
        fields = ["provider", "dispatched_at"]
