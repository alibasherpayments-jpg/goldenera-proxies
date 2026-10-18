FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create data directory for SQLite
RUN mkdir -p /data

ENV DATABASE_URL=sqlite+aiosqlite:////data/goldenera.db
ENV ENVIRONMENT=production
ENV PORT=8000

EXPOSE 8000

CMD ["python", "main.py"]
