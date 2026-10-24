from django.urls import path
from users.views import AllParentsView, AllStaffView, ProfileDashboard, CreateUserView, UpdateParentView

urlpatterns = [
    path("parents/all", AllParentsView.as_view(), name="parents-view-all"),
    path("staff/all", AllStaffView.as_view(), name="staff-view-all"),
    path("admin/dashboard", ProfileDashboard.as_view(), name="dashboard"),
    path("staff/dashboard", ProfileDashboard.as_view(), name="dashboard"),
    path("parent/dashboard", ProfileDashboard.as_view(), name="dashboard"),
    path("create/<str:user_type>", CreateUserView.as_view(), name="create-new-user"),
    path("update-parent/<int:pk>", UpdateParentView.as_view(), name="update-parent"),
]