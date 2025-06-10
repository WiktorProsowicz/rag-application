# --------------------------------------------------
# This file contains setup scripts for the project.
# For more info, see: https://github.com/casey/just
# --------------------------------------------------

# Build and run all services
up-services:
    mkdir -p persistent_data/backend_entrypoint
    mkdir -p persistent_data/web
    docker-compose up

# Stop all services and remove containers
down-services:
    docker-compose down

# Clean up all Docker images
cleanup-services:
    docker rmi -f $(docker images -aq)