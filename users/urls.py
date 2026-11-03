from django.urls import path
from users.views import AllParentsView, AllStaffView, ProfileDashboard, CreateUserView, UpdateParentView, UpdateStaffView

urlpatterns = [
    path("parents/all", AllParentsView.as_view(), name="parents-view-all"),
    path("staff/all", AllStaffView.as_view(), name="staff-view-all"),
    path("create/<str:user_type>", CreateUserView.as_view(), name="create-new-user"),
    path("update-parent/<int:pk>", UpdateParentView.as_view(), name="update-parent"),
    path("update-staff/<int:pk>", UpdateStaffView.as_view(), name="update-staff"),
]