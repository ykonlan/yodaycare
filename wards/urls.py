from django.urls import path
from wards.views import AllWardsView, CreateNewWard, UpdateWardView

urlpatterns = [
    path("all/", AllWardsView.as_view(), name="wards-view-all"),
    path("create/", CreateNewWard.as_view(), name="create-new-ward"),
    path("update/<int:pk>", UpdateWardView.as_view(), name="update-ward"),
    
]