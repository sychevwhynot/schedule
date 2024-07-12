from django import forms
from .models import Schedule, Address
from django.forms import inlineformset_factory

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['address', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }