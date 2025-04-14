from django import forms
from .models import Review

class RevieForm(forms.ModelForm):
  
  class Meta:
    model = Review
    fields = ['user','product','rating','comment']
    