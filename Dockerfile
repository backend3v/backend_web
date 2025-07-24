# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download es_core_news_sm

# Install Bito CLI

RUN apt-get update
RUN apt-get install -y curl sudo grep
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo


COPY install.sh /app/install.sh
RUN chmod +x /app/install.sh
RUN sudo /app/install.sh

RUN apt-get clean
RUN bito -v
RUN echo "bito:\n    access_key: eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidjFfODE5NV8xMjYyODA2Xzc0MDYzM19Nb24gTm92IDE4IDIyOjUyOjAwIFVUQyAyMDI0In0.AMf6d2e3Ds3po4uDWLQz4Ir8bwnmfVXcrKYOR9nwtb4\n    email: backendev.py@gmail.com\n    preferred_ai_model: BASIC\nsettings:\n    auto_update: true\n    max_context_entries: 20"\ > ~/.bitoai/etc/bito-cli.yaml
RUN cat ~/.bitoai/etc/bito-cli.yaml
RUN bito config -l
RUN cd ~/.bitoai/etc
RUN rm -rf /var/lib/apt/lists/*

RUN ls
# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["python", "__init__.py"]