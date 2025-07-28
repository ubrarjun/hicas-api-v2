# Use official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libu2f-udev \
    xdg-utils \
    firefox-esr \
    && apt-get clean

# Install geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4) && \
    wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver.tar.gz -C /usr/local/bin && \
    rm geckodriver.tar.gz

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port (Render will override this)
EXPOSE 10000

# Start using Gunicorn and read PORT from environment
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 90
