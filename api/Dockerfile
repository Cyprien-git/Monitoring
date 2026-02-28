FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY pyflux.py .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["uvicorn", "pyflux:app", "--host=0.0.0.0", "--port=5000"]
