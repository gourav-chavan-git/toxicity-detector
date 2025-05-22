FROM python:3.13-slim

WORKDIR /app

# Copy your project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Run Gunicorn as the container start command
CMD ["gunicorn", "toxiccheck.wsgi:application", "--bind", "0.0.0.0:8000"]

