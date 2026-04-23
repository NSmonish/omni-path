FROM python:3.11

# Install Chrome and ChromeDriver dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
# Add selenium to your requirements or install directly
RUN pip install selenium webdriver-manager beautifulsoup4 requests sqlalchemy geoalchemy2 psycopg2-binary

CMD ["python", "main.py"]