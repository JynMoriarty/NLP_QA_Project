from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
import requests
from PyPDF2 import PdfReader
from .functions import *

@csrf_exempt
def index(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            question = data['question']
        
            reader = PdfReader(data['file'])

            clean_data = get_cleantext_and_lists('doc_test',reader) # Retourne un dictionnaire contenant le texte clean et deux listes pour le df de pinecone
            result = get_answer(clean_data['texte'],question,0)


          
            
            
            score = result['score']

            data = {
                'question' : question,
                'score':score,
                'texte' : clean_data['contexte'],
                'result': result
            }

            return render(request, "django_nlp/result.html", data)
        
        else:

            return render(request, "django_nlp/index.html", {'form' : form})
    

    else:
        form = UploadFileForm()

        return render(request, "django_nlp/index.html", {'form' : form})
