# Minimal sandbox image: no CUDA/GUI/Playwright. Just supervisor + tcp_server + research libs via uv.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    ANONYMIZED_TELEMETRY=false \
    UV_SYSTEM_PYTHON=1

WORKDIR /workplace

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    bash \
    tree \
    unzip \
    zip \
    supervisor \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install uv and Python deps via uv (faster, reproducible)
RUN python3 -m pip install --no-cache-dir uv
COPY requirements.txt /tmp/requirements.txt
RUN cd /tmp && uv pip install --python 3.11 --system -r requirements.txt

# App files
RUN mkdir -p /app
COPY tcp_server.py /app/tcp_server.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Ensure log dir exists
RUN mkdir -p /var/log/supervisor

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
