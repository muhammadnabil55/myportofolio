from django.urls import path

from main.views import login_user, logout_user, register, show_main, show_experience, show_certificate, create_certificate, get_certificate_json, delete_certificate, toggle_star

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("certificate/", show_certificate, name="show_certificate"),
    path("certificate/add/", create_certificate, name="create_certificate"),
    path("api/certificate/", get_certificate_json, name="get_certificate_json"),
    path("certificate/<uuid:certificate_id>/delete/",delete_certificate,name="delete_certificate"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("certificate/<uuid:certificate_id>/star/", toggle_star, name="toggle_star"),
]