import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
from dotenv import load_dotenv

def get_answer(text,question):

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

    best_answer = [a for a in output.answers if a.confidence > 0.5]

    print(u"Q: {}".format(input.question))
    print(u"A: {}".format(best_answer.answer))
    print("Confidence Score: {}".format(output.answers[0].confidence))
