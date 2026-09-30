from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
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
from django.views.decorators.http import require_POST 


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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "M. Nabil Hariri",
        "title_query": title_query,
        "form": CertificateForm(),
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
    certificates = Certificate.objects.prefetch_related('starred_by').all()

    if title_query:
        certificates = certificates.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for certificate in certificates:
        starred_users = certificate.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "id": str(certificate.id),
            "fields": {
                "title": certificate.title,
                "description": certificate.description,
                "thumbnail": certificate.thumbnail,
                "date_obtained": certificate.date_obtained,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

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
def toggle_star(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    if request.method == "POST":
        if request.user in certificate.starred_by.all():
            certificate.starred_by.remove(request.user)
        else:
            certificate.starred_by.add(request.user)

    return redirect("main:show_certificate")

@require_POST
def create_certificate_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = CertificateForm(request.POST)
    if form.is_valid():
        certificate = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "id": str(certificate.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)