FROM ubuntu:latest


RUN apt update && apt install -y just git
RUN git config --system core.sshCommand /usr/bin/ssh

# Keep the container running
CMD ["sleep", "infinity"]
