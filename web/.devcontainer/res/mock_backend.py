

import asyncio
import json
import logging
import os
from typing import List, Tuple, Dict

import uvicorn
import pydantic
from fastapi import FastAPI
from fastapi.responses import StreamingResponse




app = FastAPI()

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

    mock_docs = [
        ("doc1", "This is the content of document 1." * 100),
        ("doc2", "This is the content of document 2."),
        ("doc3", "This is the content of document 3."),
    ]

    return ResponseCollectContextInfo(context_docs=mock_docs)

chat_response_count = 0

@app.post('/stream_chat_response')
async def stream_chat_response(request: RequestStreamChatResponse):

    mock_response1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
    exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
    in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
    sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est
    laborum."""

    mock_response2 = mock_response1.upper()

    responses = [
        mock_response1,
        mock_response2,
    ]

    global chat_response_count

    chat_response_count += 1

    response = responses[chat_response_count % len(responses)]

    async def event_generator():
        for token in  response.replace(' ', ' [split_token]') .split('[split_token]'):
            chunk = {"content": token}
            yield json.dumps(chunk).encode("utf-8")
            await asyncio.sleep(0.05)

    
    return StreamingResponse(event_generator(), media_type="application/json")


if __name__ == '__main__':

    uvicorn.run(
        'mock_backend:app',
        host='localhost',
        port=8080,
        reload=True
    )