from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
import streamlit as st
import requests
from PyPDF2 import PdfReader


@csrf_exempt
def index(request, **kwargs):

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            data = form.cleaned_data

            question = data['question']

            reader = PdfReader(data['file'])

            text = ''

            for page in reader.pages:
                text += page.extract_text()

            data = {
                'question' : question,
                'texte' : text,
            }

            return render(request, "django_nlp/result.html", data)
        
        else:

            return render(request, "django_nlp/index.html", {'form' : form})
    

    else:
        form = UploadFileForm()

        return render(request, "django_nlp/index.html", {'form' : form})
