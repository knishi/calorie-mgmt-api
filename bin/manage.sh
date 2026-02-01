#!/bin/bash
# Project Management Script

set -e

COMMAND=$1

case $COMMAND in
    test)
        tox -e py3
        ;;
    dist-clean)
        find . -type d -name "__pycache__" -exec rm -rf {} +
        find . -type d -name ".tox" -exec rm -rf {} +
        find . -type d -name "*.egg-info" -exec rm -rf {} +
        ;;
    db-migrate)
        alembic upgrade head
        ;;
    db-revision)
        alembic revision --autogenerate -m "$2"
        ;;
    *)
        echo "Usage: $0 {test|dist-clean|db-migrate|db-revision 'message'}"
        exit 1
esac
