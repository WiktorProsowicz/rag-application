# -*- coding: utf-8 -*-
"""Contains API of the entrypoint backend service."""
from fastapi import FastAPI

app = FastAPI()


@app.get('/ping')
async def read_ping():
    """Returns a dummy message for service health check."""
    return {'message': 'Service is running'}
