from django.urls import path
from main import api_views

app_name = "api"
urlpatterns = [
    path("certificate/", api_views.certificate_list, name="certificate-list"),
    path("certificate/<uuid:certificate_id>/", api_views.certificate_detail, name="certificate-detail"),
    path("certificate/<uuid:certificate_id>/star/", api_views.certificate_star, name="certificate-star"),
]