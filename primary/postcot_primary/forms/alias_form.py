from django import forms

from ..models import Alias


class AliasForm(forms.ModelForm):
    class Meta:
        model = Alias
        exclude = []
