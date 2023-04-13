from django import forms
from .models import Advert, Response
from froala_editor.widgets import FroalaEditor


class AdvertForm(forms.ModelForm):
    text = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Advert
        fields = [
            'title',
            'category',
            'text',

        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]


class Response_Receive_Form(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'response_status',
        ]
        labels = {'response_status': 'Отметить отклик как принятый'}
