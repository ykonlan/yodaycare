from django.urls import path
from users.views import AllParentsView, AllStaffView, ProfileDashboard

urlpatterns = [
    path("parents/all", AllParentsView.as_view(), name="parents-view-all"),
    path("staff/all", AllStaffView.as_view(), name="staff-view-all"),
    path("admin/dashboard", ProfileDashboard.as_view(), name="dashboard"),
    path("staff/dashboard", ProfileDashboard.as_view(), name="dashboard"),
    path("parent/dashboard", ProfileDashboard.as_view(), name="dashboard"),
]