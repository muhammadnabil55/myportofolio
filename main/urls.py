from django.urls import path

from main.views import show_main, show_experience, show_certificate

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("certificate/", show_certificate, name="show_certificate")
]