# Use official Python image as base
FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    gnupg \
    ca-certificates \
    curl \
    unzip \
    xvfb \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libgbm1 \
    libgtk-3-0 \
    libxss1 \
    libxtst6 \
    libxshmfence-dev \
    && rm -rf /var/lib/apt/lists/*

# 🔽 Install GeckoDriver manually
RUN GECKO_VER=0.34.0 && \
    wget https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VER/geckodriver-v$GECKO_VER-linux64.tar.gz && \
    tar -xzf geckodriver-v$GECKO_VER-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v$GECKO_VER-linux64.tar.gz

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for Render
ENV PORT=10000
EXPOSE 10000

# Run the app using gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:10000"]
