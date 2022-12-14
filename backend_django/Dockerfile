FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update

# COPY pyproject.toml poetry.lock ./

# RUN poetry install -n --no-root

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# CMD ["python", "application/manage.py", "runserver", "0.0.0.0:8000"]
