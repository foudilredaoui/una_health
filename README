# Glucose level API with Fastapi

This repository contains the source code and setup instructions for an Glucose level API built with Fastapi and Postgres.

## Table of Contents

- [Glucose_level_API](#Glucose_level_API)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
      - [Locally](#locally)
      - [Using Docker Compose](#using-docker-compose)
  - [Scripts](#scripts)
  - [Docker Compose](#docker-compose)
  - [API Documentation](#api-documentation)
  - [What I Would Improve:](#what-i-would-improve)

## Prerequisites

Before you begin, ensure you have the following installed:

- [python](https://www.python.org/) (>= v3.7.0)
- [Postgress](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) (optional)

## Getting Started

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:foudilredaoui/una_health.git
   cd una_health
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Configure your database connection in the environment variables.

### Running the Application

#### Locally

1. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

2. seed data:

   ```bash
   python run_migrations_and_populate.py
   ```

#### Using Docker Compose

1. Build and start all services:

   ```bash
   docker-compose up --build
   ```

## Scripts

- `scripts/checks.sh`: Format and Lint files.
- `pytest` or `PYTHONPATH=$(pwd) pytest`: Run all tests.

## Docker Compose

The `docker-compose.yml` file defines two services:

- `db`: Postgres database container.
- `web`: Fastapi application container.
- `migrate_and_populate`: Seed data to db

To start both services, run:

    ```bash
    docker-compose up --build
    ```

To start only the Postgress service, run:

    ```bash
    docker-compose up db
    ```

## API Documentation

API documentation will be available at \`http://localhost:8000/docs` when the application is running.

## What I Would Improve:

Given more time, there are several aspects I would focus on enhancing:
1- Implementing a proper error handling service
2- Implementing Logger using `Loguru`
3- Implementing k8s deployment and deploy it on docker-hub/gcp
4- deploy the solution on vercel
5- Implementing more robust caching strategies to optimise data retrieval from the api
6- Refactoring and cleaning up the codebase to enhance readability, maintainability, and overall quality.
7- Implementing a comprehensive testing framework to ensure code reliability and identify potential issues.
