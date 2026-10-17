from django.urls import path
from users.views import AllParentsView

urlpatterns = [
    path("parents/all", AllParentsView.as_view()),

]