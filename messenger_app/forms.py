from django import forms
from .models import Message


class NickNameSearch(forms.Form):
    nickname = forms.CharField(max_length=150, label='С кем начать переписку?', widget=forms.TextInput(attrs={"class": "form-control"}))


class WriteMsg(forms.ModelForm):
    class Meta:
        model = Message
        # fields = '__all__'
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={"class": "form-control"}),
        }