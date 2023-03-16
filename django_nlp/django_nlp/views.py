from django.shortcuts import render
import requests

def index(request):

    if request.method == 'POST':
        question = request.POST.get('question')
        pdf = request.POST.get('pdf')

        data = {
            'question': question,
            'pdf': pdf,
        }

        # headers = {"Content-Type": "application/json"}

        # url = "https://url-de-l'api"

        # response = requests.post(url, json=data, headers=headers)

    return render(request, "django_nlp/index.html")#, response)
