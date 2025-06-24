FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose ports for Gradio (7860) and FastAPI (8000)
EXPOSE 8000 7860

# Default run command
CMD ["uvicorn", "spanishtutor.src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
