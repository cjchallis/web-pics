from django import forms
from .models import PicFile 

class PicForm(forms.ModelForm):

    class Meta:
        model = PicFile
        fields = ('path', 'status',)
        widgets = {'path': forms.HiddenInput(),
                   'status': forms.RadioSelect()}

