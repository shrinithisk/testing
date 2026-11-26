# Hadolint violations: unpinned latest tag, running as root
FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Runs as root user (no USER instruction)
CMD ["python", "app.py"]
