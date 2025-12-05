from django.contrib import admin

from .models import AssistanceRequest, Provider, ServiceAssignment


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "lat", "lon", "is_available", "created_at")
    list_filter = ("is_available", "created_at")
    search_fields = ("name", "phone")
    ordering = ("-created_at",)


@admin.register(AssistanceRequest)
class AssistanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "policy_number",
        "status",
        "lat",
        "lon",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "policy_number")
    ordering = ("-created_at",)


@admin.register(ServiceAssignment)
class ServiceAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "provider", "dispatched_at")
    list_filter = ("dispatched_at", "provider")
    search_fields = ("request__customer_name", "provider__name")
    ordering = ("-dispatched_at",)
