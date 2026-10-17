from django.urls import path
from wards.views import AllWardsView

urlpatterns = [
    path("all/", AllWardsView.as_view()),
    
]