from django.urls import path
from users.views import AllParentsView, AllStaffView

urlpatterns = [
    path("parents/all", AllParentsView.as_view()),
    path("staff/all", AllStaffView.as_view()),
]