from django import forms
from .models import Source_File

class FileSearchForm(forms.ModelForm):
	class Meta:
		model = Source_File
		fields = ['url',]
	