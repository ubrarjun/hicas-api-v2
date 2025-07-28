FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg2 \
    firefox-esr \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libxss1 libxtst6 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver (fixed version)
RUN wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xzf geckodriver.tar.gz -C /usr/local/bin && \
    rm geckodriver.tar.gz

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port for Render
EXPOSE 10000

# Start app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
