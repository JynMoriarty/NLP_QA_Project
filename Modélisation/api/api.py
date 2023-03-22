from fastapi import FastAPI
from haystack.nodes import BM25Retriever, FARMReader, PreProcessor
from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import convert_files_to_docs
from haystack.pipelines import ExtractiveQAPipeline
from pydantic import BaseModel

import os


app=FastAPI()


document_store = InMemoryDocumentStore(use_bm25=True)

doc_dir = "./data/build_your_first_question_answering_system/"

all_docs = convert_files_to_docs(dir_path=doc_dir)

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

retriever = BM25Retriever(
    document_store=document_store)

reader = FARMReader(
    model_name_or_path="etalab-ia/camembert-base-squadFR-fquad-piaf",
    use_gpu=True)

pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)

class request(BaseModel):
    question: str


@app.post('/predict')
async def predict(request):
    return pipeline.run(
        query=request,
        params={
        "Retriever": {"top_k": 10},
        "Reader": {"top_k": 5}
    })
