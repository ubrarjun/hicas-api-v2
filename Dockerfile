# Dockerfile

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Firefox + dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    curl gnupg unzip wget \
    libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 \
    libxt6 libxrandr2 libasound2 libxss1 libnss3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver 0.36.0 (Linux 64-bit)
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Run the app with gunicorn (Render will inject $PORT)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
