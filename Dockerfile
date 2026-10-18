FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create data directory with full read/write permissions for SQLite (works on Hugging Face / Render / Koyeb)
RUN mkdir -p /data && chmod -R 777 /data && chmod -R 777 /app

ENV DATABASE_URL=sqlite+aiosqlite:////data/goldenera.db
ENV ENVIRONMENT=production
ENV PORT=7860

EXPOSE 7860

CMD ["python", "main.py"]
