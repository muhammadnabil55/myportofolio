from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import CertificateForm
from main.models import Experience, Certificate
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "M. Nabil Hariri",
        "npm": "2506602302",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "M. Nabil Hariri",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_certificate(request):
    json_response = get_certificate_json(request)

    certificate = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    certificate = [cert.object for cert in certificate]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "M. Nabil Hariri",
        "certificate_list": certificate,
        "title_query": title_query,
    }
    return render(request, "certificate.html", context)

@login_required(login_url="/login/")
def create_certificate(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    form = CertificateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Sertifikat baru berhasil ditambahkan!")
        return redirect("main:show_certificate")

    context = {
        "name": "M. Nabil Hariri",
        "form": form,
    }
    return render(request, "certificate_form.html", context)

def get_certificate_json(request):
    title_query = request.GET.get("title", "").strip()
    certificate = Certificate.objects.all()

    if title_query:
        certificate = certificate.filter(title__icontains=title_query)

    certificate_json = serializers.serialize(
        "json", certificate, use_natural_foreign_keys=True
    )
    return HttpResponse(certificate_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_certificate(request, certificate_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    certificate = get_object_or_404(Certificate, id=certificate_id)

    if request.method == "POST":
        certificate.delete()
        messages.success(request, "Sertifikat berhasil dihapus!")
        return redirect("main:show_certificate")

    return redirect("main:show_certificate")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "M. Nabil Hariri",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "M. Nabil Hariri",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    certificate = get_object_or_404(Certificate, id=project_id)

    if request.method == "POST":
        if request.user in certificate.starred_by.all():
            certificate.starred_by.remove(request.user)
        else:
            certificate.starred_by.add(request.user)

    return redirect("main:show_projects")