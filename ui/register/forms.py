from django import forms

from .models import register

class PostForm(forms.ModelForm):

    class Meta:
        model = register
        file = forms.FileField()
        fields = ('username', 'password','mqttuser','mqttpass','port')