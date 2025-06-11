import asyncio
import json
import logging
import os
from typing import List, Tuple, Dict

from backend_entrypoint.chroma_retriever import ChromaRetriever
from backend_entrypoint.google_api import generate_answer
import pydantic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse



logging.basicConfig(level=logging.INFO)

vector_store_path = "../vector_store"
retriever = None

if os.path.isdir(vector_store_path):
    retriever = ChromaRetriever.from_persisted(vector_store_path)
    logging.info("Loaded ChromaRetriever from persisted vector store.")
else:
    logging.warning("Vector store not found at %s", vector_store_path)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('FRONTEND_APP_URL', '*')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class RequestCollectContextInfo(pydantic.BaseModel):
    user_message: str
    chat_history: List[Dict[str, str]]

class ResponseCollectContextInfo(pydantic.BaseModel):
    context_docs: List[Tuple[str, str]]

class RequestStreamChatResponse(pydantic.BaseModel):
    user_message: str
    chat_history: List[Dict[str, str]]
    context_docs: List[Tuple[str, str]]


@app.get('/ping')
async def read_ping():
    return {"message": "Service is running"}


@app.post('/collect_context_info')
async def collect_context_info(request: RequestCollectContextInfo) -> ResponseCollectContextInfo:
    logging.info("/collect_context_info - Message: %s", request.user_message)

    retrieved = retriever.retrieve(request.user_message, k=3) if retriever else []
    context_docs = [(doc["metadata"].get("title", "Untitled"), doc["text"]) for doc in retrieved]

    return ResponseCollectContextInfo(context_docs=context_docs)


@app.post('/stream_chat_response')
async def stream_chat_response(request: RequestStreamChatResponse):
    logging.info("/stream_chat_response - User message: %s", request.user_message)


    prompt_parts = [request.user_message] + [doc[1] for doc in request.context_docs]
    prompt = "\n".join(prompt_parts)

    logging.info("Prompt to model:\n%s", prompt[:300])

    answer = generate_answer(prompt) or "Brak odpowiedzi od modelu."

    async def event_generator():
        for token in answer.split():
            chunk = {"content": token}
            yield json.dumps(chunk).encode("utf-8")
            await asyncio.sleep(0.05)

    return StreamingResponse(event_generator(), media_type="application/json")
