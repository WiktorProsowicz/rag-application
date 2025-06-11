FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]
WORKDIR /home/appuser/app

RUN apt update && apt install -y wget

RUN groupadd -g 1000 appuser && useradd appuser -u 1000 -g 1000 -m -s /bin/bash

RUN chown -R appuser:appuser /home/appuser/

USER appuser

EXPOSE 80
CMD ["/bin/bash", "./entrypoint.dev.bash"]