# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libxshmfence1 \
    fonts-liberation \
    libappindicator3-1 \
    libx11-6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver v0.36.0 (compatible with Firefox 128+)
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Set working directory
WORKDIR /app

# Copy your app code to the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Render will use
EXPOSE 10000

# Start using Gunicorn (Render sets PORT env var)
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
