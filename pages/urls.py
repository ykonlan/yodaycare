from django.urls import path
from pages.views import HomePageView, SeeGeneralReportParentView, SeeGeneralReportAdminView, SeeGeneralReportStaffView


urlpatterns = [
    path("", HomePageView.as_view(), name="login"),
    path("general-report-parent/<int:pk>", SeeGeneralReportParentView.as_view(), name="view-general-report-parent"),
    path("general-report-admin/", SeeGeneralReportAdminView.as_view(), name="view-general-report-admin"),
    path("general-report-staff/", SeeGeneralReportStaffView.as_view(), name="view-general-report-staff"),

]