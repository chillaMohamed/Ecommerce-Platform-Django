# 1. Base Image
FROM python:3.12-slim-bookworm

LABEL authors="mohamed-chilla"

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Work Directory
WORKDIR /app

# 4. Install System Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy Project Files
COPY . /app/

# 7. Expose Port
EXPOSE 8000


# 8. Command to Run the Django Server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]