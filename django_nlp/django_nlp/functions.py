import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
from dotenv import load_dotenv
#pip install python-dotenv
#pip install azure-ai-language-questionanswering

def get_answer(text,question,accuracy):

    load_dotenv()
    endpoint = "https://question-answering-test-simplon.cognitiveservices.azure.com/"
    credential = AzureKeyCredential(os.getenv('credential'))
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        input = qna.AnswersFromTextOptions(
            question=question,
            text_documents=[text]
        )


        output = client.get_answers_from_text(input)

    best_answer = [a for a in output.answers if a.confidence > accuracy]

    

    dico = {}
    dico['reponse']= best_answer[0].answer
    dico['score']=output.answers[0].confidence

    return dico
