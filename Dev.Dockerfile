# Use the official Python image from the Docker Hub
FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Add the entry point script
COPY entrypoint_dev.sh /app/entrypoint_dev.sh
RUN chmod +x /app/entrypoint_dev.sh

# Set the entry point
ENTRYPOINT ["/app/entrypoint_dev.sh"]