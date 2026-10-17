from django.shortcuts import render
from django.views.generic import ListView
from wards.models import Ward

# Create your views here.
class AllWardsView(ListView):
    model = Ward
    template_name = "wards/view_all.html"
    context_object_name = "wards"