# -*- coding: utf-8 -*-
"""Contains the main entrypoint for the web application."""
import logging
import logging.config
import os
import time

import gradio as gr
import hydra
import omegaconf

import web


def _logger():
    return logging.getLogger('web_app')


if __name__ == '__main__':
    cfg = omegaconf.OmegaConf.create({
        'backend_entrypoint_url': "http://localhost:8080",
        'persistent_data_path': "/home/appuser/data",
        'web_app_port': 8888,
        'web_app_host': "localhost"
    })

    _logger().info('Starting web application with configuration: %s',
                   omegaconf.OmegaConf.to_yaml(cfg))

logging.config.dictConfig({
    'version': 1,
    'loggers': {
        'root': {
            'level': 'NOTSET',
            'handlers': ['console', 'file'],
            'propagate': True
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(cfg.persistent_data_path, f'web_{time.time_ns()}.log'),
            'mode': 'a',
            'level': 'DEBUG',
            'formatter': 'default'
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        }
    }
})

backend_service = web.backend_communication.BackendService(
    backend_url=cfg.backend_entrypoint_url
)

custom_css = """
.retrieved-docs {
  max-height: 30vh;
  overflow-y: auto;
}
"""

with gr.Blocks(fill_height=True, title='AGH Chat', css=custom_css) as web_app:
    web.gui.MainController(backend_service).render_gui()

web_app.launch(server_name=cfg.web_app_host,
               server_port=cfg.web_app_port)
