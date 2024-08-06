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