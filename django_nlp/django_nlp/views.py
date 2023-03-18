from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
import requests
from PyPDF2 import PdfReader
from .functions import get_answer


@csrf_exempt
def index(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            question = data['question']

            reader = PdfReader(data['file'])

            text = ''

            for i, page in enumerate(reader.pages):                
                text += f'\n\nPage n°{i+1} :\n'
                text += page.extract_text()

            result = get_answer(text,question,0)

            text = text.split('\n')

            data = {
                'question' : question,
                'texte' : text,
                'result': result
            }

            return render(request, "django_nlp/result.html", data)
        
        else:

            return render(request, "django_nlp/index.html", {'form' : form})
    

    else:
        form = UploadFileForm()

        return render(request, "django_nlp/index.html", {'form' : form})
