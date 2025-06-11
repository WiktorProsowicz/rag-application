# -*- coding: utf-8 -*-
"""Contains functions to communicate with the entrypoint backend service."""
import logging
import os
from typing import Dict
from typing import List
from typing import Tuple

import httpx
import requests  # type: ignore


def collect_context_info(
        user_message: str, chat_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Collects context information based on the user's message and chat history."""

    logging.debug('Collecting context info with user_message: %s and chat_history: %s',
                  user_message, chat_history)

    url = f"{os.environ['BACKEND_API_URL']}/collect_context_info"
    payload = {
        'user_message': user_message,
        'chat_history': chat_history
    }

    response = requests.post(url, json=payload, timeout=5)
    response.raise_for_status()

    return response.json().get('context_docs', [])


def stream_chat_response(user_message: str,
                         chat_history: List[Tuple[str, str]],
                         context_docs: List[Dict[str, str]]):
    """Collects LLM response based on the context and streams it."""

    logging.debug(('Streaming chat response with user_message: %s, ' +
                   'chat_history: %s, context_docs: %s'),
                  user_message, chat_history, context_docs)

    url = f"{os.environ['BACKEND_API_URL']}/stream_chat_response"

    payload = {
        'user_message': user_message,
        'chat_history': chat_history,
        'context_docs': context_docs
    }

    yield from httpx.stream('POST', url, data=payload, timeout=5)
