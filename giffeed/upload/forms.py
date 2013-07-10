from django import forms


class UploadForm(forms.Form):
    url = forms.URLField(max_length=100)
    tags = forms.CharField()
    comment = forms.CharField()
