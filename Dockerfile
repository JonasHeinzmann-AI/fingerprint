# Use the official Python image from Docker Hub
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && wget https://chromedriver.storage.googleapis.com/120.0.6099.71/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of your application code into the container
COPY . /app/

# Expose the port that your FastAPI application will run on
EXPOSE 8000

# Command to run your FastAPI application
CMD ["python", "main.py"]
