FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pytest directly
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install pytest==7.4.0 pandas==2.0.3

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]