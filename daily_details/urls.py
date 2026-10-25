from django.urls import path
from daily_details.views import AddDailyReportView

urlpatterns = [
    path("add/<int:ward_id>/", AddDailyReportView.as_view(), name="add-daily-report")
]