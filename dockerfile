FROM python:3.8 as builder

# Setup working directory
WORKDIR /app
COPY . .

# Build
RUN python3 -m venv backend && . backend/bin/activate
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
