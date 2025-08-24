# Use the official Python image as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=pharma_cy.settings

# Set the working directory
WORKDIR /app

# Install system dependencies (optional but useful for common needs)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (excluding .env)
COPY . .
# Remove .env file from image for security
RUN rm -f .env

# Collect static files




# Expose port
EXPOSE 8080

# Start Gunicorn server using pharma_cy.wsgi:application
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8080 pharma_cy.wsgi:application"]
