FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -e .

EXPOSE 8000 7860

CMD ["uvicorn", "spanishtutor.src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
