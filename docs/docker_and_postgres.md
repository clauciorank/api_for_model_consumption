## Docker Structure for Machine Learning Prediction API with PostgreSQL integration

This demonstrates how to containerize a Machine Learning Prediction API that interacts with a PostgreSQL database using Docker and Docker Compose. Below is an overview of the project structure and the key components of the Docker setup.

### PostgreSQL Initialization Script

The postgres-init/init.sql file is used to set up the necessary database tables for the machine learning predictions. Below is the content of the initialization script it will be run in the docker start:

```
CREATE TABLE IF NOT EXISTS predictions (
    id varchar PRIMARY KEY,
    predicted float,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prediction_variables (
    id varchar,
    variable_name varchar,
    variable_value varchar,
    model varchar,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

Explanation

- predictions Table: Stores each prediction with a unique id, the predicted value, and a timestamp.
- prediction_variables Table: Stores the variables used for each prediction, along with their values, the model version, and a timestamp.

### Dockerfile

The api/Dockerfile is used to build the Docker image for the Python API service, which serves machine learning predictions. Below is the content of the Dockerfile:

```
FROM python:3.8-slim

WORKDIR /api

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port your application runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "api/main.py"]

```

Explanation

- Base Image: python:3.8-slim is used as the base image.
- Working Directory: The working directory inside the container is set to /api.
- Dependencies: System dependencies (libpq-dev, gcc) and Python packages (from requirements.txt) are installed.
- Application Code: The application code is copied into the container.
- Port Exposure: The container exposes port 8080, which is where the API will run.
- Start Command: The container will run the Python application using main.py.

### Docker Compose

The docker-compose.yml file orchestrates the setup of multiple containers, specifically the Machine Learning Prediction API and PostgreSQL.

```
version: '3.3'

services:
  postgres:
    image: postgres
    container_name: my-postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres-init:/docker-entrypoint-initdb.d
    networks:
      - my-network

  python-api:
    build:
      context: .
      dockerfile: api/Dockerfile
    container_name: my-python-api
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_HOST: ${HOST}
    ports:
      - "8080:8080"
    volumes:
      - python-models:/api/models
    depends_on:
      - postgres
    networks:
      - my-network

volumes:
  postgres-data:
  python-models:

networks:
    my-network:

```

Explanation 

- Services:

    - postgres: Runs a PostgreSQL container with the environment variables POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB for database configuration. It maps port 5432 of the container to port 5432 on the host. The database schema is initialized using the init.sql script.
    - python-api: Builds the API Docker image using the api/Dockerfile and sets up environment variables to connect to the PostgreSQL service. It maps port 8080 of the container to port 8080 on the host.
- Volumes:

    - postgres-data: Persists PostgreSQL data to avoid data loss on container restarts.
    - python-models: Mounts the models directory to ensure the machine learning models are available inside the container.
- Networks:

    - my-network: A custom network is created to allow seamless communication between the postgres and python-api services.

### Usage

To start the services, run:
```
docker-compose up --build

```

This command builds the Docker images and starts the containers. The API will be available on http://localhost:8080, and PostgreSQL will be accessible on localhost:5432.

