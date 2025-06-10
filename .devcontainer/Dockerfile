FROM ubuntu:latest

RUN apt update && apt install -y \
    git \
    openssh-client \
    ca-certificates \
    curl \
    just

RUN wget -qO- https://astral.sh/uv/install.sh | sh
RUN apt update && apt install -y just

RUN git config --system core.sshCommand /usr/bin/ssh

# Keep the container running
CMD ["sleep", "infinity"]
