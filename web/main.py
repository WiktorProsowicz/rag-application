# -*- coding: utf-8 -*-
"""Contains the main entrypoint for the web application."""
import logging
import logging.config
import os
import time

import gradio as gr

import web


def _rag_and_chat_stream(user_message, history):

    history = history or []
    chat_history = history.copy()

    history.append({
        'role': 'assistant',
        'content': 'Collecting context information...'
    })

    yield history

    context_docs = web.backend_communication.collect_context_info(
        user_message=user_message,
        chat_history=chat_history
    )

    history[-1]['content'] = ''

    yield history

    chat_response = web.backend_communication.stream_chat_response(
        user_message=user_message,
        chat_history=chat_history,
        context_docs=context_docs
    )

    full_text_response = ''
    for chunk in chat_response:
        token = chunk.get('content', '')
        full_text_response += token
        history[-1]['content'] = full_text_response

        yield history


def _obtain_gui():

    gui = gr.ChatInterface(
        _rag_and_chat_stream,
        chatbot=gr.Chatbot(elem_id='agh_chat', height=400, type='messages', show_copy_button=True),
        title='AGH Chat',
        type='messages',
        textbox=gr.Textbox(placeholder='Type a message...', label='Your message')
    )

    return gui


if __name__ == '__main__':

    persistent_data_path = os.environ['PERSISTENT_DATA_PATH']
    dev_mode = bool(os.environ['DEV_MODE'])

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(asctime)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(
                persistent_data_path, f'web_{time.time_ns()}.log'), mode='a')
        ]
    )

    gui_if = _obtain_gui()

    gui_if.launch(server_name='0.0.0.0',
                  server_port=80)
