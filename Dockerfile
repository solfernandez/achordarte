FROM debian:bookworm-slim

WORKDIR /project

COPY achordi.py requirements_dev.txt ./
COPY achordarte/ achordarte/
COPY tests/ tests/

RUN apt-get update && apt-get install -q --yes \
    python3 \
    python3-pip \
    && pip install -q --no-cache-dir -r requirements_dev.txt --break-system-packages \
    && rm -rf /var/lib/apt/lists/*
      
CMD ["python3", "achordi.py"]

