from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import CertificateForm
from main.models import Experience, Certificate


def show_main(request):
    context = {
        "name": "M. Nabil Hariri",
        "npm": "2506602302",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada kompetisi IT dan pemrograman intuitif."
        ),
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

def create_certificate(request):
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

    certificate_json = serializers.serialize("json", certificate)
    return HttpResponse(certificate_json, content_type="application/json")

def delete_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    if request.method == "POST":
        certificate.delete()
        messages.success(request, "Sertifikat berhasil dihapus!")
        return redirect("main:show_certificate")

    return redirect("main:show_certificate")