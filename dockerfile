FROM golang:1.19.4 as builder

# Setup working directory
WORKDIR /app
COPY . .

# Build
RUN pip3 install -r requirements.txt

FROM ubuntu:latest
WORKDIR /app
COPY . .

# built binary
COPY --from=builder /app/account .

EXPOSE 5000
CMD ["uvicorn", "app:app", "--port", "5000", "--workers", "4"]
