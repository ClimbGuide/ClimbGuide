from django import forms
from .models import Daytrip, Photo, Pointofinterest

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


class PointofinterestForm(forms.ModelForm):
    class Meta:
        model = Pointofinterest
        fields = [
            "name",
            "information",
            "longitude",
            "latitude",
            "public",
            "category"
        ]


