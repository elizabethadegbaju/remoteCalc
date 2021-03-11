"""remoteCalc.api URL Configuration"""
from django.urls import path

from api import views

API_TITLE = "Remote Calculator API"
API_DESCRIPTION = "A simple web service to implement a calculator."

urlpatterns = [
    path("calculus/", views.calculus, name="calculus")
]
