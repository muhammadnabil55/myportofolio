from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Certificate
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import CertificateSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certificate_list(request):
    if request.method in ("GET", "HEAD"):
        certificate = Certificate.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            certificate = certificate.filter(title__icontains=title)
        serializer = CertificateSerializer(
            certificate, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = CertificateSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.prefetch_related("starred_by"), pk=certificate_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = CertificateSerializer(certificate, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        certificate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CertificateSerializer(
        certificate, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def certificate_star(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    if certificate.starred_by.filter(pk=request.user.pk).exists():
        certificate.starred_by.remove(request.user)
    else:
        certificate.starred_by.add(request.user)
    serializer = CertificateSerializer(certificate, context={"request": request})
    return Response(serializer.data)