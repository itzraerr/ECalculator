FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    mpv \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:99

CMD ["/bin/bash", "-c", "Xvfb :99 -screen 0 1024x768x24 & python3 simplewebcal.py"]
