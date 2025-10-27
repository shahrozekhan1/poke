
# dockerfile for the backend

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poppler and other dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements (if exists)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (adjust if needed)
COPY . .

# VOLUME ["/app"]
VOLUME /app


# Expose port 8000
EXPOSE 8000

# Run FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
# CMD [ "uvicorn",  "main:app",  "--reload", "--host", "0.0.0.0", "--port", "8000", "--reload-dir", "/app", "--reload-exclude", "logs", "--reload-exclude", "images", "--reload-exclude", "data_folder"]
