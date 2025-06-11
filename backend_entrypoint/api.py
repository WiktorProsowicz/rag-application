# -*- coding: utf-8 -*-
"""Contains API of the entrypoint backend service."""
import asyncio
import logging
import os
from typing import List
from typing import Tuple
from typing import Dict
import json

import pydantic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse


class RequestCollectContextInfo(pydantic.BaseModel):
    """Contains the user's message and chat history."""
    user_message: str
    chat_history: List[Dict[str, str]]


class ResponseCollectContextInfo(pydantic.BaseModel):
    """Contains the context documents collected based on the user's message and chat history."""
    context_docs: List[Tuple[str, str]]


class RequestStreamChatResponse(pydantic.BaseModel):
    """Contains the user's message, chat history, and context information."""
    user_message: str
    chat_history: List[Dict[str, str]]
    context_docs: List[Tuple[str, str]]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ['FRONTEND_APP_URL']],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/ping')
async def read_ping():
    """Returns a dummy message for service health check."""
    return {'message': 'Service is running'}


@app.post('/collect_context_info')
async def collect_context_info(request: RequestCollectContextInfo) -> ResponseCollectContextInfo:
    """Collects context information based on the user's message and chat history."""

    logging.info('Requested /collect_info with user_message: %s and chat_history: %s',
                  request.user_message, request.chat_history)

    await asyncio.sleep(2)

    context_docs = [
        ('Document 1', 'This is the content of document 1.'),
        ('Document 2', 'This is the content of document 2.'),
        ('Document 3', 'This is the content of document 3.')
    ]

    return ResponseCollectContextInfo(context_docs=context_docs)


@app.post('/stream_chat_response')
async def stream_chat_response(request: RequestStreamChatResponse):
    """Streams the response from the LLM based on the provided context."""

    logging.info(('Requested /stream_chat_response with user_message: %s,' +
                   ' chat_history: %s, context_docs: %s'),
                  request.user_message, request.chat_history, request.context_docs)

    message = """
        In my company we use mostly httpx in our projects to do sync and async calls to our and other apis, but recently we ran into an issue, which (imo) could (and maybe should?) be solved:

    httpx.stream (in contrast to e.g. urlib and therefor requests etc. as well) does not return a file-like object - and that in turn breaks other packages which expect a file-like object, e.g. s3 stream upload via boto3 expects a file-like object, with the normal read(amount) method.

    Sure, I could write a proxy object to do this, but as this is quit a low level functionality it feels like that it's something this package should directly provide.
    """

    async def event_generator():
        for token in message.replace(' ', '\t ').split('\t'):

            chunk = {
                'content': token
            }

            chunk = json.dumps(chunk).encode('utf-8')

            yield chunk
            await asyncio.sleep(0.1)

    return StreamingResponse(event_generator(), media_type='application/json')
