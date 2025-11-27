FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=5000

EXPOSE 5000

# For production you'd normally use gunicorn; for simplicity:
CMD ["python", "app.py"]
# Example gunicorn CMD:
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
