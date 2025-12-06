import re

from rest_framework import serializers

from .models import Provider


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

    # ----------- FIELD VALIDATION -------------

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
