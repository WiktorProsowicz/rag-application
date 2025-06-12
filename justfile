# --------------------------------------------------
# This file contains setup scripts for the project.
# For more info, see: https://github.com/casey/just
# --------------------------------------------------

set shell := ["bash", "-c"]

# Run static repository checks
run-pre-commit:
    uv run pre-commit run --all-files

# Set up environment and install dependencies
setup-dev:
    uv venv
    uv sync --project . --extra dev

# Build and run all services
up-services:
    mkdir -p persistent_data/backend_entrypoint
    mkdir -p persistent_data/web
    docker-compose -f docker-compose.dev.yml up

# Stop all services and remove containers
down-services:
    docker-compose -f docker-compose.dev.yml down

# Clean up all Docker images
cleanup-services:
    docker images --format '{{{{.Repository}}:{{{{.Tag}} {{{{.ID}}' | \
    grep '^rag-application-.*' | \
    awk '{print $2}' | \
    xargs -r docker rmi
