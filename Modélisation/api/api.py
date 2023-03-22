from fastapi import FastAPI
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from pydantic import BaseModel

import os


app=FastAPI()


document_store = InMemoryDocumentStore(use_bm25=True)

doc_dir = "./data/build_your_first_question_answering_system/"

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]

indexing_pipeline = TextIndexingPipeline(document_store)

indexing_pipeline.run_batch(
    file_paths=files_to_index)

retriever = BM25Retriever(
    document_store=document_store)

reader = FARMReader(
    model_name_or_path="deepset/roberta-base-squad2")

pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)

class request(BaseModel):
    question: str


@app.post('/predict')
async def predict(request):
    return pipeline.run(
        query=request)
