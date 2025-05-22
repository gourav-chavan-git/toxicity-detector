FROM python:3.11-slim

WORKDIR /app

# Install build tools (optional but helps with some Python packages like sentencepiece)
RUN apt-get update && apt-get install -y build-essential gcc

# Copy your project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "toxiccheck.wsgi:application", "--bind", "0.0.0.0:8000"]


