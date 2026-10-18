from django.urls import path
from users.views import AllParentsView, AllStaffView

urlpatterns = [
    path("parents/all", AllParentsView.as_view(), name="parents-view-all"),
    path("staff/all", AllStaffView.as_view(), name="staff-view-all"),
    path("admin/dashboard", AllStaffView.as_view(), name="admin-dashboard"),
    path("staff/dashboard", AllStaffView.as_view(), name="staff-dashboard"),
    path("parent/dashboard", AllStaffView.as_view(), name="parent-dashboard"),
]