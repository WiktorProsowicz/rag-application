# -*- coding: utf-8 -*-
"""Contains functions to communicate with the entrypoint backend service."""
import logging
import os
from typing import Dict
from typing import List
from typing import Tuple
import json

import httpx
import requests  # type: ignore


def collect_context_info(
        user_message: str, chat_history: List[Dict[str, str]]) -> List[Tuple[str, str]]:
    """Collects context information based on the user's message and chat history."""

    logging.info('Collecting context info with user_message: %s and chat_history: %s',
                  user_message, chat_history)

    url = f"{os.environ['BACKEND_ENTRYPOINT_URL']}/collect_context_info"
    payload = {
        'user_message': user_message,
        'chat_history': chat_history
    }

    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()

    return response.json().get('context_docs', [])


def stream_chat_response(user_message: str,
                         chat_history: List[Dict[str, str]],
                         context_docs: List[Tuple[str, str]]):
    """Collects LLM response based on the context and streams it."""

    logging.info(('Streaming chat response with user_message: %s, ' +
                   'chat_history: %s, context_docs: %s'),
                  user_message, chat_history, context_docs)

    url = f"{os.environ['BACKEND_ENTRYPOINT_URL']}/stream_chat_response"

    payload = {
        'user_message': user_message,
        'chat_history': chat_history,
        'context_docs': context_docs
    }

    with httpx.stream('POST', url, json=payload, timeout=5) as stream:
        for chunk in stream.iter_bytes():
            yield json.loads(chunk.decode('utf-8'))
