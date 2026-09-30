from django.forms import DateInput, ModelForm, TextInput, Textarea, URLInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from main.models import Certificate

class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = [
            "title",
            "description",
            "thumbnail",
            "date_obtained",
        ]

        labels = {
            "title": "Nama Sertifikat",
            "description": "Deskripsi Sertifikat",
            "thumbnail": "Gambar Sertifikat",
            "date_obtained": "Tanggal Sertifikat Didapat",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Sertifikat",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan tentang sertifikat ini",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
            "date_obtained": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
    
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()