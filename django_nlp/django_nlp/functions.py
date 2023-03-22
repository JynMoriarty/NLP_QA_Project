import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna
from dotenv import load_dotenv
import pandas as pd
from tqdm.auto import tqdm
import logging
from haystack.nodes import TextConverter
from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import convert_files_to_docs
from haystack.nodes import TextConverter, PDFToTextConverter, DocxToTextConverter, PreProcessor
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Document
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

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

    text= text.split('\n')

    for i in range(1,len(text)):
        text[i]=text[i].replace(" ","").replace('●', '').replace("\n"," ")
        context_list.append(text[i])
        title_list.append('test')


    df =pd.DataFrame({"title":title_list,"context":context_list})
    docs = []
    for d in df.iterrows():
        d = d[1]
        # create haystack document object with text content and doc metadata
        doc = Document(
            content=d["context"],
            meta={
                "title": d["title"],
                'context': d['context']
            }
        )
        docs.append(doc)
    
    dico = {}
    dico["texte"] = clean_text #pour azure
    dico['document'] = docs
    dico['contexte']=context_list #ce que j'affiche mais c'est une liste de de pages
    return dico

from haystack.nodes import PDFToTextConverter


def save_document(all_docs):

    document_store = InMemoryDocumentStore(use_bm25=True)
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=100,
        split_respect_sentence_boundary=True,
    )
    docs = preprocessor.process(all_docs)
    document_store.write_documents(docs)

    retriever = BM25Retriever(document_store=document_store)

    reader = FARMReader(model_name_or_path='etalab-ia/camembert-base-squadFR-fquad-piaf', use_gpu=True)

    pipe = ExtractiveQAPipeline(reader, retriever)
    
    return pipe

def extract_answer(pipe,query):
    prediction = pipe.run(
    query=query,
    params={
        "Retriever": {"top_k": 10},
        "Reader": {"top_k": 5}
    })

    return prediction['answers'][0]
