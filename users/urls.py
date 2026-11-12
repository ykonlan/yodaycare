from django.urls import path
from users.views import AllParentsView, AllStaffView, CreateUserView, UpdateParentView, UpdateStaffView
from users.apis import AllParentsAPI, AllStaffAPI

urlpatterns = [
    path("parents/all", AllParentsView.as_view(), name="parents-view-all"),
    path("staff/all", AllStaffView.as_view(), name="staff-view-all"),
    path("create/<str:user_type>", CreateUserView.as_view(), name="create-new-user"),
    path("update-parent/<int:pk>", UpdateParentView.as_view(), name="update-parent"),
    path("update-staff/<int:pk>", UpdateStaffView.as_view(), name="update-staff"),
    path("apis/parents/all", AllParentsAPI.as_view(), name="all-parents-api"),
    path("apis/staff/all", AllStaffAPI.as_view(), name="all-staff-api"),
]