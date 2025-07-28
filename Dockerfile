# Use Python base image
FROM python:3.11-slim

# Install system dependencies and Firefox
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip ca-certificates \
    firefox-esr \
    libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 libdbus-glib-1-2 \
    libx11-xcb1 libxt6 libxss1 libasound2 libxrandr2 libxcomposite1 libxcursor1 \
    libxi6 libxtst6 libatk-bridge2.0-0 libxdamage1 libxfixes3 libxext6 libx11-6 \
    libxrender1 fonts-liberation libappindicator3-1 libdbusmenu-glib4 \
    libdbusmenu-gtk3-4 xdg-utils \
    && apt-get clean

# Install GeckoDriver 0.36.0 (compatible with Firefox 128)
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.36.0-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v0.36.0-linux64.tar.gz

# Set environment variables
ENV MOZ_HEADLESS=1
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000 and start the app using gunicorn
EXPOSE 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
