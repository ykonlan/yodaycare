from django.urls import path
from wards.views import AllWardsView, CreateNewWard, UpdateWardView, ShowWardView, AllClassroomsView, ShowClassView
from wards.apis import AllWardsAPI

urlpatterns = [
    path("all/", AllWardsView.as_view(), name="wards-view-all"),
    path("create/", CreateNewWard.as_view(), name="create-new-ward"),
    path("update/<int:pk>", UpdateWardView.as_view(), name="update-ward"),
    path("view/<int:pk>", ShowWardView.as_view(), name="view-ward"),
    path("classes/all", AllClassroomsView.as_view(), name="classes-view-all"),
    path("classes/<int:pk>", ShowClassView.as_view(), name="class-view-by-id"),
    path("apis/all/", AllWardsAPI.as_view(), name="all-wards-api"),
    
]