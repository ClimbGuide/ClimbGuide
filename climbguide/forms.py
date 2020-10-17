from django import forms
from .models import Daytrip, Photo

class DaytripForm(forms.ModelForm):
    class Meta:
        model = Daytrip
        fields = [
            "title",
            "description",
            "date"
        ]
        widgets = {
            "date": forms.SelectDateWidget(
                empty_label=("Year", "Month", "Day"),
            ),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "photo",
            "description"
        ]