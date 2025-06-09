FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]

RUN addgroup --system appgroup && adduser --system appuser

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN chown -R appuser:appgroup /app
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER appuser
EXPOSE 80
CMD ["python", "start_server.py"]