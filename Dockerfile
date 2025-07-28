FROM python:3.10-slim

# Install Firefox & GeckoDriver
RUN apt-get update && \
    apt-get install -y firefox-esr wget unzip && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.36.0-linux64.tar.gz && \
    mv geckodriver /usr/bin/geckodriver && \
    chmod +x /usr/bin/geckodriver && \
    rm geckodriver-v0.36.0-linux64.tar.gz && \
    apt-get clean

# Install dependencies
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
