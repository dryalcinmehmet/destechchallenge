from django.urls import path

from .views import (AssistanceRequestCancelView, AssistanceRequestCompleteView,
                    AssistanceRequestCreateView)

urlpatterns = [
    path(
        "request/create/", AssistanceRequestCreateView.as_view(), name="request_create"
    ),
    path(
        "request/<int:request_id>/complete/",
        AssistanceRequestCompleteView.as_view(),
        name="request_complete",
    ),
    path(
        "request/<int:request_id>/cancel/",
        AssistanceRequestCancelView.as_view(),
        name="request_cancel",
    ),
]
