FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]
WORKDIR /home/appuser/app

RUN groupadd -g 1000 appuser && useradd appuser -u 1000 -g 1000 -m -s /bin/bash

COPY . /home/appuser/app
RUN chown -R appuser:appuser /home/appuser/

USER appuser
RUN pip install --no-cache-dir .

EXPOSE 80
CMD ["python", "main.py"]
