FROM ubuntu:latest

RUN wget -qO- https://astral.sh/uv/install.sh | sh
RUN apt update && apt install -y just

# Keep the container running
CMD ["sleep", "infinity"]
