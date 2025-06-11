# -*- coding: utf-8 -*-
""""Starts the backend server for the entrypoint service."""
import logging
import multiprocessing
import os

import uvicorn

from fastapi import FastAPI


if __name__ == '__main__':

    host = os.environ['HOST']
    port = int(os.environ['PORT'])
    dev_mode = bool(os.environ['DEV_MODE'])
    n_workers = (multiprocessing.cpu_count() * 2) + 1
    persistent_data_path = os.environ['PERSISTENT_DATA_PATH']

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(asctime)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(
                persistent_data_path, 'server.log'), mode='a')
        ]
    )

    logging.info('Starting server on %s:%d with %d workers.',
                 host, port, n_workers)

    if dev_mode:
        reload_args = {
            'reload': True,
            'reload_dirs': ['src'],
        }

    else:
        reload_args = {
            'reload': False,
        }

    uvicorn.run('api:app',
                host=host,
                port=port,
                workers=n_workers,
                log_level='info',
                access_log=True,
                limit_concurrency=1000,
                timeout_keep_alive=5,
                **reload_args)
