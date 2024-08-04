#!/bin/sh
black .
isort .
ruff check .
mypy .
