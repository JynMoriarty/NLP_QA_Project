from django import forms

class UploadFileForm(forms.Form):
    
    question = forms.CharField(max_length=200)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):

        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.attrs.update({'placeholder':"Entrez votre question"})

        self.fields['file'].widget.attrs.update({'class':'pdf'})