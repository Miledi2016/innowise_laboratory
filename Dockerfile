# Using the official Python image as a base image
FROM python:3.11-slim

# Set up a working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory.
COPY . .

# Specify the port on which the container will listen.
EXPOSE 8000

# Defining a command to launch an application using Uvicorn
# 0.0.0.0 makes the application accessible outside of localhost inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]