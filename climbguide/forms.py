from django import forms
from .models import Route, Daytrip

class DaytripForm(forms.ModelForm):
    class Meta:
        model = Daytrip
        fields =[
            "title",
            "description",
            "date"
        ]
        widgets = {
            "date": forms.SelectDateWidget(
                empty_label=("Year", "Month", "Day"),
            ),
        }