from django import forms

class UploadFileForm(forms.Form):
    CHOICES = [
        ('../modelisation/api/data/model_fr/','FR'),
        ('../modelisation/api/data/model_en/','ENG'),
    ]
    
    
    question = forms.CharField(max_length=200)
    file = forms.FileField()
    language = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, )

    def __init__(self, *args, **kwargs):

        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['question'].widget.attrs.update({'class':'form-control', 'placeholder':"Entrez votre question"})

        self.fields['file'].widget.attrs.update({'class':'pdf form-control'})

