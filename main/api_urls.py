from django.urls import path
from main import api_views
from rest_framework.authtoken import views as authtoken_views

app_name = "api"
urlpatterns = [
    path("certificate/", api_views.certificate_list, name="certificate-list"),
    path("certificate/<uuid:certificate_id>/", api_views.certificate_detail, name="certificate-detail"),
    path("certificate/<uuid:certificate_id>/star/", api_views.certificate_star, name="certificate-star"),
    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_views.api_logout, name="api_token_logout"),
]