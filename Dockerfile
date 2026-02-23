FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    cmake \
    pkg-config \
    libfftw3-dev \
    libgsl-dev \
    libcfitsio-dev \
    python3-dev \
    make \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install -r /tmp/requirements.txt

CMD ["bash"]
