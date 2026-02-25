# Python 3.12 versiyasini tanlaymiz
FROM python:3.12-slim
# Terminalda xatoliklarni darrov ko'rish uchun
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Konteyner ichidagi ishchi papka
WORKDIR /app

# Pillow uchun kerakli tizim kutubxonalari
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*
# Pip-ni yangilash va kutubxonalarni o'rnatish
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Loyiha fayllarini ko'chirish
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
