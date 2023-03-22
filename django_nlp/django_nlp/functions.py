import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
from dotenv import load_dotenv
import re
import pandas as pd
from tqdm.auto import tqdm
import pinecone
import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pprint import pprint
from haystack.document_stores import PineconeDocumentStore
from haystack import Document
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader
from haystack.nodes import EmbeddingRetriever

#!pip install -U farm-haystack>=1.3.0 pinecone-client datasets
#pip install python-dotenv
#pip install azure-ai-language-questionanswering
#!pip install -qU datasets pinecone-client sentence-transformers torch

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



def get_cleantext_and_lists(title,reader):
    """
    prend un titre et reader_file object et retourne un dictionnaire avec un texte,liste de titre et une liste de contexte par pages
    """
    title_list = []
    context_list = []
    text = ''
    clean_text = ''
    for i, page in enumerate(reader.pages):                
        text += f'\n\nPage n°{i+1} :\n'
        n =page.extract_text()
        text += n
    clean_text = text.replace(" ","").replace('●', '').replace("\n"," ") # pour azure
    text= text.split('\n\n')

    for i in range(1,len(text)):
        text[i]=text[i].replace(" ","").replace('●', '').replace("\n"," ")
        context_list.append(text[i])
        title_list.append('test')


    df =pd.DataFrame({"title":title_list,"context":context_list})
    
    
    dico = {}
    dico["texte"] = clean_text
    dico['dataframe'] = df
    dico['contexte']=context_list # pour haystack/pinecone et ce qu'on va afficher

    return dico