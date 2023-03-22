from django import forms

class UploadFileForm(forms.Form):
    
    question = forms.CharField(max_length=200)
    file = forms.FileField()
    language = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):

        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.attrs.update({'class':'form-control', 'placeholder':"Entrez votre question"})

        self.fields['file'].widget.attrs.update({'class':'pdf form-control'})

        self.fields['language'].widget.attrs.update({'class':'form-control', 'placeholder':"Entrez la langue "})
