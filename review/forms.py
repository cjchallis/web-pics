from django import forms
from .models import PicFile 

class PicForm(forms.ModelForm):

    class Meta:
        model = PicFile
        fields = ('path', 'name', 'status', 'filetype', 'thumbnail')
        widgets = {'path': forms.HiddenInput(),
                   'name': forms.HiddenInput(),
                   'status': forms.RadioSelect(),
                   'filetype': forms.HiddenInput(),
                   'thumbnail': forms.HiddenInput(),
                  }

