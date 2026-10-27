from django.urls import path
from daily_details.views import AddDailyReportView, SeeDailyReportView

urlpatterns = [
    path("add/<int:ward_id>/", AddDailyReportView.as_view(), name="add-daily-report"),
    path("view/<int:pk>/", SeeDailyReportView.as_view(), name="view-daily-report")
]