# Base image with Python and system tools
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies required by Firefox and Selenium
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg2 \
    firefox-esr \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libxss1 libxtst6 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver (latest release)
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/') && \
    wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xzf geckodriver.tar.gz -C /usr/local/bin && \
    rm geckodriver.tar.gz

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Render uses PORT env)
EXPOSE 10000

# Start the server with dynamic port
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
